import json
from ..logic import webserver_handler, server_path
import util.const as const


@server_path("/game/join.ashx")
def _(self: webserver_handler) -> bool:
    placeid = self.query.get('placeid', None)
    ip = self.query.get('ip', None)
    port = self.query.get('port', None)
    uid = self.query.get('id', 0)
    username = self.query.get('user', None)
    app = self.query.get('app', None)
    membership = self.query.get('membership', None)

    self.send_json({
        'ClientPort': 0,
        'MachineAddress': ip,
        'ServerPort': port,
        'PingUrl': '',
        'PingInterval': 0,
        'UserName': username,
        'SeleniumTestMode': False,
        'UserId': int(uid),
        'SuperSafeChat': False,
        'CharacterAppearance': app,
        'PlaceId': int(placeid),
        'MeasurementUrl': '',
        'WaitingForCharacterGuid': 'e01c22e4-a428-45f8-ae40-5058b4a1dafc',
        'BaseUrl': self.host,
        'ChatStyle': 'ClassicAndBubble',
        'VendorId': 0,
        'ScreenShotInfo': '',
        'VideoInfo': '<?xml version="1.0"?><entry xmlns="http://www.w3.org/2005/Atom" xmlns:media="http://search.yahoo.com/mrss/" xmlns:yt="http://gdata.youtube.com/schemas/2007"><media:group><media:title type="plain"><![CDATA[ROBLOX Place]]></media:title><media:description type="plain"><![CDATA[ For more games visit http://www.roblox.com]]></media:description><media:category scheme="http://gdata.youtube.com/schemas/2007/categories.cat">Games</media:category><media:keywords>ROBLOX, video, free game, online virtual world</media:keywords></media:group></entry>',
        'CreatorId': 1,
        'CreatorTypeEnum': 'User',
        'MembershipType': 'OutrageousBuildersClub',
        'AccountAge': 6969,
        'CookieStoreFirstTimePlayKey': 'rbx_evt_ftp',
        'CookieStoreFiveMinutePlayKey': 'rbx_evt_fmp',
        'CookieStoreEnabled': False,
        'IsRobloxPlace': True,
        'GenerateTeleportJoin': False,
        'IsUnknownOrUnder13': False,
        'SessionId': '',
        'DataCenterId': 0,
        'FollowUserId': 0,
        'CharacterAppearanceId': int(uid),
        'UniverseId': 0,
    }, sign_prefix=b'--rbxsig')
    return True


@server_path("/game/join.ashx", min_version=401)
def _(self: webserver_handler) -> bool:
    placeid = self.query.get('placeid', None)
    ip = self.query.get('ip', None)
    port = self.query.get('port', None)
    uid = self.query.get('id', 0)
    username = self.query.get('user', None)
    app = self.query.get('app', None)
    membership = self.query.get('membership', None)

    self.send_json({
        "ClientPort": 0,
        "MachineAddress": "127.0.0.1",
        "ServerPort": 2005,
        "ServerConnections": [
            {
                "Address": "127.0.0.1",
                "Port": 2005
            }
        ],
        "DirectServerReturn": True,
        "PingUrl": "",
        "PingInterval": 120,
        'UserName': username,
        "DisplayName": username,
        "SeleniumTestMode": False,
        'UserId': int(uid),
        "RobloxLocale": "en_us",
        "GameLocale": "en_us#RobloxTranslateAbTest2",
        "SuperSafeChat": False,
        'CharacterAppearance': app,
        "ClientTicket": "2022-03-26T05:13:05.7649319Z;dj09X5iTmYtOPwh0hbEC8yvSO1t99oB3Yh5qD/sinDFszq3hPPaL6hH16TvtCen6cABIycyDv3tghW7k8W+xuqW0/xWvs0XJeiIWstmChYnORzM1yCAVnAh3puyxgaiIbg41WJSMALRSh1hoRiVFOXw4BKjSKk7DrTTcL9nOG1V5YwVnmAJKY7/m0yZ81xE99QL8UVdKz2ycK8l8JFvfkMvgpqLNBv0APRNykGDauEhAx283vARJFF0D9UuSV69q6htLJ1CN2kXL0Saxtt/kRdoP3p3Nhj2VgycZnGEo2NaG25vwc/KzOYEFUV0QdQPC8Vs2iFuq8oK+fXRc3v6dnQ==;BO8oP7rzmnIky5ethym6yRECd6H14ojfHP3nHxSzfTs=;XsuKZL4TBjh8STukr1AgkmDSo5LGgQKQbvymZYi/80TYPM5/MXNr5HKoF3MOT3Nfm0MrubracyAtg5O3slIKBg==;6",
        "GameId": "29fd9df4-4c59-4d8c-8cee-8f187b09709b",
        'PlaceId': int(placeid),
        'BaseUrl': self.host,
        "ChatStyle": "ClassicAndBubble",
        "CreatorId": 4372130,
        "CreatorTypeEnum": "Group",
        "MembershipType": "None",
        "AccountAge": 1859,
        "CookieStoreFirstTimePlayKey": "rbx_evt_ftp",
        "CookieStoreFiveMinutePlayKey": "rbx_evt_fmp",
        "CookieStoreEnabled": True,
        "IsUnknownOrUnder13": False,
        "GameChatType": "AllUsers",
        "SessionId": json.dumps({
            "SessionId": "c89589f1-d1de-46e3-80e0-2703d1159409",
            "GameId": "29fd9df4-4c59-4d8c-8cee-8f187b09709b",
            "PlaceId": int(placeid),
            "ClientIpAddress": "207.241.232.186",
            "PlatformTypeId": 5,
            "SessionStarted": "2022-03-26T05:13:05.762819Z",
            "BrowserTrackerId": 129849985826,
            "PartyId": None,
            "Age": 80.2683342765271,
            "Latitude": 37.78,
            "Longitude": -122.465,
            "CountryId": 1,
            "PolicyCountryId": None,
            "LanguageId": 41,
            "BlockedPlayerIds": [],
            "JoinType": "MatchMade",
            "PlaySessionFlags": 0,
            "MatchmakingDecisionId": "a0311216-ec21-4b5d-b3c0-8538a9a4dc7d",
            "UserScoreObfuscated": 4895515560,
            "UserScorePublicKey": 235,
            "GameJoinMetadata": {
                "JoinSource": 0,
                "RequestType": 0
            },
            "RandomSeed2": "7HOfysTid4XsV/3mBPPPhKHIykE4GXSBBBzd93rplbDQ3bNSgPFcR9auB780LjNYg+4mbNQPOqTmJ2o3hUefmw==",
            "IsUserVoiceChatEnabled": True,
            "SourcePlaceId": None,
        }),
        "AnalyticsSessionId": "c89589f1-d1de-46e3-80e0-2703d1159409",
        "DataCenterId": 302,
        "UniverseId": 994732206,
        "FollowUserId": 0,
        'CharacterAppearanceId': int(uid),
        "CountryCode": "US",
        "RandomSeed1": "7HOfysTid4XsV/3mBPPPhKHIykE4GXSBBBzd93rplbDQ3bNSgPFcR9auB780LjNYg+4mbNQPOqTmJ2o3hUefmw==",
        "ClientPublicKeyData": json.dumps({
            "creationTime": "19:56 11/23/2021",
            "applications": {
                "RakNetEarlyPublicKey": {
                    "versions": [{
                        "id": 2,
                        "value": "HwatfCnkndvyKCMPSa0VAl2M2c0GQv9+0z0kENhcj2w=",
                        "allowed": True
                    }],
                    "send": 2,
                    "revert": 2,
                }
            }
        }),
    }, sign_prefix=b'--rbxsig2')
    return True


