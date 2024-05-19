from web_server._logic import web_server_handler, server_path, web_server_ssl
import util.resource
import util.const
import util.ssl
import json
import time
import re


def basic_join(self: web_server_handler):
    ip_addr = self.query.get('ip', None)
    port_num = self.query.get('port', None)

    user_code = self.query.get('user', None)
    if not user_code:
        user_code = self.game_config.server_core. \
            retrieve_default_user_code(time.time())
    user_id = self.server.game_users.add_user(user_code)

    return {
        'ServerConnections': [
            {
                'Address': ip_addr,
                'Port': port_num,
            }
        ],
        'UserId':
            user_id,
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
        'AccountAge':
            self.game_config.server_core.retrieve_account_age(user_code),
        'ChatStyle':
            self.game_config.server_core.chat_style.value,
        'characterAppearanceId':
            user_id,
        'CharacterAppearanceId':
            user_id,
        'CharacterAppearance':
            f'{self.hostname}/v1.1/avatar-fetch?userId={user_id}',
    }


@server_path('/rfd/certificate')
def _(self: web_server_handler) -> bool:
    if not isinstance(self.server, web_server_ssl):
        return False
    self.server.add_identities(self.ip_addr)
    self.send_data(self.server.ssl_mutable.get_client_cert())
    return True


@server_path('/rfd/roblox-version')
def _(self: web_server_handler) -> bool:
    '''
    Used by clients to automatically detect which version to run.
    '''
    self.send_data(
        bytes(self.server.game_config.game_setup.roblox_version.name, encoding='utf-8'))
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
        'IsUnknownOrUnder13': False,
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
        'IsUnknownOrUnder13': False,
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


@server_path('/Game/PlaceLauncher.ashx')
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


@server_path('/game/validate-machine')
def _(self: web_server_handler) -> bool:
    self.send_json({"success": True})
    return True


@server_path('/v1.1/avatar-fetch/')
def _(self: web_server_handler) -> bool:
    '''
    Character appearance for v348.
    '''
    self.query
    userid = self.query['userId']
    placeId = self.query['placeId']
    json = {
        "animations": {},
        "resolvedAvatarType": self.game_config.server_core.avatar_type.value,
        "accessoryVersionIds": [],
        "equippedGearVersionIds": [],
        "backpackGearVersionIds": [],
        "bodyColors": {
            "HeadColor": 1013,
            "LeftArmColor": 1013,
            "LeftLegColor": 1013,
            "RightArmColor": 1013,
            "RightLegColor": 1013,
            "TorsoColor": 1013,
        },
        "scales": {
            "Height": 2.0000,
            "Width": 2.0000,
            "Head": 2.0000,
            "Depth": 2.0000,
            "Proportion": 0.0000,
            "BodyType": 0.0000,
        },
    }
    self.send_json(json)
    return True


