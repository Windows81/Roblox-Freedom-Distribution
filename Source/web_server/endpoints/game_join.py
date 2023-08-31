import re
from web_server._logic import web_server_handler, server_path
import util.ssl_context
import util.const
import json
import time


def basic_join(self: web_server_handler):
    ip_addr = self.query.get('ip', None)
    port_num = self.query.get('port', None)
    user_code = self.query.get('user', None)
    if not user_code:
        user_code = self.game_config.server_core.retrieve_default_user_code(time.time())
    return {
        'ServerConnections': [
            {
                'Address': ip_addr,
                'Port': port_num,
            }
        ],
        'MachineAddress':
            ip_addr,
        'ServerPort':
            port_num,
        'BaseUrl':
            self.hostname,
        'PlaceId':
            util.const.DEFAULT_PLACE_ID,
        'UserName':
            self.game_config.server_core.retrieve_username(user_code),
        'DisplayName':
            self.game_config.server_core.retrieve_username(user_code),
        'UserId':
            self.game_config.server_core.retrieve_user_id(user_code),
        'AccountAge':
            self.game_config.server_core.retrieve_account_age(user_code),
        'ChatStyle':
            self.game_config.server_core.chat_style.value,
        'CharacterAppearanceId':
            self.game_config.server_core.retrieve_user_id(user_code),
        'CharacterAppearance':
            '',
    }


@server_path('/retrieve_certs')
def _(self: web_server_handler) -> bool:
    self.send_data(util.ssl_context.get_client_cert())
    return True


@server_path('/roblox_version')
def _(self: web_server_handler) -> bool:
    '''
    Used by clients to automatically detect which version to run.
    '''
    self.send_data(bytes(self.server.game_config.game_setup.roblox_version.name, encoding='utf-8'))
    return True


@server_path('/game/join.ashx')
def _(self: web_server_handler) -> bool:
    self.send_json(basic_join(self) | {
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
        'IsUnknownOrUnder13': True,
        'SessionId': '',
        'DataCenterId': 0,
        'FollowUserId': 0,
        'UniverseId': 0,
    }, sign_prefix=b'--rbxsig')
    return True


