from web_server._logic import server_path, web_server_handler
import util.const

from . import (
    auth,
    assets,
    avatar,
    badges,
    data_transfer,
    funds,
    games_api,
    groups,
    image,
    join_data,
    marketplace,
    mobile,
    persistence,
    player_info,
    save_place,
    setup_player,
    setup_rcc,
    telemetry,
    text_filter,
    studio,
)


@server_path("/")
def _(self: web_server_handler) -> bool:
    if self.try_proxy_frontend(fallback_on_error=True):
        return True

    data_string = (
        'Roblox Freedom Distribution webserver %s [%s]' %
        (
            util.const.GIT_RELEASE_VERSION,
            self.game_config.game_setup.roblox_version.value[0],
        )
    )
    self.send_data(data_string.encode('utf-8'))
    return True
