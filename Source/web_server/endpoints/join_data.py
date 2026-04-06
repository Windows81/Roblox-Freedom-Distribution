# Standard library imports
import dataclasses
from datetime import UTC, datetime, timedelta
import json
import random
import uuid
import base64
import urllib.parse

# Typing imports
from typing import Any

# Local application imports
import util.auth
import util.const
import game_config
import util.versions as versions
from util.signscript import signUTF8
from web_server._logic import web_server_handler, server_path


@dataclasses.dataclass
class join_user_item:
    id: int
    username: str
    created: str
    accountstatus: int
    user_code: str


def utcnow() -> datetime:
    return datetime.now(UTC)


def make_join_user(
    current_user,
    *,
    user_code: str | None = None,
) -> join_user_item:
    return join_user_item(
        id=current_user.id,
        username=current_user.username,
        created=str(current_user.created),
        accountstatus=current_user.accountstatus,
        user_code=user_code or current_user.username,
    )


def is_join_user_allowed(
    self: web_server_handler,
    user_code: str,
    username: str,
) -> bool:
    return self.game_config.server_core.check_user_allowed.cached_call(
        7,
        user_code,
        username,
    )


def build_legacy_join_user(
    self: web_server_handler,
    user_code: str,
    user_id: int,
    username: str,
):
    if not is_join_user_allowed(self, user_code, username):
        return None

    current_user = self.server.storage.user.check_object(user_id)
    if current_user is not None:
        if current_user.accountstatus != 1:
            return None
        return make_join_user(
            current_user,
            user_code=user_code,
        )

    account_age = max(
        int(self.game_config.server_core.retrieve_account_age(
            user_id,
            username,
        )),
        0,
    )
    created_at = utcnow() - timedelta(days=account_age)
    return join_user_item(
        id=user_id,
        username=username,
        created=created_at.isoformat(),
        accountstatus=1,
        user_code=user_code,
    )


def get_authenticated_join_user(self: web_server_handler):
    current_user = util.auth.GetCurrentUser(self)
    if current_user is None or current_user.accountstatus != 1:
        return None

    if not is_join_user_allowed(
        self,
        current_user.username,
        current_user.username,
    ):
        return None
    return make_join_user(current_user)


def get_legacy_query_user(self: web_server_handler):
    user_code = (
        self.query.get('UserCode') or
        self.query.get('user-code') or
        ""
    ).strip()
    if not user_code:
        return None

    existing_player = self.server.storage.players.check(user_code)
    if existing_player is not None:
        return build_legacy_join_user(
            self,
            user_code,
            existing_player[0],
            existing_player[1],
        )

    current_user = self.server.storage.user.check_object_from_username(user_code)
    if current_user is not None and current_user.accountstatus == 1:
        if not is_join_user_allowed(
            self,
            user_code,
            current_user.username,
        ):
            return None
        return make_join_user(
            current_user,
            user_code=user_code,
        )

    try:
        user_id = int(self.game_config.server_core.retrieve_user_id(user_code))
        username = str(self.game_config.server_core.retrieve_username(
            user_id,
            user_code,
        ))
    except Exception:
        return None
    return build_legacy_join_user(
        self,
        user_code,
        user_id,
        username,
    )


def get_place_launcher_user(
    self: web_server_handler,
    *,
    consume_ticket: bool = True,
):
    place_launcher_ticket = self.query.get('t', '')
    if place_launcher_ticket:
        ticket_info = util.auth.GetTemporaryTicketInfo(
            self.server.storage,
            place_launcher_ticket,
            util.auth.AUTH_TICKET_KIND_LOGIN,
        )
        if ticket_info is None:
            return None
        if consume_ticket:
            self.server.storage.auth_ticket.delete(place_launcher_ticket)
        current_user = self.server.storage.user.check_object(ticket_info.user_id)
        if current_user is None or current_user.accountstatus != 1:
            return None
        return make_join_user(current_user)

    current_user = get_authenticated_join_user(self)
    if current_user is not None:
        return current_user

    return get_legacy_query_user(self)


