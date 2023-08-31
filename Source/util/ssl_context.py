# Much of this script is from https://github.com/begleysm/ipwatch/blob/master/ipgetter.py.
import functools
import time
import urllib.request
import http.cookiejar
import util.resource
import trustme
import random
import socket
import ssl
import re

# https://raw.githubusercontent.com/begleysm/ipwatch/master/servers.json [2023-08-26]
IP_SERVER_LIST = [
    "http://ip.dnsexit.com",
    "http://ifconfig.me/ip",
    "https://ipecho.net/plain",
    "http://checkip.dyndns.org/plain",
    "https://www.ipanywhere.com/",
    "https://www.my-ip-address.co/",
    "https://myexternalip.com/raw",
    "https://canyouseeme.org/",
    "http://www.trackip.net/",
    "http://icanhazip.com/",
    "https://www.ipchicken.com/",
    "http://whatsmyip.net/",
    "http://www.lawrencegoetz.com/programs/ipinfo/",
    "https://ip-lookup.net/",
    "http://ipgoat.com/",
    "http://www.myipnumber.com/my-ip-address.asp",
    "http://formyip.com/",
    "https://check.torproject.org/",
    "http://www.displaymyip.com/",
    "https://www.geodatatool.com/",
    "https://www.whatsmydns.net/whats-my-ip-address.html",
    "http://checkip.dyndns.com/",
    "http://www.ip-adress.eu/",
    "https://www.infosniper.net/",
    "https://wtfismyip.com/text",
    "http://httpbin.org/ip",
    "https://diagnostic.opendns.com/myip",
    "http://checkip.amazonaws.com",
    "https://api.ipify.org",
    "https://v4.ident.me",
]


def fetch(server) -> str | None:
    '''
        This function gets your IP from a specific server.
        '''
    url = None
    cj = http.cookiejar.CookieJar()
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    opener = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(cj),
        urllib.request.HTTPSHandler(context=ctx),
    )
    opener.addheaders = list({
        'User-agent': "Mozilla/5.0 (X11; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0",
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        'Accept-Language': "en-US,en;q=0.5",
    }.items())

    try:
        url = opener.open(server, timeout=4)
        content = url.read()
        try:
            content = content.decode('UTF-8')
        except UnicodeDecodeError:
            content = content.decode('ISO-8859-1')

        match = re.search(
            '(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' +
            '(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' +
            '(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' +
            '(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)',
            content,
        )
        if not match:
            return None

        address = match.group(0)
        if len(address) == 0:
            return None
        return address

    except Exception:
        return None

    finally:
        if url:
            url.close()


def get_external_ips() -> list[str]:
    for _ in range(7):
        server = random.choice(IP_SERVER_LIST)
        address = fetch(server)
        if address != None:
            return [address]
    return []


# From https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib
def get_local_ips() -> list[str]:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
            # Doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            return [s.getsockname()[0]]
        except Exception:
            return []


def get_path(*paths: str):
    return util.resource.retr_full_path(util.resource.dir_type.SSL, *paths)


CLIENT_PEM_PATH = get_path('client.pem')
SERVER_PEM_PATH = get_path('server.pem')
SERVER_KEY_PATH = get_path('server.key')


@functools.cache
def init_cert_auth() -> trustme.CA:
    ca = trustme.CA()
    cert: trustme.LeafCert = ca.issue_cert(
        *get_external_ips(),
        *get_local_ips(),
        '127.0.0.1',
        'localhost',
    )

    # Write the certificate and private key the server should use.
    cert.private_key_pem.write_to_path(path=SERVER_KEY_PATH)
    with open(SERVER_PEM_PATH, mode='w') as f:
        f.truncate()
    for blob in cert.cert_chain_pems:
        blob.write_to_path(path=SERVER_PEM_PATH, append=True)

    # Write the certificate the client should trust.
    ca.cert_pem.write_to_path(path=CLIENT_PEM_PATH)
    return ca


@functools.cache
def get_ssl_context() -> ssl.SSLContext:
    init_cert_auth()
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(
        certfile=SERVER_PEM_PATH,
        keyfile=SERVER_KEY_PATH,
    )
    return ssl_context


@functools.cache
def get_client_cert() -> bytes:
    init_cert_auth()
    with open(util.ssl_context.CLIENT_PEM_PATH, 'rb') as f:
        return f.read()
