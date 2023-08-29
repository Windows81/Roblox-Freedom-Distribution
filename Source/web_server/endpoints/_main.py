from web_server.logic import server_path, web_server_handler
from .text_filter import _
from .load_assets import _
from .game_setup import _
from .game_join import _


@server_path("/")
def _(self: web_server_handler) -> bool:
    self.send_data('ÒÓ'.encode('utf-16'))
    return True
