
from http.server import ThreadingHTTPServer
from .handler import webserver_handler
import ssl
import os

# Make sure all API endpoints are working without taking anything therefrom.
from .endpoints.main import _


def make_httpd(port=80, is_ssl=False) -> ThreadingHTTPServer:
    httpd = ThreadingHTTPServer(('', port), webserver_handler)
    if is_ssl:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(
            certfile=f'{dir_path}/cert.cert',
            keyfile=f'{dir_path}/roblox.key',
        )
        httpd.socket = context.wrap_socket(
            httpd.socket,
            server_side=True,
        )
    return httpd
