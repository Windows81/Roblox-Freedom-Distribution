from web_server.logic import web_server_handler, server_path
from web_server.assets import load_asset


@server_path("/asset")
@server_path("/asset/")
@server_path("/v1/asset")
@server_path("/.127.0.0.1/asset/")
def _(self: web_server_handler) -> bool:
    try:
        aid = int(self.query['id'])
    except ValueError:
        return

    asset = load_asset(aid)
    if not asset:
        return

    self.send_data(asset)
    return True
