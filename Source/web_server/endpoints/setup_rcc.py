from web_server._logic import web_server_handler, server_path
import util.versions as versions
import util.const
import util.ssl


@server_path('/api.GetAllowedMD5Hashes/')
def _(self: web_server_handler) -> bool:
    self.send_json(util.const.ALLOWED_MD5_HASHES)
    return True


@server_path('/api.GetAllowedSecurityVersions/')
def _(self: web_server_handler) -> bool:
    self.send_json({
        'data': self.server.game_config.game_setup.roblox_version.security_versions(),
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


@server_path('/marketplace/productinfo')
def _(self: web_server_handler) -> bool:
    # Returns an error if the thing trying to be accessed isn't the place we're in.
    if self.query['assetId'] != str(util.const.DEFAULT_PLACE_ID):
        self.send_error(404)
        return True

    self.send_json({
        'AssetId': util.const.DEFAULT_PLACE_ID,
        'ProductId': 13831621,
        'Name': self.game_config.game_setup.title,
        'Description': self.game_config.game_setup.description,
        'AssetTypeId': 19,
        'Creator': {
            'Id': 1,
            'Name': self.game_config.game_setup.creator_name,
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


@server_path('/v1.1/Counters/BatchIncrement')
def _(self: web_server_handler) -> bool:
    self.send_json({})
    return True
