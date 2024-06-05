from web_server._logic import server_path, web_server_handler

from . import (
    data_transfer,
    load_assets,
    setup_player,
    setup_rcc,
    text_filter,
    player_info,
)


@server_path("/")
def _(self: web_server_handler) -> bool:
    self.send_data('ÒÓ'.encode('utf-16'))
    return True
