import web_server._logic

# Make sure all API endpoints are working without taking anything therefrom.
from .endpoints._main import _


def make_server(port_num=80, is_ssl=False, *args, **kwargs) -> web_server._logic.web_server:
    return (is_ssl and web_server._logic.web_server_ssl or web_server._logic.web_server)(('', port_num), *args, **kwargs)
