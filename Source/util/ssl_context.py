import util.resource
import ssl

SSL_CONTEXT = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
SSL_CONTEXT.load_cert_chain(
    certfile=util.resource.get_full_path(util.resource.dir_type.SSL, 'cert.cert'),
    keyfile=util.resource.get_full_path(util.resource.dir_type.SSL, 'roblox.key'),
)