def build_place_launcher_url(
    self: web_server_handler,
    place_launcher_ticket: str | None = None,
    *,
    game_id: str | None = None,
) -> str:
    query = {
        'request': 'RequestGameJob',
        'placeId': str(self.query.get('placeId', util.const.PLACE_IDEN_CONST)),
        'gameId': game_id or str(
            self.query.get('gameId') or
            self.query.get('jobId') or
            uuid.uuid4()
        ),
        'isPartyLeader': 'false',
        'gender': '',
        'isTeleport': 'true',
    }

    for key in (
        'MachineAddress',
        'ServerPort',
        'browserTrackerId',
        'BrowserTrackerId',
    ):
        value = self.query.get(key)
        if value:
            query[key] = str(value)

    if place_launcher_ticket:
        query['t'] = place_launcher_ticket
    return (
        f'{self.hostname}/Game/PlaceLauncher.ashx?' +
        urllib.parse.urlencode(query)
    )


def build_player_launch_prefix(
    game_info: str,
    place_launcher_url: str,
    client_version: str,
) -> str:
    # Official Roblox
    # roblox-player:1+launchmode:play+
    # gameinfo:LoNO0wfhsdjnpx2OGIFo5evyMcf1ahE-tEf...
    # +launchtime:1774792078961+
    # placelauncherurl:https%3A%2F%2Fwww.roblox.com%2FGame%2FPlaceLauncher.ashx%3Frequest%3DRequestGame%26browserTrackerId%3D1766145293603501%26placeId%3D192800%26isPlayTogetherGame%3Dfalse%26referredByPlayerId%3D0%26joinAttemptId%3Dbc3458fe-2452-4d4b-9969-04787766e31b%26joinAttemptOrigin%3DPlayButton+browsertrackerid:1766145293603501+robloxLocale:en_us+gameLocale:en_us+channel:+LaunchExp:InApp

    return (
        "rfd-player:1+launchmode:play+" +
        f"clientversion:{client_version}+" +
        f"gameinfo:{game_info}+" +
        f"placelauncherurl:{place_launcher_url}+" +
        "k:l+client"
    )


def get_player_client_version(
    self: web_server_handler,
) -> str:
    version = self.game_config.game_setup.roblox_version
    raw_version = version.value[2]
    if raw_version.startswith('v'):
        raw_version = raw_version[1:]
    return f'0.{raw_version}.0pcplayer'


def gen_player(config: game_config.obj_type, authenticated_user) -> tuple[int, str, bool] | None:
    '''
    Returns a tuple with the following:
    `int`: corresponds with the iden number of a user whose `index` field matches `value`.
    `str`: corresponds with the username of a user whose `index` field matches `value`.
    `bool`: returns `True` if the player is being created for the first time.
    '''
    database = config.storage.players
    username = authenticated_user.username
    user_code = getattr(authenticated_user, 'user_code', username)
    existing = database.check(user_code)
    if existing is not None:
        return (*existing, False)

    result = database.add_player(
        user_code,
        authenticated_user.id,
        username,
    )
    if result is None:
        existing_username = database.get_player_field_from_index(
            index=database.player_field.IDEN_NUM,
            value=authenticated_user.id,
            field=database.player_field.USERNAME,
        )
        if existing_username is None:
            return None
        return (authenticated_user.id, str(existing_username), False)
    return (*result, True)


def init_player(config: game_config.obj_type, authenticated_user) -> tuple[int, str] | None:
    '''
    Returns a tuple with the following:
    `int`: corresponds with that user's `id_num`.
    `str`: corresponds with that user's `username`.
    '''
    player_data = gen_player(config, authenticated_user)
    if player_data is None:
        return None
    (iden_num, username, first_time) = player_data

    if first_time and config.storage.funds.check(iden_num) is None:
        funds = config.server_core.retrieve_default_funds(
            iden_num,
            authenticated_user.username,
        )
        config.storage.funds.first_init(iden_num, funds)

    return (iden_num, username)


