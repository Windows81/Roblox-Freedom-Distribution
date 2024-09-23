from web_server._logic import web_server_handler, server_path
from typing_extensions import Any
import util.versions as versions
import util.resource
import util.const
import util.ssl
import json


def init_player(self: web_server_handler, user_code: str, id_num: int) -> tuple[str, int, str]:
    config = self.game_data.config

    username = config.server_core.retrieve_username(
        id_num, user_code,
    )

    (user_code, id_num, username) = self.server.storage.players.add_player(
        user_code, id_num, username,
    )

    # This method only affects a player's fund balance if they're joining for the first time.
    self.server.storage.funds.first_init(
        id_num, config.server_core.retrieve_default_funds(id_num, user_code),
    )
    return (user_code, id_num, username)


def perform_join(self: web_server_handler) -> dict[str, Any]:
    '''
    The query arguments in `Roblox-Session-Id` were previously serialised
    when `join.ashx` was called the first time a player joined.

    Some methods (such as retrieving a user fund balance or rejoining in 2021E)
    need data from `Roblox-Session-Id`.
    '''
    config = self.game_data.config
    server_core = config.server_core
    query_args = json.loads(
        self.headers.get('Roblox-Session-Id', '{}'),
    ) | self.query

    rcc_host_addr = query_args.get('rcc-host-addr', self.hostname)
    rcc_port = query_args.get('rcc-port')
    user_code = query_args.get('user-code')

    # Very hacky to call `send_error` when the webserver will later call `send_json`.
    if user_code is None:
        self.send_error(404)
        return {}

    id_num = config.server_core.retrieve_user_id(user_code)

    # The `check_user_allowed` function will also be called after the player is added.
    # (Potentially) for additional protection.
    if not server_core.check_user_allowed(id_num, user_code):
        self.send_error(403)
        return {}

    (user_code, id_num, username) = init_player(self, user_code, id_num)

    join_data = {
        'ServerConnections': [
            {
                'Address': rcc_host_addr,
                'Port': rcc_port,
            }
        ],
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
        'SessionId': json.dumps(join_data)
    }
    return join_data


@server_path('/game/join.ashx', versions={versions.rōblox.v348})
def _(self: web_server_handler) -> bool:
    self.send_json(perform_join(self) | {
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
        'CreatorId': 1,
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
    }, sign_prefix=b'--rbxsig')
    return True


@server_path('/game/join.ashx', versions={versions.rōblox.v463})
def _(self: web_server_handler) -> bool:
    self.send_json(perform_join(self) | {
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
        'CreatorId': 4372130,
        'CreatorTypeEnum': 'Group',
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
    }, sign_prefix=b'--rbxsig2')
    return True


@server_path('/game/PlaceLauncher.ashx')
@server_path('/game/placelauncher.ashx')
def _(self: web_server_handler) -> bool:
    self.send_json({
        'jobId': 'Test',
        'status': 2,
        'joinScriptUrl': f'{self.hostname}/game/join.ashx?{self.url_split.query}',
        'authenticationUrl': f'{self.hostname}/login/negotiate.ashx',
        'authenticationTicket': '1',
        'message': None,
    })
    return True
