# Standard library imports
import base64
import dataclasses
import enum
import functools
import http.server
import json
import re
import socket
import ssl
import tempfile
import traceback
from urllib import parse

# Typing imports
from typing import Any, Callable, override

# Local application imports
import game_config
import logger
import logger.bcolors
import util.const as const
import util.versions as versions

import trustme

# Cryptography imports
from cryptography.hazmat.primitives import hashes, padding, serialization
from cryptography.hazmat.backends import default_backend



class func_mode(enum.Enum):
    STATIC = 0
    REGEX = 1


class server_mode(enum.Enum):
    RCC = 0
    STUDIO = 1


@dataclasses.dataclass(frozen=True)
class server_func_key:
    mode: func_mode
    version: versions.rōblox
    path: str
    command: str


SERVER_FUNCS = dict[server_func_key, Callable[..., Any]]()
DEFAULT_COMMANDS = {'POST', 'GET'}
ALL_VERSIONS = set(versions.rōblox)


def server_path(
    path: str,
    regex: bool = False,
    versions: set[versions.rōblox] = ALL_VERSIONS,
    commands: set[str] = DEFAULT_COMMANDS
):
    def inner(func):
        dict_mode = (
            func_mode.REGEX
            if regex
            else func_mode.STATIC
        )

        SERVER_FUNCS.update({
            server_func_key(
                mode=dict_mode,
                version=version,
                path=path,
                command=command,
            ): func
            for version in versions
            for command in commands
        })

        return func
    return inner


def rbx_sign(data: bytes, key: bytes, prefix: bytes = b'--rbxsig') -> bytes:
    data = b'\r\n' + data
    key = b"-----BEGIN RSA PRIVATE KEY-----\n%s\n-----END RSA PRIVATE KEY-----" % key
    private_key = serialization.load_pem_private_key(
        key, None, default_backend())
    signature = private_key.sign(   # type: ignore[reportAttributeAccessIssue]
        data,
        padding.PKCS1v15(),  # type: ignore[reportCallIssue]
        hashes.SHA1(),  # type: ignore[reportCallIssue]
    )
    return prefix + b"%" + base64.b64encode(signature) + b'%' + data


class web_server(http.server.ThreadingHTTPServer):
    def __init__(
        self,
        port: int,
        is_ipv6: bool,
        game_config: game_config.obj_type,
        server_mode: server_mode,
        log_filter: logger.filter.filter_type,
        *args, **kwargs,
    ) -> None:
        self.game_config = game_config
        self.data_transferer = game_config.data_transferer
        self.storage = game_config.storage
        self.server_mode = server_mode
        self.log_filter = log_filter
        self.is_ipv6 = is_ipv6
        self.address_family = (
            socket.AF_INET6
            if self.is_ipv6
            else socket.AF_INET
        )

        logger.log(
            (
                f"{log_filter.bcolors.BOLD}[TCP %d %s]{log_filter.bcolors.ENDC}: " +
                "initialising webserver"
            ) % (
                port,
                'IPv6' if self.is_ipv6 else 'IPv4',
            ),
            context=logger.log_context.PYTHON_SETUP,
            filter=log_filter,
        )

        super().__init__(
            ('', port),
            web_server_handler,
            *args, **kwargs,
        )