def get_account_age_days(
    self: web_server_handler,
    authenticated_user,
) -> int:
    created = getattr(authenticated_user, 'created', None)
    if not isinstance(created, str) or not created:
        return max(
            int(self.game_config.server_core.retrieve_account_age(
                authenticated_user.id,
                authenticated_user.username,
            )),
            0,
        )

    for parser in (
        datetime.fromisoformat,
        lambda value: datetime.strptime(value, "%Y-%m-%d %H:%M:%S"),
    ):
        try:
            created_at = parser(created)
            break
        except ValueError:
            continue
    else:
        return max(
            int(self.game_config.server_core.retrieve_account_age(
                authenticated_user.id,
                authenticated_user.username,
            )),
            0,
        )

    if created_at.tzinfo is None:
        created_at = created_at.replace(tzinfo=UTC)
    else:
        created_at = created_at.astimezone(UTC)

    now = utcnow()
    return max((now - created_at).days, 0)


def generate_client_ticket(self: web_server_handler, user_id: int, username: str, job_id: str, character_url: str = None, custom_timestamp: str = "", ticket_version: int = 1, place_id: int = 1, account_age: int | None = None) -> str:
    """
        Generates a client ticket so that RCC can verify the user is authenticated
        If character_url is not None, it will be used as the character URL instead of the default
        If custom_timestamp is not 0, it will be used as the timestamp instead of the current time
    """
    config = self.game_config
    server_core = config.server_core

    if custom_timestamp == "":
        custom_timestamp = utcnow().strftime("%m/%d/%Y %I:%M:%S %p")
    if character_url is None:
        if ticket_version == 2:
            character_url = str(user_id)
        elif ticket_version == 1:
            character_url = f"{self.hostname}/Asset/CharacterFetch.ashx?userId={user_id}"
        elif ticket_version == 4:
            character_url = f"{self.hostname}/v1.1/avatar-fetch?userId={str(user_id)}&placeId={str(place_id)}"

    first_ticket_unsigned = f"{str(user_id)}\n{username}\n{character_url}\n{job_id}\n{str(custom_timestamp)}"
    signed_first_ticket_raw: bytes = signUTF8(first_ticket_unsigned, formatAutomatically=False, addNewLine=False,
                                              useNewKey=(ticket_version > 1))
    signed_first_ticket = base64.b64encode(signed_first_ticket_raw).decode("utf-8")

    if account_age is None:
        account_age = server_core.retrieve_account_age(user_id, username)
    user_membership_type = "None"

    if ticket_version <= 3:
        second_ticket_unsigned = f"{str(user_id)}\n{str(job_id)}\n{str(custom_timestamp)}"
    elif ticket_version == 4:
        second_ticket_unsigned = f"{custom_timestamp}\n{job_id}\n{user_id}\n{user_id}\n0\n{account_age}\nf\n{len(username)}\n{username}\n{len(user_membership_type)}\n{user_membership_type}\n0\n\n0\n\n{len(username)}\n{username}"

    signed_second_ticket_raw: bytes = signUTF8(second_ticket_unsigned, formatAutomatically=False, addNewLine=False,
                                               useNewKey=(ticket_version > 1))
    signed_second_ticket = base64.b64encode(signed_second_ticket_raw).decode("utf-8")

    return f"{str(custom_timestamp)};{signed_first_ticket};{signed_second_ticket}{f';{ticket_version}' if ticket_version > 1 else ''}"


