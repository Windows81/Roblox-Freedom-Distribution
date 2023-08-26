from webserver.logic import server_path, webserver_handler
from .text_filter import _
from .load_assets import _
from .join_game import _


@server_path("/")
def _(self: webserver_handler) -> bool:
    self.send_data('ÒÓ'.encode('utf-16'))
    return True
