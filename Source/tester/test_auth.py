import argparse
from datetime import UTC, datetime, timedelta
import hashlib
import json
import os
import shutil
import tempfile
import urllib.error
import urllib.request
import unittest
from unittest import mock
from http.cookies import SimpleCookie
from types import SimpleNamespace

import logger
import storage
import util.auth
import util.player_cookie_store
import util.versions
import web_server.endpoints.badges as badges_api
import web_server.endpoints.funds as funds_api
import web_server.endpoints.join_data as join_data
from routines import player as player_routine
import web_server.endpoints.users_api as users_api


class fake_server:
    def __init__(
        self,
        data_storage: storage.storager,
        game_config=None,
    ) -> None:
        self.storage = data_storage
        self.game_config = game_config


class fake_handler:
    def __init__(
        self,
        data_storage: storage.storager,
        *,
        body: bytes = b"",
        cookie_header: str | None = None,
        query: dict[str, str | list[str]] | None = None,
        game_config=None,
    ) -> None:
        self.server = fake_server(data_storage, game_config)
        self.game_config = game_config
        self._body = body
        self.headers: dict[str, str] = {}
        if cookie_header is not None:
            self.headers["Cookie"] = cookie_header
        self.client_address = ("127.0.0.1", 12345)
        raw_query = query or {}
        self.query_lists = {
            key: (
                value
                if isinstance(value, list) else
                [value]
            )
            for key, value in raw_query.items()
        }
        self.query = {
            key: value[0]
            for key, value in self.query_lists.items()
        }
        self.hostname = "https://localhost:2005"
        self.port_num = 2005
        self.domain = "localhost"
        self.url_split = SimpleNamespace(query="")
        self.wfile = SimpleNamespace(
            write=lambda *_args, **_kwargs: None,
            flush=lambda: None,
        )
        self.status_code: int | None = None
        self.response_headers: list[tuple[str, str]] = []
        self.json_body = None
        self.data_body: bytes | None = None

    def read_content(self) -> bytes:
        return self._body

    def send_response(self, status: int) -> None:
        self.status_code = status

    def send_header(self, key: str, value: str) -> None:
        self.response_headers.append((key, value))

    def end_headers(self) -> None:
        return

    def send_json(
        self,
        json_data,
        status: int | None = 200,
        prefix: bytes = b"",
    ) -> None:
        assert isinstance(prefix, bytes)
        if status is not None:
            self.status_code = status
        self.json_body = json_data

    def send_data(
        self,
        text: bytes | str,
        status: int | None = 200,
        content_type: str | None = None,
    ) -> None:
        if isinstance(text, str):
            text = text.encode("utf-8")
        if status is not None:
            self.status_code = status
        if content_type is not None:
            self.response_headers.append(("Content-Type", content_type))
        self.data_body = text