def perform_and_send_join(self: web_server_handler, additional_return_data: dict[str, Any], prefix: bytes) -> None:
    '''
    The query arguments in `Roblox-Session-Id` were previously serialized.
    For example, when `join.ashx` was called the first time a player joined.

    Some methods (such as retrieving a user fund balance, or rejoining in 2021E) need data from `Roblox-Session-Id`.
    '''
    config = self.game_config
    server_core = config.server_core

    query_args: dict[str, str] = json.loads(
        self.headers.get('Roblox-Session-Id', '{}'),
    ) | self.query

    rcc_host_addr = str(query_args.get('MachineAddress', self.hostname))
    rcc_port = int(query_args.get('ServerPort', self.port_num))
    current_user = get_place_launcher_user(self)
    if current_user is None:
        self.send_json({"error": "403: disallowed user"}, 403)
        return

    result = init_player(self.game_config, current_user)
    if result is None:
        self.send_json({"error": "403: disallowed user"}, 403)
        return

    (id_num, username) = result
    account_age = get_account_age_days(self, current_user)
    user_code = getattr(current_user, 'user_code', username)

    join_data = {
        'ServerConnections': [
            {
                'Address': rcc_host_addr,
                'Port': rcc_port,
            }
        ],
        'UserCode':
            user_code,
        'UserId':
            id_num,
        'MachineAddress':
            rcc_host_addr,
        'ServerPort':
            rcc_port,
        'BaseUrl':
            self.hostname,
        'PlaceId':
            util.const.PLACE_IDEN_CONST,
        'UserName':
            username,
        'DisplayName':
            username,
        'AccountAge':
            account_age,
        'ChatStyle':
            server_core.chat_style.value,
        'characterAppearanceId':
            id_num,
        'CharacterAppearanceId':
            id_num,
        'CharacterAppearance':
            f'{self.hostname}/v1.1/avatar-fetch?userId={id_num}',
    }

    # NOTE: the `SessionId` is saved as an HTTPS header `Roblox-Session-Id` for later requests.
    # I'm placing the information which was passed into `join.ashx` here for simplicity.
    join_data |= {
        'SessionId': json.dumps(join_data | {'RFDJoinQuery': query_args})
    }
    self.send_response(200)
    self.send_json(join_data | additional_return_data, prefix=prefix)


@server_path('/game/join.ashx', versions={versions.rōblox.v347, versions.rōblox.v271})
def _(self: web_server_handler) -> bool:
    perform_and_send_join(self, {
        'ClientPort': 0,
        'PingUrl': '',
        'PingInterval': 0,
        'SeleniumTestMode': False,
        'SuperSafeChat': False,
        'MeasurementUrl': '',
        'WaitingForCharacterGuid': '',
        'VendorId': 0,
        'ScreenShotInfo': '',
        'VideoInfo': '',
        'CreatorId': 0,
        'CreatorTypeEnum': 'User',
        'MembershipType': 'None',
        'CookieStoreFirstTimePlayKey': 'rbx_evt_ftp',
        'CookieStoreFiveMinutePlayKey': 'rbx_evt_fmp',
        'CookieStoreEnabled': False,
        'IsRobloxPlace': True,
        'GenerateTeleportJoin': False,
        'IsUnknownOrUnder13': False,
        'DataCenterId': 0,
        'FollowUserId': 0,
        'UniverseId': 0,
    }, prefix=b'--rbxsig%0%\r\n')
    return True


@server_path('/game/join.ashx', versions={versions.rōblox.v463})
def _(self: web_server_handler) -> bool:
    perform_and_send_join(self, {
        'ClientPort': 0,
        'PingUrl': '',
        'PingInterval': 0,
        'DirectServerReturn': True,
        'SeleniumTestMode': False,
        'RobloxLocale': 'en_us',
        'GameLocale': 'en_us#RobloxTranslateAbTest2',
        'SuperSafeChat': True,
        'ClientTicket': '2022-03-26T05:13:05.7649319Z;dj09X5iTmYtOPwh0hbEC8yvSO1t99oB3Yh5qD/sinDFszq3hPPaL6hH16TvtCen6cABIycyDv3tghW7k8W+xuqW0/xWvs0XJeiIWstmChYnORzM1yCAVnAh3puyxgaiIbg41WJSMALRSh1hoRiVFOXw4BKjSKk7DrTTcL9nOG1V5YwVnmAJKY7/m0yZ81xE99QL8UVdKz2ycK8l8JFvfkMvgpqLNBv0APRNykGDauEhAx283vARJFF0D9UuSV69q6htLJ1CN2kXL0Saxtt/kRdoP3p3Nhj2VgycZnGEo2NaG25vwc/KzOYEFUV0QdQPC8Vs2iFuq8oK+fXRc3v6dnQ==;BO8oP7rzmnIky5ethym6yRECd6H14ojfHP3nHxSzfTs=;XsuKZL4TBjh8STukr1AgkmDSo5LGgQKQbvymZYi/80TYPM5/MXNr5HKoF3MOT3Nfm0MrubracyAtg5O3slIKBg==;6',
        'GameId': util.const.PLACE_IDEN_CONST,
        'CreatorId': 0,
        'CreatorTypeEnum': 'User',
        'MembershipType': 'None',
        'CookieStoreFirstTimePlayKey': 'rbx_evt_ftp',
        'CookieStoreFiveMinutePlayKey': 'rbx_evt_fmp',
        'CookieStoreEnabled': True,
        'IsUnknownOrUnder13': False,
        'GameChatType': 'AllUsers',
        'AnalyticsSessionId': 'c89589f1-d1de-46e3-80e0-2703d1159409',
        'DataCenterId': 302,
        'UniverseId': 994732206,
        'FollowUserId': 0,
        'CountryCode': 'US',
        'RandomSeed1': '7HOfysTid4XsV/3mBPPPhKHIykE4GXSBBBzd93rplbDQ3bNSgPFcR9auB780LjNYg+4mbNQPOqTmJ2o3hUefmw==',
        'ClientPublicKeyData': json.dumps({
            'creationTime': '19:56 11/23/2021',
            'applications': {
                'RakNetEarlyPublicKey': {
                    'versions': [{
                        'id': 2,
                        'value': 'HwatfCnkndvyKCMPSa0VAl2M2c0GQv9+0z0kENhcj2w=',
                        'allowed': True,
                    }],
                    'send': 2,
                    'revert': 2,
                }
            }
        }),
    }, prefix=b'--rbxsig2%0%\r\n')
    return True


