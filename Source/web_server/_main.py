import web_server._logic

# Make sure all API endpoints are working without taking anything therefrom.
from .endpoints._main import _

import launcher.routines._logic as logic


def make_server(port: logic.port, *args, **kwargs) -> web_server._logic.web_server:
    cls = web_server._logic.web_server_ssl if port.is_ssl else web_server._logic.web_server
    return cls(port, *args, **kwargs)
