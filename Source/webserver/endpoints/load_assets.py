from webserver.handler import webserver_handler, server_path
import webserver.assets


@server_path("/asset")
@server_path("/asset/")
@server_path("/.127.0.0.1/asset/")
def _(self: webserver_handler) -> bool:
    asset = webserver.assets.load_asset(self.query['id'])
    if not asset:
        return

    self.send_data(asset)
    return True