@server_path('/game/join.ashx', min_version=401)
def _(self: web_server_handler) -> bool:
    self.send_json(basic_join(self) | {
        'ClientPort': 0,
        'PingUrl': '',
        'PingInterval': 0,
        'DirectServerReturn': True,
        'SeleniumTestMode': False,
        'RobloxLocale': 'en_us',
        'GameLocale': 'en_us#RobloxTranslateAbTest2',
        'SuperSafeChat': True,
        'ClientTicket': '2022-03-26T05:13:05.7649319Z;dj09X5iTmYtOPwh0hbEC8yvSO1t99oB3Yh5qD/sinDFszq3hPPaL6hH16TvtCen6cABIycyDv3tghW7k8W+xuqW0/xWvs0XJeiIWstmChYnORzM1yCAVnAh3puyxgaiIbg41WJSMALRSh1hoRiVFOXw4BKjSKk7DrTTcL9nOG1V5YwVnmAJKY7/m0yZ81xE99QL8UVdKz2ycK8l8JFvfkMvgpqLNBv0APRNykGDauEhAx283vARJFF0D9UuSV69q6htLJ1CN2kXL0Saxtt/kRdoP3p3Nhj2VgycZnGEo2NaG25vwc/KzOYEFUV0QdQPC8Vs2iFuq8oK+fXRc3v6dnQ==;BO8oP7rzmnIky5ethym6yRECd6H14ojfHP3nHxSzfTs=;XsuKZL4TBjh8STukr1AgkmDSo5LGgQKQbvymZYi/80TYPM5/MXNr5HKoF3MOT3Nfm0MrubracyAtg5O3slIKBg==;6',
        'GameId': '29fd9df4-4c59-4d8c-8cee-8f187b09709b',
        'CreatorId': 4372130,
        'CreatorTypeEnum': 'Group',
        'MembershipType': 'None',
        'CookieStoreFirstTimePlayKey': 'rbx_evt_ftp',
        'CookieStoreFiveMinutePlayKey': 'rbx_evt_fmp',
        'CookieStoreEnabled': True,
        'IsUnknownOrUnder13': True,
        'GameChatType': 'AllUsers',
        'SessionId': json.dumps({
            'SessionId': 'c89589f1-d1de-46e3-80e0-2703d1159409',
            'GameId': '29fd9df4-4c59-4d8c-8cee-8f187b09709b',
            'PlaceId': util.const.DEFAULT_PLACE_ID,
            'ClientIpAddress': '207.241.232.186',
            'PlatformTypeId': 5,
            'SessionStarted': '2022-03-26T05:13:05.762819Z',
            'BrowserTrackerId': 129849985826,
            'PartyId': None,
            'Age': 80.2683342765271,
            'Latitude': 37.78,
            'Longitude': -122.465,
            'CountryId': 1,
            'PolicyCountryId': 'US',
            'LanguageId': 41,
            'BlockedPlayerIds': [],
            'JoinType': 'MatchMade',
            'PlaySessionFlags': 0,
            'MatchmakingDecisionId': 'a0311216-ec21-4b5d-b3c0-8538a9a4dc7d',
            'UserScoreObfuscated': 4895515560,
            'UserScorePublicKey': 235,
            'GameJoinMetadata': {
                'JoinSource': 0,
                'RequestType': 0
            },
            'RandomSeed2': '7HOfysTid4XsV/3mBPPPhKHIykE4GXSBBBzd93rplbDQ3bNSgPFcR9auB780LjNYg+4mbNQPOqTmJ2o3hUefmw==',
            'IsUserVoiceChatEnabled': True,
            'SourcePlaceId': None,
        }),
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


@server_path('/game/placelauncher.ashx')
def _(self: web_server_handler) -> bool:
    self.send_json({
        'jobId': 'Test',
        'status': 2,
        'joinScriptUrl': f'{self.hostname}/game/join.ashx?{self.urlsplit.query}',
        'authenticationUrl': f'{self.hostname}/login/negotiate.ashx',
        'authenticationTicket': '1',
        'message': None,
    })
    return True


@server_path('/marketplace/productinfo')
def _(self: web_server_handler) -> bool:
    self.send_json({
        'AssetId': 93722443,
        'ProductId': 13831621,
        'Name': self.game_config.game_setup.name,
        'Description': self.game_config.game_setup.description,
        'AssetTypeId': 19,
        'Creator': {
            'Id': 1,
            'Name': self.game_config.game_setup.creator.name,
            'CreatorType': 'User',
            'CreatorTargetId': 1
        },
        'IconImageAssetId': 0,
        'Created': '2012-09-28T01:09:47.077Z',
        'Updated': '2017-01-03T00:25:45.8813192Z',
        'PriceInRobux': None,
        'PriceInTickets': None,
        'Sales': 0,
        'IsNew': False,
        'IsForSale': True,
        'IsPublicDomain': False,
        'IsLimited': False,
        'IsLimitedUnique': False,
        'Remaining': None,
        'MinimumMembershipLevel': 0,
        'ContentRatingTypeId': 0,
    })
    return True


@server_path('/game/load-place-info')
@server_path('/.127.0.0.1/game/load-place-info')
@server_path('/.127.0.0.1/game/load-place-info/')
def _(self: web_server_handler) -> bool:
    self.send_json({
        'CreatorId': 1,
        'CreatorType': 'User',
        'PlaceVersion': 1,
        'GameId': 123456,
        'IsRobloxPlace': True,
    })
    return True


@server_path('/login/negotiate.ashx')
@server_path('/universes/validate-place-join')
def _(self: web_server_handler) -> bool:
    self.send_json(True)
    return True


@server_path('/Setting/QuietGet/ClientAppSettings/')
def _(self: web_server_handler) -> bool:
    self.send_json({})
    return True


@server_path('/asset-thumbnail/json')
def _(self: web_server_handler) -> bool:
    self.send_json({
        'Url': f'{self.hostname}/Thumbs/GameIcon.ashx',
        'Final': True,
        'SubstitutionType': 0,
    })
    return True


@server_path('/Thumbs/GameIcon.ashx')
def _(self: web_server_handler) -> bool:
    with open(self.game_config.game_setup.icon_path, 'rb') as f:
        self.send_data(f.read())
    return True


@server_path('/v1/settings/application')
def _(self: web_server_handler) -> bool:
    self.send_json({'applicationSettings': {}})
    return True


@server_path('/v1/player-policies-client')
def _(self: web_server_handler) -> bool:
    self.send_json({
        'isSubjectToChinaPolicies': False,
        'arePaidRandomItemsRestricted': False,
        'isPaidItemTradingAllowed': True,
        'areAdsAllowed': True,
    })
    return True


@server_path('/users/([0-9]+)/canmanage/([0-9]+)', regex=True)
def _(self: web_server_handler, match: re.Match[str]) -> bool:
    self.send_json({"Success": True, "CanManage": True})
    return True


@server_path('/v1/user/([0-9]+)/is-admin-developer-console-enabled', regex=True)
def _(self: web_server_handler, match: re.Match[str]) -> bool:
    self.send_json({"isAdminDeveloperConsoleEnabled": True})
    return True


@server_path('/v1/avatar-fetch')
@server_path('/v1/avatar-fetch/')
def _(self: web_server_handler) -> bool:
    self.send_json({"scales": {"height": 1.0, "width": 1.0, "head": 1.0, "depth": 1.00, "proportion": 0.0, "bodyType": 0.0}, "playerAvatarType": "R6", "bodyColors": {"headColorId": 1002, "torsoColorId": 1002, "rightArmColorId": 1002, "leftArmColorId": 1002, "rightLegColorId": 1002, "leftLegColorId": 1002}, "assets": [{"id": 63690008, "name": "Pal Hair", "assetType": {"id": 41, "name": "HairAccessory"}, "currentVersionId": 8443736161, "meta": {"order": 11, "version": 1}}, {"id": 86498048, "name": "Man Head", "assetType": {"id": 17, "name": "Head"}, "currentVersionId": 11008778043}, {"id": 86500008, "name": "Man Torso", "assetType": {"id": 27, "name": "Torso"}, "currentVersionId": 11837972128}, {"id": 86500036, "name": "Man Right Arm", "assetType": {"id": 28, "name": "RightArm"}, "currentVersionId": 11837973329}, {"id": 86500054, "name": "Man Left Arm", "assetType": {"id": 29, "name": "LeftArm"}, "currentVersionId": 11837974431}, {
                   "id": 86500064, "name": "Man Left Leg", "assetType": {"id": 30, "name": "LeftLeg"}, "currentVersionId": 11837975410}, {"id": 86500078, "name": "Man Right Leg", "assetType": {"id": 31, "name": "RightLeg"}, "currentVersionId": 11837976476}, {"id": 144076358, "name": "Blue and Black Motorcycle Shirt", "assetType": {"id": 11, "name": "Shirt"}, "currentVersionId": 339950145}, {"id": 144076760, "name": "Dark Green Jeans", "assetType": {"id": 12, "name": "Pants"}, "currentVersionId": 339951177}, {"id": 453479994, "name": "roblox compute cloud", "assetType": {"id": 2, "name": "TShirt"}, "currentVersionId": 765412475}, {"id": 2510235063, "name": "Rthro Idle", "assetType": {"id": 51, "name": "IdleAnimation"}, "currentVersionId": 13806699932}], "defaultShirtApplied": False, "defaultPantsApplied": False, "emotes": [{"assetId": 3360689775, "assetName": "Salute", "position": 1}, {"assetId": 3576968026, "assetName": "Shrug", "position": 2}]})
    return True
