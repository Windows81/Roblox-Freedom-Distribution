from web_server._logic import server_path, web_server_handler
import util.const

from . import (
    assets,
    avatar,
    badges,
    data_transfer,
    funds,
    gamepasses,
    groups,
    joinscript,
    persistence,
    player_info,
    save_place,
    setup_player,
    setup_rcc,
    text_filter,
)


@server_path("/")
def _(self: web_server_handler) -> bool:
    data_string = (
        'Roblox Freedom Distribution webserver %s [%s]' %
        (
            util.const.GIT_RELEASE_VERSION,
            self.game_config.game_setup.roblox_version.value[0],
        )
    )
    self.send_data(data_string.encode('utf-8'))
    return True