class web_server_ssl(web_server):
    def get_context(self):
        self.tmp_cert = tempfile.NamedTemporaryFile(delete_on_close=False)
        self.tmp_key = tempfile.NamedTemporaryFile(delete_on_close=False)

        auth = trustme.CA()
        cert = auth.issue_cert('localhost')
        for i, blob in enumerate(cert.cert_chain_pems):
            blob.write_to_path(
                path=self.tmp_cert.name,
                append=(i > 0),
            )
        cert.private_key_pem.write_to_path(
            path=self.tmp_key.name,
            append=False,
        )

        self.tmp_cert.close()
        self.tmp_key.close()
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.load_cert_chain(
            certfile=self.tmp_cert.name,
            keyfile=self.tmp_key.name,
        )
        ctx.check_hostname = False
        return ctx

    def __init__(
        self,
        *args, **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.socket = self.get_context().wrap_socket(
            self.socket,
            server_side=True,
        )


class web_server_handler(http.server.BaseHTTPRequestHandler):
    default_request_version = "HTTP/1.1"
    sockname: tuple[str, int]
    request: socket.socket
    server: web_server

    @functools.cache
    def read_content(self) -> bytes:
        length = int(self.headers.get('content-length', -1))
        return self.rfile.read(length)

    @override
    def parse_request(self) -> bool:
        self.is_valid_request = False
        if not super().parse_request():
            return False

        host: str | None = self.headers.get('Host')
        if host is None:
            return False

        self.is_valid_request = True
        self.game_config = self.server.game_config

        host_part, port_part = host.rsplit(':', 1)
        self.sockname = (host_part, int(port_part))

        if host_part == '127.0.0.1':
            self.domain = 'localhost'
        else:
            self.domain = host_part

        if host_part.startswith('['):
            self.ip_addr = host_part[1:-1]
        else:
            self.ip_addr = host_part

        self.hostname = (
            f'http{"s" if isinstance(self.server, web_server_ssl) else ""}://' +
            f'{self.domain}:{self.sockname[1]}'
        )

        # Some endpoints should only allow the RCC to do stuff.
        # TODO: use a proper allow-listing system.
        self.is_privileged = self.domain == 'localhost'

        self.url = f'{self.hostname}{self.path}'
        assert isinstance(self.url, str)
        self.url_split = parse.urlsplit(self.url)

        # Optimised for query values which may contain more than one of the
        # same field.
        self.query_lists = parse.parse_qs(self.url_split.query)

        # Optimised for quick access for query indicies which only show up
        # once.
        self.query = {
            i: v[0]
            for i, v in self.query_lists.items()
        }
        return True

    def handle_request(self) -> None:
        try:
            if self.__open_from_static():
                return
            if self.__open_from_regex():
                return
            self.send_error(404)
        except ssl.SSLError:
            pass
        except ConnectionResetError:
            pass

    def do_GET(self) -> None: return self.handle_request()
    def do_POST(self) -> None: return self.handle_request()
    def do_HEAD(self) -> None: return self.handle_request()
    def do_PATCH(self) -> None: return self.handle_request()
    def do_DELETE(self) -> None: return self.handle_request()

    def send_json(
        self,
        json_data,
        status: int | None = 200,
        sign_prefix: bytes | None = None,
    ) -> None:
        byts = json.dumps(json_data).encode('utf-8')
        self.send_data(
            byts,
            content_type='application/json',
            sign_prefix=sign_prefix,
            status=status,
        )

    def send_data(
        self,
        text: bytes | str,
        status: int | None = 200,
        content_type: str | None = None,
        sign_prefix: bytes | None = None,
    ) -> None:
        if isinstance(text, str):
            text = text.encode('utf-8')
        assert isinstance(text, bytes)

        text = sign_prefix and rbx_sign(
            key=const.JOIN_GAME_SIGN_KEY,
            prefix=sign_prefix,
            data=text,
        ) or text

        # If `status` is None, we can add headers before calling `send_data`.
        if status is not None:
            self.send_response(status)
        if content_type:
            self.send_header('content-type', content_type)
        self.send_header('content-length', str(len(text)))
        self.end_headers()
        self.wfile.write(text)

    def send_redirect(self, url: str) -> None:
        self.send_response(301)
        self.send_header("Location", url)
        self.end_headers()

    def __open_from_static(self) -> bool:
        key = server_func_key(
            mode=func_mode.STATIC,
            version=self.game_config.game_setup.roblox_version,
            path=self.url_split.path,
            command=self.command,
        )

        func = SERVER_FUNCS.get(key)
        if func is None:
            return False
        try:
            return func(self)
        except ssl.SSLEOFError:
            return False
        except ConnectionResetError:
            return False
        except Exception as _:
            logger.log(
                traceback.format_exc().encode('utf-8'),
                context=logger.log_context.WEB_SERVER,
                filter=self.server.log_filter,
            )
            return False

    def __open_from_regex(self) -> bool:
        for key, func in SERVER_FUNCS.items():
            if key.mode != func_mode.REGEX:
                continue
            match = re.fullmatch(key.path, self.url_split.path)
            if match is None:
                continue
            try:
                return func(self, match)
            except Exception:
                continue
        return False

    @override
    def log_message(self, format, *args) -> None:
        if not self.is_valid_request:
            return
        logger.log(
            self.url.rstrip('\r\n').encode('utf-8'),
            context=logger.log_context.WEB_SERVER,
            filter=self.server.log_filter,
        )
