import web_server._logic as web_server_logic
import game_config.structure
import game_config

# Make sure all API endpoints are working without taking anything therefrom.
from .endpoints import _


def make_server(
    port: web_server_logic.port_typ,
    game_config: game_config.obj_type,
    *args,
    **kwargs,
) -> web_server_logic.web_server:
    print(
        "[TCP %d %s]: initialising webserver" %
        (port.port_num, 'IPv6' if port.is_ipv6 else 'IPv4',),
    )
    cls = web_server_logic.web_server_ssl if port.is_ssl else web_server_logic.web_server
    return cls(port, game_config, *args, **kwargs)
