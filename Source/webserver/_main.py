from server_ssl.main import SSL_CONTEXT
from .logic import webserver

# Make sure all API endpoints are working without taking anything therefrom.
from .endpoints._main import _


def make_server(port=80, is_ssl=False, *args, **kwargs) -> webserver:
    httpd = webserver(('', port), *args, **kwargs)
    if is_ssl:
        httpd.socket = SSL_CONTEXT.wrap_socket(
            httpd.socket,
            server_side=True,
        )
    return httpd
