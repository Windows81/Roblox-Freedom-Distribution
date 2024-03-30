# Much of this script is from https://github.com/begleysm/ipwatch/blob/master/ipgetter.py.
import functools
import os
import urllib.request
import http.cookiejar
import util.resource
import trustme
import random
import socket
import ssl
import re

IPV4_SERVER_LIST = [
    "http://ipv4.icanhazip.com/",
    "https://v4.ident.me",
]

IPV6_SERVER_LIST = [
    "http://ipv6.icanhazip.com/",
    "https://v6.ident.me",
]


def fetch(server) -> str | None:
    '''
    This function gets your IP address from a specific server.
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

        return content
        match = re.search(
            r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' +
            r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' +
            r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' +
            r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)',
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


def get_external_ips(server_list: list[str]) -> list[str]:
    for _ in range(7):
        server = random.choice(server_list)
        address = fetch(server)
        if address != None:
            return [address.rstrip()]
    return []


# From https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib
def get_local_ips(mode: socket.AddressFamily, addr: tuple[str, int]) -> list[str]:
    with socket.socket(mode, socket.SOCK_DGRAM) as s:
        try:
            # Address doesn't have to be reachable.
            s.connect(addr)
            return [s.getsockname()[0]]
        except Exception:
            return []


def get_path(*paths: str) -> str:
    return util.resource.retr_full_path(util.resource.dir_type.SSL, *paths)


class ssl_mutable:
    CONTEXT_COUNT = 0

    def __init__(self) -> None:
        self.ca = trustme.CA()

        suffix = f'{ssl_mutable.CONTEXT_COUNT:03d}'
        self.client_pem_path = get_path(f'client{suffix}.pem')
        self.server_pem_path = get_path(f'server{suffix}.pem')
        self.server_key_path = get_path(f'server{suffix}.key')

        ssl_mutable.CONTEXT_COUNT += 1

    def issue_cert(self, *identities: str) -> trustme.LeafCert:
        cert: trustme.LeafCert = self.ca.issue_cert(*identities)

        try:
            os.remove(self.server_pem_path)
        except Exception:
            pass

        # Writes the certificate that the server should use.
        for blob in cert.cert_chain_pems:
            blob.write_to_path(path=self.server_pem_path, append=True)

        try:
            os.remove(self.server_key_path)
        except Exception:
            pass

        # Writes the private key that the server should use.
        cert.private_key_pem.write_to_path(
            path=self.server_key_path, append=True)

        try:
            os.remove(self.client_pem_path)
        except Exception:
            pass

        # Writes the certificate that the client should trust.
        self.ca.cert_pem.write_to_path(
            path=self.client_pem_path)

        return cert

    def get_client_cert(self) -> bytes:
        with open(self.client_pem_path, 'rb') as f:
            return f.read()

    def get_ssl_context(self) -> ssl.SSLContext:
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_context.load_cert_chain(
            certfile=self.server_pem_path,
            keyfile=self.server_key_path,
        )
        return ssl_context
