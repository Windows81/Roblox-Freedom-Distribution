import webserver.logic

# Make sure all API endpoints are working without taking anything therefrom.
from .endpoints.main import _


def make_server(port_num=80, *args, **kwargs) -> webserver.logic.webserver:
    return webserver.logic.webserver(('', port_num), *args, **kwargs)
