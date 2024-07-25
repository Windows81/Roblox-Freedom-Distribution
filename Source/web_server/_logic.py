from typing_extensions import Any, Callable
import util.versions as versions
import util.const as const
from urllib import parse
import OpenSSL.crypto
import http.server
import dataclasses
import mimetypes
import functools
import util.ssl
import base64
import config
import socket
import enum
import json
import ssl
import re
import os


@dataclasses.dataclass
class port_typ:
    def __hash__(self) -> int:
        return self.port_num
    port_num: int
    is_ssl: bool = True
    is_ipv6: bool = False


class func_mode(enum.Enum):
    STATIC = 0
    REGEX = 1


class holder(dict[versions.rōblox, Any]):
    def __add_pred(self, func: Callable[[int], bool], obj):
        for v in versions.rōblox:
            if not func(v.get_number()):
                continue
            super().__setitem__(v, obj)
        return obj

    def add_min(self, obj, min_version: int):
        return self.__add_pred(lambda n: n >= min_version, obj)

    def add_all(self, obj):
        return self.__add_pred(lambda n: True, obj)


@dataclasses.dataclass(frozen=True)
class server_func_key:
    mode: func_mode
    version: versions.rōblox
    path: str
    command: str


SERVER_FUNCS = dict[server_func_key, Callable]()


def server_path(
    path: str,
    regex: bool = False,
    versions: set[versions.rōblox] = set(versions.rōblox),
    commands: set[str] = {'POST', 'GET'}
):
    def inner(func):
        dict_mode = (
            func_mode.REGEX
            if regex
            else func_mode.STATIC
        )

        global SERVER_FUNCS
        SERVER_FUNCS |= {
            server_func_key(
                mode=dict_mode,
                version=version,
                path=path,
                command=command,
            ): func
            for version in versions
            for command in commands
        }

        return func
    return inner


def rbx_sign(data: bytes, key: bytes, prefix: bytes = b'--rbxsig') -> bytes:
    data = b'\r\n' + data
    key = b"-----BEGIN RSA PRIVATE KEY-----\n%s\n-----END RSA PRIVATE KEY-----" % key
    signature = OpenSSL.crypto.sign(
        OpenSSL.crypto.load_privatekey(
            OpenSSL.crypto.FILETYPE_PEM,
            key,
        ),
        data,
        'sha1',
    )
    return prefix + b"%" + base64.b64encode(signature) + b'%' + data


class web_server(http.server.ThreadingHTTPServer):
    def __init__(
        self,
        port: port_typ,
        game_config: config.obj_type,
        print_http_log: bool = False,
        *args, **kwargs,
    ) -> None:
        self.game_config = game_config
        self.data_transferer = game_config.data_transferer
        self.database = game_config.database

        self.is_ipv6 = port.is_ipv6
        self.address_family = socket.AF_INET6 if self.is_ipv6 else socket.AF_INET
        self.print_http_log = print_http_log

        super().__init__(
            ('', port.port_num),
            web_server_handler,
            *args, **kwargs,
        )


class web_server_ssl(web_server):
    ssl_mutable: util.ssl.ssl_mutable
    identities: set[str]

    def __init__(
        self,
        port: port_typ,
        *args, **kwargs,
    ) -> None:

        super().__init__(
            port,
            *args, **kwargs,
        )
        self.identities = {'::1', '127.0.0.1', 'localhost'}
        self.ssl_mutable = util.ssl.ssl_mutable()
        self.update_socket()

    def add_identities(self, *new_identities: str) -> None:
        old_len = len(self.identities)
        self.identities.update(new_identities)
        new_len = len(self.identities)
        if old_len == new_len:
            return
        self.update_socket()

    def update_socket(self) -> None:
        self.ssl_mutable.issue_cert(*self.identities)
        self.socket = self.ssl_mutable.get_ssl_context().wrap_socket(
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

        self.hostname = \
            f'http{"s" if isinstance(self.server, web_server_ssl) else ""}://' + \
            f'{self.domain}:{self.sockname[1]}'

        self.url = f'{self.hostname}{self.path}'
        self.url_split = parse.urlsplit(self.url)

        # Optimised for query values which may contain more than one of the same field.
        self.query_lists = parse.parse_qs(self.url_split.query)

        # Optimised for quick access for query indicies which only show up once.
        self.query = {
            i: v[0]
            for i, v in self.query_lists.items()
        }
        return True

    def handle_rcc_request(self) -> None:
        if self.__open_from_static():
            return
        if self.__open_from_regex():
            return
        if self.__open_from_file():
            return
        try:
            self.send_error(404)
        except ssl.SSLEOFError:
            pass

    def do_GET(self) -> None: return self.handle_rcc_request()
    def do_POST(self) -> None: return self.handle_rcc_request()
    def do_HEAD(self) -> None: return self.handle_rcc_request()
    def do_PATCH(self) -> None: return self.handle_rcc_request()
    def do_DELETE(self) -> None: return self.handle_rcc_request()

    def send_json(
        self,
        json_data,
        sign_prefix: bytes | None = None,
    ) -> None:
        byts = json.dumps(json_data).encode('utf-8')
        self.send_data(
            byts,
            content_type='application/json',
            sign_prefix=sign_prefix,
        )

    def send_data(
        self,
        byts: bytes,
        status: int = 200,
        content_type: str | None = None,
        sign_prefix: bytes | None = None,
    ) -> None:

        data = sign_prefix and rbx_sign(
            key=const.JOIN_GAME_SIGN_KEY,
            prefix=sign_prefix,
            data=byts,
        ) or byts

        self.send_response(status)
        if content_type:
            self.send_header('content-type', content_type)
        self.send_header('content-length', str(len(data)))
        try:
            self.end_headers()
            self.wfile.write(data)
        except ssl.SSLEOFError:
            # A `ssl.SSLEOFError` is likely thrown whenever a request is interrupted.
            pass

    def __open_from_static(self) -> bool:
        key = server_func_key(
            mode=func_mode.STATIC,
            version=self.game_config.game_setup.roblox_version,
            path=self.url_split.path,
            command=self.command,
        )

        func = SERVER_FUNCS.get(key, None)
        if func:
            return func(self)
        return False

    def __open_from_regex(self) -> bool:
        for key, func in SERVER_FUNCS.items():
            if key.mode != func_mode.REGEX:
                continue
            match = re.fullmatch(key.path, self.url_split.path)
            if match is None:
                continue
            return func(self, match)
        return False

    def __open_from_file(self) -> bool:
        return False
        # TODO: remove completely or find a new use for this piece of code.
        fn = os.path.realpath(os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            '../www', self.url_split.path,
        ))

        if "." not in fn.split(os.path.sep)[-1]:
            fn = os.path.join(fn, 'index.php')
        mime_type = mimetypes.guess_type(fn)[0]

        if os.path.exists(fn):
            self.send_header('content-type', mime_type)
            self.send_data(open(fn, "rb").read())
            return True

    def log_message(self, format, *args) -> None:
        if not self.server.print_http_log:
            return
        if not self.is_valid_request:
            return
        # if not self.requestline.startswith('\x16\x03'):
            # super().log_message(format, *args)
        print(self.url)
