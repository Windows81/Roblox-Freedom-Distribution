from web_server._logic import server_path, web_server_handler

from . import (
    assets,
    avatar,
    data_transfer,
    persistence,
    setup_player,
    setup_rcc,
    text_filter,
    player_info,
    save_place,
    joinscript,
    badges,
)


@server_path("/")
def _(self: web_server_handler) -> bool:
    self.send_data('ÒÓ'.encode('utf-16'))
    return True