@ server_path("/game/placelauncher.ashx")
def _(self: webserver_handler) -> bool:
    self.send_json({
        'jobId': 'Test',
        'status': 2,
        'joinScriptUrl': f'{self.host}/game/join.ashx?{self.urlsplit.query}',
        'authenticationUrl': f'{self.host}/login/negotiate.ashx',
        'authenticationTicket': '1',
        'message': None,
    })
    return True


@ server_path("/marketplace/productinfo")
def _(self: webserver_handler) -> bool:
    self.send_json({
        'AssetId': 93722443,
        'ProductId': 13831621,
        'Name': 'place.rbxl',
        'Description': ':) everything will be ok friend',
        'AssetTypeId': 19,
        'Creator': {
            'Id': 1,
            'Name': 'Jetray#4509',
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
        'ContentRatingTypeId': 0
    })
    return True


@ server_path("/.127.0.0.1/game/load-place-info")
@ server_path("/.127.0.0.1/game/load-place-info/")
def _(self: webserver_handler) -> bool:
    self.send_json({
        'CreatorId': 1,
        'CreatorType': 'User',
        'PlaceVersion': 1,
        'GameId': 123456,
        'IsRobloxPlace': True,
    })
    return True


@ server_path("/login/negotiate.ashx")
@ server_path("/universes/validate-place-join")
def _(self: webserver_handler) -> bool:
    self.send_json(True)
    return True


@ server_path("/Setting/QuietGet/ClientAppSettings/")
def _(self: webserver_handler) -> bool:
    self.send_json(const.CLIENT_SETTINGS)
    return True


@ server_path("/asset-thumbnail/json")
def _(self: webserver_handler) -> bool:
    self.send_json({
        "Url": "",
        "Final": True,
        "SubstitutionType": 0,
    })
    return True


@ server_path("/Thumbs/GameIcon.ashx")
def _(self: webserver_handler) -> bool:
    with open('C:/Users/USERNAME/Documents/Projects/FilteringDisabled/OldRFD/Webserver/www/Thumbs/gameicon.ashx/img.png', 'rb') as f:
        self.send_data(f.read())
    return True


@ server_path("/v1/settings/application")
def _(self: webserver_handler) -> bool:
    self.send_json({"applicationSettings": {}})
    return True


@ server_path("/api.GetAllowedMD5Hashes/")
def _(self: webserver_handler) -> bool:
    self.send_json(const.ALLOWED_MD5_HASHES)
    return True


@ server_path("/api.GetAllowedSecurityVersions/")
def _(self: webserver_handler) -> bool:
    self.send_json({
        "data": self.server.roblox_version.security_versions(),
    })
    return True


@ server_path("/v1.1/Counters/BatchIncrement")
def _(self: webserver_handler) -> bool:
    self.send_json({})
    return True
