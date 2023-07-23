from webserver.handler import server_path, webserver_handler
from .load_assets import _
from .join_game import _


@server_path("/")
def _(self: webserver_handler) -> bool:
    self.send_response(200)
    self.wfile.write('ÒÓ'.encode('utf-16'))
    return True
