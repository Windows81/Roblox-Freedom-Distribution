from ..logic import webserver_handler, server_path
from ..assets import load_asset


@server_path("/asset")
@server_path("/asset/")
@server_path("/v1/asset")
@server_path("/.127.0.0.1/asset/")
def _(self: webserver_handler) -> bool:
    asset = load_asset(self.query['id'])
    if not asset:
        return

    self.send_data(asset)
    return True