@server_path('/v1/avatar', min_version=400)
@server_path('/v1/avatar/', min_version=400)
@server_path('/v1/avatar-fetch', min_version=400)
@server_path('/v1/avatar-fetch/', min_version=400)
def _(self: web_server_handler) -> bool:
    '''
    Character appearance for v463.
    '''
    self.send_json({
        "playerAvatarType": "R15",
        "scales": {
            "height": 1.0,
            "width": 1.0,
            "head": 1.0,
            "depth": 1.00,
            "proportion": 0.0,
            "bodyType": 0.0
        },
        "bodyColors": {
            "headColorId": 1002,
            "torsoColorId": 1002,
            "rightArmColorId": 1002,
            "leftArmColorId": 1002,
            "rightLegColorId": 1002,
            "leftLegColorId": 1002
        },
        "assets": [
            {"id": 63690008, "name": "Pal Hair", "assetType": {"id": 41, "name": "HairAccessory"},
                "currentVersionId": 8443736161, "meta": {"order": 11, "version": 1}},
        ],
        "defaultShirtApplied": False,
        "defaultPantsApplied": False,
        "emotes": [
            {"assetId": 3360689775, "assetName": "Salute", "position": 1},
            {"assetId": 3576968026, "assetName": "Shrug", "position": 2},
        ]
    })
    return True

    self.send_json({
        "resolvedAvatarType": self.game_config.server_core.avatar_type.value,
        "equippedGearVersionIds": [],
        "backpackGearVersionIds": [],
        "assetAndAssetTypeIds": [
            {
                "assetId": 10726856854,
                "assetTypeId": 28
            },
            {
                "assetId": 9482991343,
                "assetTypeId": 71,
                "meta": {
                    "order": 3,
                    "version": 1
                }
            },
            {
                "assetId": 9481782649,
                "assetTypeId": 70,
                "meta": {
                    "order": 3,
                    "version": 1
                }
            },
            {
                "assetId": 9120251003,
                "assetTypeId": 66,
                "meta": {
                    "order": 4,
                    "version": 1
                }
            },
            {
                "assetId": 6445262286,
                "assetTypeId": 30
            },
            {
                "assetId": 6969309778,
                "assetTypeId": 11
            },
            {
                "assetId": 5731052645,
                "assetTypeId": 8
            },
            {
                "assetId": 2846257298,
                "assetTypeId": 8
            },
            {
                "assetId": 121390054,
                "assetTypeId": 42
            },
            {
                "assetId": 261826995,
                "assetTypeId": 42
            },
            {
                "assetId": 154386348,
                "assetTypeId": 12
            },
            {
                "assetId": 201733574,
                "assetTypeId": 47
            },
            {
                "assetId": 48474294,
                "assetTypeId": 41,
                "meta": {
                    "order": 11,
                    "version": 1
                }
            },
            {
                "assetId": 6340101,
                "assetTypeId": 17
            },
            {
                "assetId": 192483960,
                "assetTypeId": 47
            },
            {
                "assetId": 190245296,
                "assetTypeId": 43
            },
            {
                "assetId": 183808364,
                "assetTypeId": 8
            },
            {
                "assetId": 34247191,
                "assetTypeId": 8
            }
        ],
        "animationAssetIds": {
            "run": 2510238627,
            "jump": 2510236649,
            "fall": 2510233257,
            "climb": 2510230574
        },
        "bodyColors": {
            "headColorId": 105,
            "torsoColorId": 105,
            "rightArmColorId": 105,
            "leftArmColorId": 105,
            "rightLegColorId": 105,
            "leftLegColorId": 105,

            "HeadColor": 1013,
            "TorsoColor": 1013,
            "RightUpperArm": 1013,
            "LeftArmColor": 1013,
            "RightLegColor": 1013,
            "LeftLegColor": 1013,
        },
        "scales": {
            "height": 1.05,
            "width": 1,
            "head": 1,
            "depth": 1,
            "proportion": 1,
            "bodyType": 0.8
        },
        "emotes": [
            {
                "assetId": 3696763549,
                "assetName": "Heisman Pose",
                "position": 1
            },
            {
                "assetId": 3360692915,
                "assetName": "Tilt",
                "position": 2
            },
            {
                "assetId": 3696761354,
                "assetName": "Air Guitar",
                "position": 3
            },
            {
                "assetId": 3576968026,
                "assetName": "Shrug",
                "position": 4
            },
            {
                "assetId": 3576686446,
                "assetName": "Hello",
                "position": 5
            },
            {
                "assetId": 3696759798,
                "assetName": "Superhero Reveal",
                "position": 6
            },
            {
                "assetId": 3360689775,
                "assetName": "Salute",
                "position": 7
            },
            {
                "assetId": 3360686498,
                "assetName": "Stadium",
                "position": 8
            }
        ]
    })
    return True


@server_path('/avatar-thumbnail/json')
def _(self: web_server_handler) -> bool:
    '''
    To simplify the server program, let's not there be avatar thumbnail storage.
    '''
    self.send_json({})
    return True


@server_path('/avatar-thumbnail/image')
def _(self: web_server_handler) -> bool:
    '''
    To simplify the server program, let's not there be avatar thumbnail images.
    '''
    return True


# TODO: handle social requests.
@server_path('/Game/LuaWebService/HandleSocialRequest.ashx')
def _(self: web_server_handler) -> bool:
    match self.query['method']:
        case 'GetGroupRank':
            self.send_data(
                bytes(f'<Value Type="integer">{255}</Value>', encoding='utf-8'))
            return True

    self.send_json({})
    return True


@server_path('/v2/users/([0-9]+)/groups/roles', regex=True)
def _(self: web_server_handler, match: re.Match[str]) -> bool:
    self.send_json({
        "data": [
            {
                "group": {
                    "id": group_id,
                    "name": "string",
                    "memberCount": 0,
                    "hasVerifiedBadge": True,
                },
                "role": {
                    "id": group_id,
                    "name": "string",
                    "rank": 255,
                },
                "isNotificationsEnabled": True,
            }
            for group_id in [
                1200769,
                2868472,
                4199740,
                4265462,
                4265456,
                4265443,
                4265449,
            ]
        ]
    })
    return True


@server_path('/gametransactions/getpendingtransactions/', min_version=400)
def _(self: web_server_handler) -> bool:
    self.send_json([])
    return True
