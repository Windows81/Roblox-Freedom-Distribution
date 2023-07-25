from server_ssl.main import SSL_CONTEXT
from .logic import bridge


def make_server(port=80, is_ssl=False, *args, **kwargs) -> bridge:
    httpd = bridge(('', port), *args, **kwargs)
    if is_ssl:
        httpd.socket = SSL_CONTEXT.wrap_socket(
            httpd.socket,
            server_side=True,
        )
    return httpd
