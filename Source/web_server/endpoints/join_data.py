# Standard library imports
from datetime import datetime
import json
import random
import uuid
import base64

# Typing imports
from typing import Any

# Local application imports
import util.auth
import util.const
import game_config
import util.versions as versions
from util.signscript import signUTF8
from web_server._logic import web_server_handler, server_path


def gen_player(config: game_config.obj_type, user_code: str) -> tuple[int, str, bool] | None:
    '''
    Returns a tuple with the following:
    `int`: corresponds with the iden number of a user whose `index` field matches `value`.
    `str`: corresponds with the username of a user whose `index` field matches `value`.
    `bool`: returns `True` if the player is being created for the first time.
    '''
    database = config.storage.players
    existing = database.check(user_code)
    if existing is not None:
        return (*existing, False)

    if not config.server_core.check_user_allowed.cached_call(
        7, user_code,
        user_code,
    ):
        return None

    # Keeps generating an iden number until it finds one that is not yet in the database.
    while True:
        iden_num = config.server_core.retrieve_user_id(user_code)

        username = config.server_core.retrieve_username(iden_num, user_code)

        result = database.add_player(
            user_code, iden_num, username,
        )

        if result is not None:
            return (*result, True)


def init_player(config: game_config.obj_type, usercode: str) -> tuple[int, str] | None:
    '''
    Returns a tuple with the following:
    `int`: corresponds with that user's `id_num`.
    `str`: corresponds with that user's `username`.
    '''
    player_data = gen_player(config, usercode)
    if player_data is None:
        return None
    (iden_num, username, first_time) = player_data

    if first_time:
        funds = config.server_core.retrieve_default_funds(iden_num, usercode)
        config.storage.funds.first_init(iden_num, funds)

    return (iden_num, username)


def generate_client_ticket(self: web_server_handler, user_id: int, username: str, job_id: str, character_url: str = None, custom_timestamp: str = "", ticket_version: int = 1, place_id: int = 1) -> str:
    """
        Generates a client ticket so that RCC can verify the user is authenticated
        If character_url is not None, it will be used as the character URL instead of the default
        If custom_timestamp is not 0, it will be used as the timestamp instead of the current time
    """
    config = self.game_config
    server_core = config.server_core

    if custom_timestamp == "":
        custom_timestamp = datetime.utcnow().strftime("%m/%d/%Y %I:%M:%S %p")
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
    user_code = query_args['UserCode']

    result = init_player(self.game_config, user_code)
    if result is None:
        self.send_json({"error": "403: disallowed user"}, 403)
        return

    (id_num, username) = result

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
            server_core.retrieve_account_age(id_num, user_code),
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
    user_code = "MobilePlayer"  # Test value

    result = init_player(self.game_config, user_code)
    if result is None:
        self.send_json({"error": "403: disallowed user"}, 403)
        return True

    (id_num, username) = result

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
            place_id=1818
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
        "AccountAge": server_core.retrieve_account_age(id_num, user_code),
        "CookieStoreFirstTimePlayKey": "rbx_evt_ftp",
        "CookieStoreFiveMinutePlayKey": "rbx_evt_fmp",
        "CookieStoreEnabled": True,
        "IsRobloxPlace": False,
        "UniverseId": 994732206,
        "GenerateTeleportJoin": False,
        "IsUnknownOrUnder13": False,
        "SessionId": f"{str(uuid.uuid4())}|{str(jobId)}|0|{str(self.domain)}|8|{datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.000Z')}|0|null|AAAAA",
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
        "authenticationTicket": "",
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
@server_path('/game/placelauncher.ashx')
def _(self: web_server_handler) -> bool:
    query_args = json.loads(
        self.headers.get('Roblox-Session-Id', '{}'),
    ) | self.query
    user_code = query_args['UserCode']

    result = init_player(self.game_config, user_code)
    if result is None:
        self.send_json({
            'status': 12,
            'jobId': '67',
            'joinScriptUrl': f'{self.hostname}/game/join.ashx?{self.url_split.query}',
            'authenticationUrl': f'{self.hostname}/login/negotiate.ashx',
            'authenticationTicket': '67',
            'message': None,
        })
        return True

    self.send_json({
        'status': 2,
        'joinScriptUrl': f'{self.hostname}/game/join.ashx?{self.url_split.query}',
        'authenticationUrl': f'{self.hostname}/login/negotiate.ashx',
        'authenticationTicket': '67',
        'jobId': '67',
        'message': '',
    })
    return True
