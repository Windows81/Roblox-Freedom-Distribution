from web_server._logic import web_server_handler, server_path
import util.const


@server_path("/asset")
@server_path("/asset/")
@server_path("/v1/asset")
@server_path("/v1/asset/")
@server_path("/.127.0.0.1/asset/")
def _(self: web_server_handler) -> bool:
    assets = self.server.game_config.asset_cache
    asset_redirects = self.server.game_config.remote_data.asset_redirects

    # Paramater can either be `id` or `assetversionid`.
    asset_id = assets.resolve_asset_query(self.query)

    asset_redirect = asset_redirects.get(asset_id)

    if (
        asset_id == util.const.PLACE_ID_CONST
        and self.domain != 'localhost'
    ):
        self.send_error(
            403,
            "Server hosters don't tend to like exposing their place files.  " +
            "Ask them if they'd be willing to lend this one to you.",
        )
        return True

    asset = assets.load_asset(asset_id)
    if asset is None:
        self.send_error(404)
        return True

    self.send_data(asset)
    return True


@server_path('/ownership/hasasset', commands={'GET'})
def _(self: web_server_handler) -> bool:
    '''
    Typically used to check if players own specific catalogue items.
    There are no current plans to implement catalogue APIs in RFD.
    Collective ownership it is...
    '''
    self.send_json('true')
    return True
