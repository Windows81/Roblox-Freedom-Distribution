import ssl
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
SSL_CONTEXT = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
SSL_CONTEXT.load_cert_chain(
    certfile=f'{dir_path}/cert.cert',
    keyfile=f'{dir_path}/roblox.key',
)
