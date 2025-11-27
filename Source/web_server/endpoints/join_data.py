# Standard library imports
import functools
import json

# Typing imports
from typing import Any

# Local application imports
import util.const
import game_config
import util.versions as versions
from web_server._logic import web_server_handler, server_path


def gen_player(config: game_config.obj_type, usercode: str) -> tuple[int, str, bool] | None:
    '''
    Returns a tuple with the following:
    `int`: corresponds with the iden number of a user whose `index` field matches `value`.
    `str`: corresponds with the username of a user whose `index` field matches `value`.
    `bool`: returns `True` if the player is being created for the first time.
    '''
    database = config.storage.players
    existing = database.check(usercode)
    if existing is not None:
        return (*existing, False)

    # Keeps generating an iden number until it finds one that is not yet in the database.
    while True:
        iden_num = config.server_core.retrieve_user_id(usercode)
        if not config.server_core.check_user_allowed.cached_call(
            7, usercode,
            iden_num, usercode,
        ):
            return None

        username = config.server_core.retrieve_username(iden_num, usercode)

        result = database.add_player(
            usercode, iden_num, username,
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


def perform_and_send_join(self: web_server_handler, additional_return_data: dict[str, Any], prefix: bytes) -> None:
    '''
    The query arguments in `Roblox-Session-Id` were previously serialised.
    For example, when `join.ashx` was called the first time a player joined.

    Some methods (such as retrieving a user fund balance, or rejoining in 2021E) need data from `Roblox-Session-Id`.
    '''
    config = self.game_config
    server_core = config.server_core

    query_args: dict[str, str] = json.loads(
        self.headers.get('Roblox-Session-Id', '{}'),
    ) | self.query

    rcc_host_addr = str(query_args.get('rcc-host-addr', self.hostname))
    rcc_port = int(query_args.get('rcc-port', self.port_num))
    user_code = query_args['user-code']

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
    self.send_json(join_data | additional_return_data, prefix=prefix)


@server_path('/game/join.ashx', versions={versions.rōblox.v348})
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


@server_path('/login/negotiate.ashx')
@server_path('/universes/validate-place-join')
def _(self: web_server_handler) -> bool:
    self.send_json(True)
    return True


@server_path('/game/PlaceLauncher.ashx')
@server_path('/game/placelauncher.ashx')
def _(self: web_server_handler) -> bool:

    query_args = json.loads(
        self.headers.get('Roblox-Session-Id', '{}'),
    ) | self.query
    user_code = query_args.get('user-code')

    result = init_player(self.game_config, user_code)
    if result is None:
        self.send_json({
            'status': 12,
            'jobId': '',
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
        'authenticationTicket': '',
        'jobId': '',
        'message': "gggjlkdsjgkls",
    })
    return True