# FIXME: Adapt this path to mobile client (it's stuck on loading screen).
@server_path('/v1/join-game', commands={'POST'})
def _(self: web_server_handler) -> bool:
    config = self.game_config
    server_core = config.server_core

    query_args: dict[str, str] = json.loads(
        self.headers.get('Roblox-Session-Id', '{}'),
    ) | self.query

    rcc_port = int(query_args.get('ServerPort', self.port_num))
    current_user = get_authenticated_join_user(self)
    if current_user is None:
        self.send_json({"error": "403: disallowed user"}, 403)
        return True

    result = init_player(self.game_config, current_user)
    if result is None:
        self.send_json({"error": "403: disallowed user"}, 403)
        return True

    (id_num, username) = result
    account_age = get_account_age_days(self, current_user)

    jobId = str(uuid.uuid4())
    status = 2  # Assuming ready
    joinScript = {
        "ClientPort": 0,
        "MachineAddress": self.domain,
        "ServerConnections": [{"Port": rcc_port, "Address": self.domain}],
        "ServerPort": rcc_port,
        "PingUrl": "",
        "PingInterval": 120,
        "UserName": username,
        "DisplayName": username,
        "SeleniumTestMode": False,
        "UserId": id_num,
        "ClientTicket": generate_client_ticket(
            self,
            id_num,
            username,
            jobId,
            f'{self.hostname}/v1.1/avatar-fetch?userId={id_num}',
            ticket_version=4,
            place_id=1818,
            account_age=account_age,
        ),
        "SuperSafeChat": False,
        "PlaceId": 1818,
        "MeasurementUrl": "",
        "WaitingForCharacterGuid": str(uuid.uuid4()),
        "BaseUrl": self.hostname,
        "ChatStyle": server_core.chat_style.value,
        "VendorId": 0,
        "ScreenShotInfo": "",
        "VideoInfo": "",
        "CreatorId": 0,
        "CreatorTypeEnum": "User",
        "MembershipType": "None",
        "AccountAge": account_age,
        "CookieStoreFirstTimePlayKey": "rbx_evt_ftp",
        "CookieStoreFiveMinutePlayKey": "rbx_evt_fmp",
        "CookieStoreEnabled": True,
        "IsRobloxPlace": False,
        "UniverseId": 994732206,
        "GenerateTeleportJoin": False,
        "IsUnknownOrUnder13": False,
        "SessionId": f"{str(uuid.uuid4())}|{str(jobId)}|0|{str(self.domain)}|8|{utcnow().strftime('%Y-%m-%dT%H:%M:%S.000Z')}|0|null|AAAAA",
        "DataCenterId": 69420,
        "FollowUserId": 0,
        "BrowserTrackerId": 0,
        "UsePortraitMode": False,
        "CharacterAppearance": f'{self.hostname}/v1.1/avatar-fetch?userId={id_num}',
        "GameId": jobId,
        "RobloxLocale": "en_us",
        "GameLocale": "en_us",
        "characterAppearanceId": id_num,
        "CharacterAppearanceId": id_num,
    }
    response = json.dumps({
        "jobId": jobId,
        "status": status,
        "authenticationUrl": f"{self.hostname}/Login/Negotiate.ashx",
        "authenticationTicket": util.auth.CreateAuthTicket(
            self.server.storage,
            current_user.id,
        ),
        "message": None,
        "rand": random.randint(0, 100000000000),
        "joinScript": joinScript
    }).encode('utf-8')

    self.send_response(200)
    self.send_header("Content-Type", "application/json")
    self.send_header("Content-Length", str(len(response)))
    self.end_headers()
    self.wfile.write(response)
    self.wfile.flush()
    return True

