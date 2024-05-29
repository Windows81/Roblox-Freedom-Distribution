import web_server._logic
import config.structure
import config._main

# Make sure all API endpoints are working without taking anything therefrom.
from .endpoints._main import _

import launcher.routines._logic as logic


def make_server(
    port: logic.port,
    game_config: config._main.obj_type,
    *args,
    **kwargs,
) -> web_server._logic.web_server:
    cls = web_server._logic.web_server_ssl if port.is_ssl else web_server._logic.web_server
    return cls(port, game_config, * args, **kwargs)
