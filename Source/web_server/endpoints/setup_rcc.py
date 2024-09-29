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
    config = self.game_data_group.configs
    self.send_json({
        'data': config.game_setup.roblox_version.security_versions(),
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
    asset_id = int(self.query['assetId'])
    config = self.game_data_group.configs

    gamepass_library = config.remote_data.gamepasses
    metadata = config.server_core.metadata
    if asset_id in gamepass_library:
        gamepass_data = gamepass_library[asset_id]
        self.send_json({
            "PriceInRobux": gamepass_data.price,
            "MinimumMembershipLevel": 0,
            "TargetId": gamepass_data.id_num,
            "AssetId": gamepass_data.id_num,
            "ProductId": gamepass_data.id_num,
            "Name": gamepass_data.name,
            "Description": "",
            "AssetTypeId": "GamePass",
            "IsForSale": True,
            "IsPublicDomain": False,
            'Creator': {
                'Id': 1,
                'Name': metadata.creator_name,
                'CreatorType': 'User',
                'CreatorTargetId': 1
            },
        })
        return True

    # Returns an error if the thing trying to be accessed isn't the place we're in.
    if asset_id != util.const.PLACE_IDEN_CONST:
        self.send_error(404)
        return True

    self.send_json({
        'AssetId': util.const.PLACE_IDEN_CONST,
        'ProductId': 13831621,
        'Name': metadata.title,
        'Description': metadata.description,
        'AssetTypeId': 19,
        'Creator': {
            'Id': 1,
            'Name': metadata.creator_name,
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
