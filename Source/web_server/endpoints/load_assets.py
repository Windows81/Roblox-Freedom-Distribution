from web_server._logic import web_server_handler, server_path
import assets._main


@server_path("/asset")
@server_path("/asset/")
@server_path("/v1/asset")
@server_path("/v1/asset/")
@server_path("/.127.0.0.1/asset/")
def _(self: web_server_handler) -> bool:
    asset_id = next(
        i for i in [
            assets._main.resolve_asset_id(
                self.query.get('id', None)),
            assets._main.resolve_asset_version_id(
                self.query.get('assetversionid', None)),
        ]
        if i != None
    )
    if not asset_id:
        return False

    asset = assets._main.load_asset(asset_id)
    if not asset:
        return False

    self.send_data(asset)
    return True
