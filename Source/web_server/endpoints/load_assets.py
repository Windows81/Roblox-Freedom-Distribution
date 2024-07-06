from web_server._logic import web_server_handler, server_path
import util.const


@server_path("/asset")
@server_path("/asset/")
@server_path("/v1/asset")
@server_path("/v1/asset/")
@server_path("/.127.0.0.1/asset/")
def _(self: web_server_handler) -> bool:
    assets = self.server.game_config.asset_cache
    asset_id = assets.resolve_asset_query(self.query)

    if isinstance(asset_id, str):
        asset = assets.load_asset_str(asset_id)

    elif isinstance(asset_id, int):
        if (
            asset_id == util.const.DEFAULT_PLACE_ID
            and self.domain != 'localhost'
        ):
            self.send_error(
                403,
                "Server hosters don't tend to like exposing their place files.",
            )
            return True
        asset = assets.load_asset_num(asset_id)

    # Branch case for if the asset id was invalidly passed.
    # Returns false so that other `@server_path` functions can use it.
    else:
        return False

    if asset is None:
        self.send_error(404)
        return True

    self.send_data(asset)
    return True
