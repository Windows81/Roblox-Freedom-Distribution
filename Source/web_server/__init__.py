import web_server._logic as web_server_logic

# Make sure all API endpoints are working without taking anything therefrom.
from .endpoints import _


def make_server(
    port: int,
    *args,
    **kwargs,
) -> web_server_logic.web_server:
    cls = web_server_logic.web_server
    return cls(port, *args, **kwargs)