class TestAuth(unittest.TestCase):
    def make_storage(self) -> storage.storager:
        temp_dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, temp_dir, True)
        return storage.storager(
            os.path.join(temp_dir, "test.sqlite"),
            force_init=False,
        )

    @staticmethod
    def make_game_config(
        badges: dict[int, object] | None = None,
        data_storage: storage.storager | None = None,
    ):
        return SimpleNamespace(
            storage=data_storage,
            game_setup=SimpleNamespace(
                roblox_version=util.versions.VERSION_MAP["v463"],
            ),
            remote_data=SimpleNamespace(
                badges=badges or {},
            ),
            server_core=SimpleNamespace(
                metadata=SimpleNamespace(
                    title="Test Universe",
                ),
                chat_style=SimpleNamespace(value="Classic"),
                retrieve_default_funds=lambda *_args: 0,
                retrieve_account_age=lambda *_args: 0,
                check_user_allowed=SimpleNamespace(
                    cached_call=lambda *_args: True,
                ),
            ),
        )

    @staticmethod
    def get_cookie_value(
        response_headers: list[tuple[str, str]],
        cookie_name: str,
    ) -> str | None:
        for header, value in response_headers:
            if header.lower() != "set-cookie":
                continue
            cookie = SimpleCookie()
            cookie.load(value)
            if cookie_name in cookie:
                return cookie[cookie_name].value
        return None

    def test_signup_login_and_authenticated_user_flow(self) -> None:
        data_storage = self.make_storage()
        signup_handler = fake_handler(
            data_storage,
            body=json.dumps({
                "username": "Tester_One",
                "password": "secret123",
            }).encode("utf-8"),
        )

        self.assertTrue(util.auth.HandleSignup(signup_handler))
        self.assertEqual(signup_handler.status_code, 200)

        signup_token = self.get_cookie_value(
            signup_handler.response_headers,
            util.auth.AUTH_COOKIE_NAME,
        )
        self.assertIsNotNone(signup_token)
        assert signup_token is not None
        self.assertTrue(util.auth.ValidateToken(data_storage, signup_token))

        login_handler = fake_handler(
            data_storage,
            body=json.dumps({
                "username": "Tester_One",
                "password": "secret123",
            }).encode("utf-8"),
        )

        self.assertTrue(util.auth.HandleLogin(login_handler))
        self.assertEqual(login_handler.status_code, 200)

        login_token = self.get_cookie_value(
            login_handler.response_headers,
            util.auth.AUTH_COOKIE_NAME,
        )
        self.assertIsNotNone(login_token)
        assert login_token is not None

        current_user_handler = fake_handler(
            data_storage,
            cookie_header=f"{util.auth.AUTH_COOKIE_NAME}={login_token}",
        )
        self.assertTrue(util.auth.HandleAuthenticatedUserEndpoint(current_user_handler))
        self.assertEqual(current_user_handler.status_code, 200)
        self.assertEqual(current_user_handler.json_body["name"], "Tester_One")

    def test_legacy_password_migrates_to_argon2(self) -> None:
        data_storage = self.make_storage()
        user_id = data_storage.user.update(
            username="legacy_user",
            password=hashlib.sha512("old-secret".encode("utf-8")).hexdigest(),
        )
        user = data_storage.user.check_object(user_id)
        self.assertIsNotNone(user)
        assert user is not None

        self.assertTrue(util.auth.VerifyPassword(data_storage, user, "old-secret"))

        updated_user = data_storage.user.check_object(user_id)
        self.assertIsNotNone(updated_user)
        assert updated_user is not None
        self.assertTrue(updated_user.password.startswith("$argon2"))

    def test_expired_token_is_rejected_and_deleted(self) -> None:
        data_storage = self.make_storage()
        user = util.auth.CreateUser(
            data_storage,
            "expired_user",
            "secret123",
        )
        self.assertIsNotNone(user)
        assert user is not None

        token = util.auth.CreateToken(
            data_storage,
            user.id,
            "127.0.0.1",
            expireIn=-1,
        )
        self.assertFalse(util.auth.ValidateToken(data_storage, token))
        self.assertIsNone(data_storage.auth_session.check_object(token))

    def test_auth_ticket_negotiate_and_logout_flow(self) -> None:
        data_storage = self.make_storage()
        user = util.auth.CreateUser(
            data_storage,
            "ticket_user",
            "secret123",
        )
        self.assertIsNotNone(user)
        assert user is not None

        session_token = util.auth.CreateToken(
            data_storage,
            user.id,
            "127.0.0.1",
        )
        new_ticket_handler = fake_handler(
            data_storage,
            cookie_header=f"{util.auth.AUTH_COOKIE_NAME}={session_token}",
        )
        self.assertTrue(util.auth.HandleLoginNewAuthTicket(new_ticket_handler))
        self.assertEqual(new_ticket_handler.status_code, 200)
        self.assertIsNotNone(new_ticket_handler.data_body)
        assert new_ticket_handler.data_body is not None
        auth_ticket = new_ticket_handler.data_body.decode("utf-8")

        negotiate_handler = fake_handler(
            data_storage,
            query={"suggest": auth_ticket},
        )
        self.assertTrue(util.auth.HandleLoginNegotiate(negotiate_handler))
        self.assertEqual(negotiate_handler.status_code, 200)
        negotiated_token = self.get_cookie_value(
            negotiate_handler.response_headers,
            util.auth.AUTH_COOKIE_NAME,
        )
        self.assertIsNotNone(negotiated_token)
        assert negotiated_token is not None
        self.assertTrue(util.auth.ValidateToken(data_storage, negotiated_token))

        logout_handler = fake_handler(
            data_storage,
            cookie_header=f"{util.auth.AUTH_COOKIE_NAME}={negotiated_token}",
        )
        self.assertTrue(util.auth.HandleLogoutApi(logout_handler))
        self.assertEqual(logout_handler.status_code, 200)
        self.assertFalse(util.auth.ValidateToken(data_storage, negotiated_token))

    def test_password_status_returns_valid(self) -> None:
        data_storage = self.make_storage()
        handler = fake_handler(data_storage)
        self.assertTrue(util.auth.HandlePasswordsCurrentStatus(handler))
        self.assertEqual(handler.status_code, 200)
        self.assertEqual(handler.json_body, {"valid": True})

    def test_v1_users_id_returns_expected_shape(self) -> None:
        data_storage = self.make_storage()
        user = util.auth.CreateUser(
            data_storage,
            "profile_user",
            "secret123",
        )
        self.assertIsNotNone(user)
        assert user is not None

        handler = fake_handler(data_storage)
        self.assertTrue(users_api.send_user_details_v1(handler, user.id))
        self.assertEqual(handler.status_code, 200)
        self.assertEqual(handler.json_body["id"], user.id)
        self.assertEqual(handler.json_body["name"], "profile_user")
        self.assertEqual(handler.json_body["displayName"], "profile_user")
        self.assertEqual(handler.json_body["externalAppDisplayName"], "profile_user")
        self.assertFalse(handler.json_body["hasVerifiedBadge"])
        self.assertFalse(handler.json_body["isBanned"])
        self.assertIn("created", handler.json_body)
        self.assertIn("description", handler.json_body)

    def test_v1_users_id_returns_404_for_missing_user(self) -> None:
        data_storage = self.make_storage()
        handler = fake_handler(data_storage)
        self.assertTrue(users_api.send_user_details_v1(handler, 999999))
        self.assertEqual(handler.status_code, 404)
        self.assertEqual(
            handler.json_body,
            {"errors": [{"code": 3, "message": "The user id is invalid."}]},
        )

    def test_v1_users_currency_returns_balance_for_authenticated_user(self) -> None:
        data_storage = self.make_storage()
        user = util.auth.CreateUser(
            data_storage,
            "currency_user",
            "secret123",
        )
        self.assertIsNotNone(user)
        assert user is not None

        data_storage.funds.set(user.id, 125)
        token = util.auth.CreateToken(
            data_storage,
            user.id,
            "127.0.0.1",
        )
        handler = fake_handler(
            data_storage,
            cookie_header=f"{util.auth.AUTH_COOKIE_NAME}={token}",
        )
        self.assertTrue(funds_api.send_user_currency_v1(handler, user.id))
        self.assertEqual(handler.status_code, 200)
        self.assertEqual(
            handler.json_body,
            {
                "robux": 125,
                "tickets": 0,
            },
        )

    def test_v1_users_currency_rejects_other_user(self) -> None:
        data_storage = self.make_storage()
        user = util.auth.CreateUser(
            data_storage,
            "currency_owner",
            "secret123",
        )
        other_user = util.auth.CreateUser(
            data_storage,
            "currency_other",
            "secret123",
        )
        self.assertIsNotNone(user)
        self.assertIsNotNone(other_user)
        assert user is not None

        token = util.auth.CreateToken(
            data_storage,
            user.id,
            "127.0.0.1",
        )
        handler = fake_handler(
            data_storage,
            cookie_header=f"{util.auth.AUTH_COOKIE_NAME}={token}",
        )
        self.assertTrue(funds_api.send_user_currency_v1(handler, user.id + 1))
        self.assertEqual(handler.status_code, 401)
        self.assertEqual(
            handler.json_body,
            {
                "success": False,
                "message": "Unauthorized",
            },
        )

    def test_v1_users_badges_returns_paginated_badge_details(self) -> None:
        data_storage = self.make_storage()
        user = util.auth.CreateUser(
            data_storage,
            "badge_owner",
            "secret123",
        )
        other_user = util.auth.CreateUser(
            data_storage,
            "badge_other",
            "secret123",
        )
        self.assertIsNotNone(user)
        self.assertIsNotNone(other_user)
        assert user is not None
        assert other_user is not None

        badge_config = self.make_game_config({
            101: SimpleNamespace(name="Explorer", icon=None),
            202: SimpleNamespace(name="Winner", icon=None),
        })
        data_storage.badges.award(user.id, 101)
        data_storage.badges.award(user.id, 202)
        data_storage.badges.award(other_user.id, 202)

        handler = fake_handler(
            data_storage,
            query={
                "limit": "1",
                "sortOrder": "Desc",
            },
            game_config=badge_config,
        )
        self.assertTrue(badges_api.send_user_badges_v1(handler, user.id))
        self.assertEqual(handler.status_code, 200)
        self.assertEqual(handler.json_body["previousPageCursor"], None)
        self.assertEqual(handler.json_body["nextPageCursor"], "1")
        self.assertEqual(len(handler.json_body["data"]), 1)
        self.assertEqual(handler.json_body["data"][0]["id"], 202)
        self.assertEqual(handler.json_body["data"][0]["name"], "Winner")
        self.assertEqual(handler.json_body["data"][0]["displayName"], "Winner")
        self.assertEqual(handler.json_body["data"][0]["statistics"]["awardedCount"], 2)
        self.assertEqual(handler.json_body["data"][0]["statistics"]["pastDayAwardedCount"], 2)
        self.assertEqual(handler.json_body["data"][0]["awardingUniverse"]["name"], "Test Universe")

    def test_join_response_uses_authenticated_user_instead_of_query_usercode(self) -> None:
        data_storage = self.make_storage()
        user = util.auth.CreateUser(
            data_storage,
            "join_cookie_user",
            "secret123",
        )
        self.assertIsNotNone(user)
        assert user is not None

        token = util.auth.CreateToken(
            data_storage,
            user.id,
            "127.0.0.1",
        )
        game_config = self.make_game_config(data_storage=data_storage)
        handler = fake_handler(
            data_storage,
            cookie_header=f"{util.auth.AUTH_COOKIE_NAME}={token}",
            query={"UserCode": "LegacyQueryValue"},
            game_config=game_config,
        )

        join_data.perform_and_send_join(handler, {}, prefix=b"")
        self.assertEqual(handler.status_code, 200)
        self.assertEqual(handler.json_body["UserId"], user.id)
        self.assertEqual(handler.json_body["UserName"], "join_cookie_user")
        self.assertEqual(handler.json_body["DisplayName"], "join_cookie_user")
        self.assertEqual(handler.json_body["UserCode"], "join_cookie_user")
        self.assertEqual(
            data_storage.players.check("join_cookie_user"),
            (user.id, "join_cookie_user"),
        )

    def test_place_launcher_ticket_authenticates_without_cookie(self) -> None:
        data_storage = self.make_storage()
        user = util.auth.CreateUser(
            data_storage,
            "launcher_ticket_user",
            "secret123",
        )
        self.assertIsNotNone(user)
        assert user is not None

        ticket = util.auth.CreateAuthTicket(
            data_storage,
            user.id,
        )
        handler = fake_handler(
            data_storage,
            query={
                "placeId": "1818",
                "UserCode": "LegacyQueryValue",
                "t": ticket,
            },
            game_config=self.make_game_config(data_storage=data_storage),
        )

        resolved_user = join_data.get_place_launcher_user(handler)
        self.assertIsNotNone(resolved_user)
        assert resolved_user is not None
        self.assertEqual(resolved_user.id, user.id)
        launcher_url = join_data.build_place_launcher_url(
            handler,
            "another-ticket",
        )
        self.assertIn("/Game/PlaceLauncher.ashx?request=RequestGameJob", launcher_url)
        self.assertIn("placeId=1818", launcher_url)
        self.assertIn("gameId=", launcher_url)
        self.assertIn("isPartyLeader=false", launcher_url)
        self.assertIn("isTeleport=true", launcher_url)
        self.assertIn("t=another-ticket", launcher_url)

    def test_place_launcher_ticket_can_be_reused_by_join_after_place_launcher(self) -> None:
        data_storage = self.make_storage()
        user = util.auth.CreateUser(
            data_storage,
            "ticket_reuse_user",
            "secret123",
        )
        self.assertIsNotNone(user)
        assert user is not None

        ticket = util.auth.CreateAuthTicket(
            data_storage,
            user.id,
        )
        place_launcher_handler = fake_handler(
            data_storage,
            query={
                "placeId": "1818",
                "t": ticket,
            },
            game_config=self.make_game_config(data_storage=data_storage),
        )
        join_handler = fake_handler(
            data_storage,
            query={
                "placeId": "1818",
                "MachineAddress": "127.0.0.1",
                "ServerPort": "2005",
                "t": ticket,
            },
            game_config=self.make_game_config(data_storage=data_storage),
        )

        place_launcher_user = join_data.get_place_launcher_user(
            place_launcher_handler,
            consume_ticket=False,
        )
        self.assertIsNotNone(place_launcher_user)
        join_data.perform_and_send_join(join_handler, {}, prefix=b"")
        self.assertEqual(join_handler.status_code, 200)
        self.assertEqual(join_handler.json_body["UserId"], user.id)

    def test_place_launcher_falls_back_to_legacy_usercode_without_cookie(self) -> None:
        data_storage = self.make_storage()
        user = util.auth.CreateUser(
            data_storage,
            "legacy_launcher_user",
            "secret123",
        )
        self.assertIsNotNone(user)
        assert user is not None

        handler = fake_handler(
            data_storage,
            query={
                "placeId": "1818",
                "UserCode": "legacy_launcher_user",
            },
            game_config=self.make_game_config(data_storage=data_storage),
        )

        resolved_user = join_data.get_place_launcher_user(handler)
        self.assertIsNotNone(resolved_user)
        assert resolved_user is not None
        self.assertEqual(resolved_user.id, user.id)

    def test_join_response_supports_legacy_player_mapping_without_user_row(self) -> None:
        data_storage = self.make_storage()
        data_storage.players.add_player(
            "мирон крутой",
            5636584,
            "мирон крутой",
        )
        handler = fake_handler(
            data_storage,
            query={
                "MachineAddress": "127.0.0.1",
                "ServerPort": "2005",
                "UserCode": "мирон крутой",
            },
            game_config=self.make_game_config(data_storage=data_storage),
        )

        join_data.perform_and_send_join(handler, {}, prefix=b"")
        self.assertEqual(handler.status_code, 200)
        self.assertEqual(handler.json_body["UserId"], 5636584)
        self.assertEqual(handler.json_body["UserName"], "мирон крутой")
        self.assertEqual(handler.json_body["UserCode"], "мирон крутой")

    def test_get_join_script_returns_player_protocol_prefix_and_ticketed_place_launcher(self) -> None:
        data_storage = self.make_storage()
        user = util.auth.CreateUser(
            data_storage,
            "website_join_user",
            "secret123",
        )
        self.assertIsNotNone(user)
        assert user is not None

        token = util.auth.CreateToken(
            data_storage,
            user.id,
            "127.0.0.1",
        )
        handler = fake_handler(
            data_storage,
            cookie_header=f"{util.auth.AUTH_COOKIE_NAME}={token}",
            query={"placeId": "1818"},
            game_config=self.make_game_config(data_storage=data_storage),
        )

        self.assertTrue(join_data.send_get_join_script(handler))
        self.assertEqual(handler.status_code, 200)
        self.assertTrue(handler.json_body["prefix"].startswith("rfd-player:1+launchmode:play+clientversion:0.463.0pcplayer+gameinfo:"))
        self.assertIn(f"+gameinfo:{token}+", handler.json_body["prefix"])
        self.assertIn("+placelauncherurl:https://localhost:2005/Game/PlaceLauncher.ashx?", handler.json_body["prefix"])
        self.assertTrue(handler.json_body["prefix"].endswith("+k:l+client"))
        self.assertEqual(handler.json_body["joinUrl"], handler.json_body["prefix"])
        self.assertIn("/Game/PlaceLauncher.ashx?request=RequestGameJob", handler.json_body["joinScriptUrl"])
        self.assertIn("placeId=1818", handler.json_body["joinScriptUrl"])
        self.assertIn("gameId=", handler.json_body["joinScriptUrl"])
        self.assertIn("isPartyLeader=false", handler.json_body["joinScriptUrl"])
        self.assertIn("isTeleport=true", handler.json_body["joinScriptUrl"])
        self.assertIn("t=", handler.json_body["joinScriptUrl"])

    def test_get_join_script_accepts_roblosecurity_header(self) -> None:
        data_storage = self.make_storage()
        user = util.auth.CreateUser(
            data_storage,
            "header_join_user",
            "secret123",
        )
        self.assertIsNotNone(user)
        assert user is not None

        token = util.auth.CreateToken(
            data_storage,
            user.id,
            "127.0.0.1",
        )
        handler = fake_handler(
            data_storage,
            query={"placeId": "1818"},
            game_config=self.make_game_config(data_storage=data_storage),
        )
        handler.headers["X-Roblosecurity"] = token

        self.assertTrue(join_data.send_get_join_script(handler))
        self.assertEqual(handler.status_code, 200)
        self.assertIn("&t=", handler.json_body["joinScriptUrl"])

    def test_player_cookie_store_sync_roundtrip(self) -> None:
        temp_dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, temp_dir, True)
        cookie_path = os.path.join(temp_dir, "RobloxCookies.dat")

        util.player_cookie_store.sync_auth_cookie(
            {"localhost", "127.0.0.1"},
            "local-auth-token",
            path=util.player_cookie_store.Path(cookie_path),
        )

        entries = util.player_cookie_store.read_cookie_entries(
            util.player_cookie_store.Path(cookie_path),
        )
        matching = {
            entry.domain: entry.value
            for entry in entries
            if entry.name == ".ROBLOSECURITY"
        }
        self.assertEqual(matching["localhost"], "local-auth-token")
        self.assertEqual(matching["127.0.0.1"], "local-auth-token")

    def test_player_cookie_store_ignores_invalid_store(self) -> None:
        temp_dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, temp_dir, True)
        cookie_path = util.player_cookie_store.Path(
            os.path.join(temp_dir, "RobloxCookies.dat")
        )

        with open(cookie_path, "w", encoding="utf-8") as file:
            file.write("{not-json")

        self.assertEqual(
            util.player_cookie_store.read_cookie_entries(cookie_path),
            [],
        )
        self.assertIsNone(
            util.player_cookie_store.get_cookie_value(path=cookie_path),
        )

    def test_player_cookie_store_prefers_localhost_cookie_for_launcher(self) -> None:
        temp_dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, temp_dir, True)
        cookie_path = util.player_cookie_store.Path(
            os.path.join(temp_dir, "RobloxCookies.dat")
        )

        util.player_cookie_store.write_cookie_entries([
            util.player_cookie_store.cookie_entry(
                domain=".roblox.com",
                include_subdomains=True,
                path="/",
                secure=True,
                expiry="0",
                name=".ROBLOSECURITY",
                value="_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_real",
            ),
            util.player_cookie_store.cookie_entry(
                domain="localhost",
                include_subdomains=False,
                path="/",
                secure=True,
                expiry="0",
                name=".ROBLOSECURITY",
                value="local-session-token",
            ),
        ], cookie_path)

        self.assertEqual(
            util.player_cookie_store.get_cookie_value(
                preferred_hosts={"localhost", "127.0.0.1"},
                path=cookie_path,
            ),
            "local-session-token",
        )

    def test_player_launcher_prefers_authenticated_join_script(self) -> None:
        launcher = player_routine.obj_type(
            rcc_host='127.0.0.1',
            web_host='127.0.0.1',
            rcc_port=2005,
            web_port=2005,
            user_code='legacy_user_code',
            logger=logger.PRINT_QUIET,
        )
        fake_response = mock.MagicMock()
        fake_response.__enter__.return_value = fake_response
        fake_response.read.return_value = (
            b'{"joinScriptUrl":"https://localhost:2005/game/PlaceLauncher.ashx?placeId=1818&t=abc",'
            b'"authenticationUrl":"https://localhost:2005/login/negotiate.ashx"}'
        )

        captured: dict[str, tuple[str, ...]] = {}
        launcher.get_versioned_path = lambda *_args: 'RobloxPlayerBeta.exe'
        launcher.init_popen = lambda _exe, args: captured.setdefault("args", args)

        with (
            mock.patch(
                'util.player_cookie_store.get_cookie_value',
                return_value='local-session-token',
            ),
            mock.patch(
                'urllib.request.urlopen',
                return_value=fake_response,
            ),
        ):
            launcher.make_client_popen()

        join_argument = captured["args"][3]
        self.assertIn('/game/PlaceLauncher.ashx?', join_argument)
        self.assertIn('&t=abc', join_argument)
        self.assertNotIn('UserCode=', join_argument)

    def test_player_launcher_opens_client_auth_error_flow_without_cookie(self) -> None:
        launcher = player_routine.obj_type(
            rcc_host='127.0.0.1',
            web_host='127.0.0.1',
            rcc_port=2006,
            web_port=2005,
            user_code='legacy_user_code',
            logger=logger.PRINT_QUIET,
        )

        captured: dict[str, tuple[str, ...]] = {}
        launcher.get_versioned_path = lambda *_args: 'RobloxPlayerBeta.exe'
        launcher.init_popen = lambda _exe, args: captured.setdefault("args", args)

        with mock.patch(
            'util.player_cookie_store.get_cookie_value',
            return_value=None,
        ):
            launcher.make_client_popen()

        join_argument = captured["args"][3]
        self.assertIn('/game/PlaceLauncher.ashx?', join_argument)
        self.assertIn('ServerPort=2006', join_argument)
        self.assertNotIn('UserCode=', join_argument)

    def test_player_launcher_opens_client_auth_error_flow_when_cookie_join_fails(self) -> None:
        launcher = player_routine.obj_type(
            rcc_host='127.0.0.1',
            web_host='127.0.0.1',
            rcc_port=2006,
            web_port=2005,
            user_code='legacy_user_code',
            logger=logger.PRINT_QUIET,
        )

        captured: dict[str, tuple[str, ...]] = {}
        launcher.get_versioned_path = lambda *_args: 'RobloxPlayerBeta.exe'
        launcher.init_popen = lambda _exe, args: captured.setdefault("args", args)

        request = urllib.request.Request(
            "https://localhost:2005/game/get-join-script",
        )
        http_error = urllib.error.HTTPError(
            request.full_url,
            401,
            "Unauthorized",
            hdrs=None,
            fp=None,
        )

        with (
            mock.patch(
                'util.player_cookie_store.get_cookie_value',
                return_value='local-session-token',
            ),
            mock.patch(
                'urllib.request.urlopen',
                side_effect=http_error,
            ),
        ):
            launcher.make_client_popen()

        join_argument = captured["args"][3]
        self.assertIn('/game/PlaceLauncher.ashx?', join_argument)
        self.assertIn('ServerPort=2006', join_argument)
        self.assertNotIn('UserCode=', join_argument)

    def test_get_account_age_days_accepts_aware_created_timestamp(self) -> None:
        handler = fake_handler(
            self.make_storage(),
            game_config=self.make_game_config(),
        )
        created = (datetime.now(UTC) - timedelta(days=5)).isoformat()
        user = SimpleNamespace(
            id=1,
            username="aware_user",
            created=created,
        )

        account_age = join_data.get_account_age_days(handler, user)
        self.assertGreaterEqual(account_age, 5)

    def test_get_account_age_days_accepts_naive_created_timestamp(self) -> None:
        handler = fake_handler(
            self.make_storage(),
            game_config=self.make_game_config(),
        )
        created = (
            datetime.now(UTC).replace(tzinfo=None) - timedelta(days=3)
        ).isoformat()
        user = SimpleNamespace(
            id=1,
            username="naive_user",
            created=created,
        )

        account_age = join_data.get_account_age_days(handler, user)
        self.assertGreaterEqual(account_age, 3)