from web_server._logic import server_path, web_server_handler

from .data_transfer import _
from .load_assets import _
from .setup_player import _
from .setup_rcc import _
from .text_filter import _


@server_path("/")
def _(self: web_server_handler) -> bool:
    self.send_data('ÒÓ'.encode('utf-16'))
    return True
