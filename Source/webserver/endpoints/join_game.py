from webserver.logic import webserver_handler, server_path
import const


@server_path("/game/join.ashx")
def _(self: webserver_handler) -> bool:
    placeid = self.query.get("placeid", None)
    ip = self.query.get('ip', None)
    port = self.query.get('port', None)
    uid = self.query.get('id', 0)
    username = self.query.get('user', None)
    app = self.query.get('app', None)
    membership = self.query.get("membership", None)

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
    }, sign=True)
    return True


@server_path("/game/placelauncher.ashx")
def _(self: webserver_handler) -> bool:
    self.send_json({
        'jobId': 'Test',
        'status': 2,
        'joinScriptUrl': f"http://localhost/game/join.ashx?{self.urlsplit.query}",
        'authenticationUrl': 'http://localhost/login/negotiate.ashx',
        'authenticationTicket': '1',
        'message': None,
    })
    return True


@server_path("/marketplace/productinfo")
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


@server_path("/.127.0.0.1/game/load-place-info")
@server_path("/.127.0.0.1/game/load-place-info/")
def _(self: webserver_handler) -> bool:
    self.send_json({
        'CreatorId': 1,
        'CreatorType': 'User',
        'PlaceVersion': 1,
        'GameId': 123456,
        'IsRobloxPlace': True,
    })
    return True


@server_path("/login/negotiate.ashx")
def _(self: webserver_handler) -> bool:
    self.send_json(True)
    return True


@server_path("/Setting/QuietGet/ClientAppSettings/")
def _(self: webserver_handler) -> bool:
    self.send_json(const.CLIENT_SETTINGS)
    return True


@server_path("/api.GetAllowedMD5Hashes/")
def _(self: webserver_handler) -> bool:
    self.send_json(const.ALLOWED_MD5_HASHES)
    return True


@server_path("/api.GetAllowedSecurityVersions/")
def _(self: webserver_handler) -> bool:
    self.send_json({
        "data": self.server.version.security_versions(),
    })
    return True
