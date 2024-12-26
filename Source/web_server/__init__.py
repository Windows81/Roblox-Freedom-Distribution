import web_server._logic as web_server_logic

# Make sure all API endpoints are working without taking anything therefrom.
from .endpoints import _


def make_server(
    port: web_server_logic.port_typ,
    *args,
    **kwargs,
) -> web_server_logic.web_server:
    if port.is_ssl:
        cls = web_server_logic.web_server_ssl
    else:
        cls = web_server_logic.web_server
    return cls(port, *args, **kwargs)
