import hashlib
import json
import os
import shutil
import tempfile
import unittest
from http.cookies import SimpleCookie

import storage
import util.auth
import web_server.endpoints.users_api as users_api


class fake_server:
    def __init__(self, data_storage: storage.storager) -> None:
        self.storage = data_storage


class fake_handler:
    def __init__(
        self,
        data_storage: storage.storager,
        *,
        body: bytes = b"",
        cookie_header: str | None = None,
        query: dict[str, str] | None = None,
    ) -> None:
        self.server = fake_server(data_storage)
        self._body = body
        self.headers: dict[str, str] = {}
        if cookie_header is not None:
            self.headers["Cookie"] = cookie_header
        self.client_address = ("127.0.0.1", 12345)
        self.query = query or {}
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
        assert prefix in {b"",}
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
