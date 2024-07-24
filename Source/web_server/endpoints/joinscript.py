from web_server._logic import web_server_handler, server_path
import util.versions as versions
import util.resource
import util.const
import util.ssl
import json


def perform_join(self: web_server_handler):
    # The query arguments in `Roblox-Session-Id` were previously serialised
    # when `join.ashx` was called the first time a player joined.
    # Only 2021E supports rejoining when connection is lost.
    query_args = json.loads(
        self.headers.get('Roblox-Session-Id', '{}'),
    ) | self.query

    rcc_host_addr = query_args.get('rcc-host-addr', self.hostname)
    rcc_port = query_args.get('rcc-port')

    user_code = query_args.get('user-code')
    if user_code is None:
        return {}

    username = self.game_config.server_core.retrieve_username(user_code)
    id_num = self.game_config.server_core.retrieve_user_id(user_code)

    database = self.server.database.players
    (user_code, username, id_num) = database.add_player(
        user_code, username, id_num
    )

    return {
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
            util.const.DEFAULT_PLACE_ID,
        'UserName':
            username,
        'DisplayName':
            username,
        'AccountAge':
            self.game_config.server_core.retrieve_account_age(user_code),
        'ChatStyle':
            self.game_config.server_core.chat_style.value,
        'characterAppearanceId':
            id_num,
        'CharacterAppearanceId':
            id_num,
        'CharacterAppearance':
            f'{self.hostname}/v1.1/avatar-fetch?userId={id_num}',

        # NOTE: the `SessionId` is saved as an HTTPS header for later requests.
        # I'm placing the information which was passed into `join.ashx` here for simplicity.
        'SessionId': json.dumps(query_args),
    }


@server_path('/game/join.ashx', versions={versions.rōblox.v348})
def _(self: web_server_handler) -> bool:
    self.send_json(perform_join(self) | {
        'ClientPort': 0,
        'PingUrl': '',
        'PingInterval': 0,
        'SeleniumTestMode': False,
        'SuperSafeChat': True,
        'MeasurementUrl': '',
        'WaitingForCharacterGuid': 'e01c22e4-a428-45f8-ae40-5058b4a1dafc',
        'VendorId': 0,
        'ScreenShotInfo': '',
        'VideoInfo': '',
        'CreatorId': 1,
        'CreatorTypeEnum': 'User',
        'MembershipType': 'OutrageousBuildersClub',
        'CookieStoreFirstTimePlayKey': 'rbx_evt_ftp',
        'CookieStoreFiveMinutePlayKey': 'rbx_evt_fmp',
        'CookieStoreEnabled': False,
        'IsRobloxPlace': True,
        'GenerateTeleportJoin': False,
        'IsUnknownOrUnder13': False,
        'SessionId': '',
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
        'GameId': 1818,
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
