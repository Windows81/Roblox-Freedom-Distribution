# Much of this script is from https://github.com/begleysm/ipwatch/blob/master/ipgetter.py.
import functools
import urllib.request
import http.cookiejar

import cryptography
import cryptography.x509.oid
import util.resource
import trustme
import random
import socket
import ssl
import re

from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, ec
from cryptography.hazmat.primitives.serialization import (
    PrivateFormat, NoEncryption
)
from cryptography.x509.oid import ExtendedKeyUsageOID, NameOID
from cryptography.hazmat.primitives.serialization import Encoding
from cryptography.hazmat.primitives.serialization import load_pem_private_key

IPV4_SERVER_LIST = [
    "http://ipv4.icanhazip.com/",
    "https://v4.ident.me",
]

IPV6_SERVER_LIST = [
    "http://ipv6.icanhazip.com/",
    "https://v6.ident.me",
]

CERTIFICATE_AUTHORITY = trustme.CA()
PRIVATE_KEY: ec.EllipticCurvePrivateKey = ec.generate_private_key(
    ec.SECP256R1()),  # type: ignore


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


CLIENT_PEM_PATH = get_path('client.pem')
SERVER_PEM_PATH = get_path('server.pem')
SERVER_KEY_PATH = get_path('server.key')


def issue_cert(
    *identities: str,
) -> trustme.LeafCert:

    ski_ext = CERTIFICATE_AUTHORITY._certificate.extensions.get_extension_for_class(
        x509.SubjectKeyIdentifier)
    aki = x509.AuthorityKeyIdentifier.from_issuer_subject_key_identifier(
        ski_ext.value)

    cert = (
        trustme._cert_builder_common(
            trustme._name(
                "Testing cert #" + trustme.random_text(),
            ),
            CERTIFICATE_AUTHORITY._certificate.subject,
            PRIVATE_KEY.public_key(),
        )
        .add_extension(
            x509.BasicConstraints(ca=False, path_length=None),
            critical=True,
        )
        .add_extension(aki, critical=False)
        .add_extension(
            x509.SubjectAlternativeName(
                [trustme._identity_string_to_x509(
                    ident) for ident in identities]
            ),
            critical=True,
        )
        .add_extension(
            x509.KeyUsage(
                digital_signature=True,
                content_commitment=False,
                key_encipherment=True,
                data_encipherment=False,
                key_agreement=False,
                key_cert_sign=False,
                crl_sign=False,
                encipher_only=False,
                decipher_only=False),
            critical=True
        )
        .add_extension(
            x509.ExtendedKeyUsage([
                cryptography.x509.oid.ExtendedKeyUsageOID.CLIENT_AUTH,
                cryptography.x509.oid.ExtendedKeyUsageOID.SERVER_AUTH,
                cryptography.x509.oid.ExtendedKeyUsageOID.CODE_SIGNING,
            ]),
            critical=True
        )
        .sign(
            private_key=CERTIFICATE_AUTHORITY._private_key,
            algorithm=hashes.SHA256(),
        )
    )

    return trustme.LeafCert(
        PRIVATE_KEY.private_bytes(
            Encoding.PEM,
            PrivateFormat.TraditionalOpenSSL,
            NoEncryption(),
        ),
        cert.public_bytes(Encoding.PEM),
        [],
    )


def init_cert_auth(identities) -> trustme.CA:
    ca = trustme.CA()
    cert: trustme.LeafCert = ca.issue_cert(
        *get_external_ips(IPV4_SERVER_LIST),
        *get_external_ips(IPV6_SERVER_LIST),
        *get_local_ips(socket.AF_INET, ('10.255.255.255', 1)),
        *get_local_ips(socket.AF_INET6, ('2001:db8::', 1)),
        '127.0.0.1',
        '::1',
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


def get_client_cert(web_server_handler) -> bytes:
    init_cert_auth()
    with open(CLIENT_PEM_PATH, 'rb') as f:
        return f.read()
