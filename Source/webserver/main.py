import webserver.logic
import util.ssl_context

# Make sure all API endpoints are working without taking anything therefrom.
from .endpoints.main import _


def make_server(port_num=80, is_ssl=False, *args, **kwargs) -> webserver.logic.webserver:
    httpd = webserver.logic.webserver(('', port_num), *args, **kwargs)
    if is_ssl:
        httpd.socket = util.ssl_context.SSL_CONTEXT.wrap_socket(
            httpd.socket,
            server_side=True,
        )
    return httpd