@server_path('/Game/JoinRate.ashx', commands={'GET'})
def _(self: web_server_handler) -> bool:
    self.send_response(200)
    self.send_header("Content-Type", "application/json")
    self.end_headers()
    self.send_json({})
    return True

@server_path('/login/negotiate.ashx')
@server_path('/Login/Negotiate.ashx')
@server_path('/universes/validate-place-join')
def _(self: web_server_handler) -> bool:
    if self.query.get('suggest'):
        return util.auth.HandleLoginNegotiate(self)
    self.send_json(True)
    return True


@server_path('/game/PlaceLauncher.ashx')
@server_path('/Game/PlaceLauncher.ashx')
@server_path('/game/placelauncher.ashx')
def _(self: web_server_handler) -> bool:
    current_user = get_place_launcher_user(
        self,
        consume_ticket=False,
    )
    if current_user is None:
        self.send_json({
            'status': 12,
            'jobId': '67',
            'joinScriptUrl': build_place_launcher_url(self),
            'authenticationUrl': f'{self.hostname}/login/negotiate.ashx',
            'authenticationTicket': '',
            'message': 'Invalid request',
        })
        return True

    result = init_player(self.game_config, current_user)
    if result is None:
        self.send_json({
            'status': 12,
            'jobId': '67',
            'joinScriptUrl': build_place_launcher_url(self),
            'authenticationUrl': f'{self.hostname}/login/negotiate.ashx',
            'authenticationTicket': '',
            'message': None,
        })
        return True

    auth_ticket = util.auth.CreateAuthTicket(
        self.server.storage,
        current_user.id,
    )
    self.send_json({
        'status': 2,
        'joinScriptUrl': f'{self.hostname}/game/join.ashx?{self.url_split.query}',
        'authenticationUrl': f'{self.hostname}/login/negotiate.ashx',
        'authenticationTicket': auth_ticket,
        'jobId': '67',
        'message': '',
    })
    return True

@server_path("/game/get-join-script")
@util.auth.authenticated_required_api
def _(self: web_server_handler) -> bool:
    return send_get_join_script(self)


def send_get_join_script(self: web_server_handler) -> bool:
    current_user = get_authenticated_join_user(self)
    if current_user is None:
        self.send_json({"error": "403: disallowed user"}, 403)
        return True

    place_launcher_ticket = util.auth.CreateAuthTicket(
        self.server.storage,
        current_user.id,
    )
    authentication_ticket = util.auth.CreateAuthTicket(
        self.server.storage,
        current_user.id,
    )
    place_launcher_url = build_place_launcher_url(
        self,
        place_launcher_ticket,
    )
    request_token = util.auth.GetRequestToken(self) or authentication_ticket
    client_version = get_player_client_version(self)
    launch_url = build_player_launch_prefix(
        request_token,
        place_launcher_url,
        client_version,
    )
    self.send_json({
        'status': 2,
        'joinScriptUrl': place_launcher_url,
        'joinUrl': launch_url,
        'authenticationUrl': f'{self.hostname}/login/negotiate.ashx',
        'authenticationTicket': authentication_ticket,
        'jobId': '67',
        'prefix': launch_url,
    })
    return True
