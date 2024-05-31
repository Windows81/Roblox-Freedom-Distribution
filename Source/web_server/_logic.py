import launcher.routines._logic as logic
import util.versions as versions
import dataclasses
import util.const as const
from urllib import parse
import config.structure
import OpenSSL.crypto
import config._main
import http.server
import mimetypes
import functools
import util.ssl
import base64
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


SERVER_FUNCS = {m: dict[str, versions.version_holder]() for m in func_mode}


def server_path(path: str, regex: bool = False, min_version: int = 0):
    def inner(f):
        dict_mode = func_mode.REGEX if regex else func_mode.STATIC
        SERVER_FUNCS[dict_mode].setdefault(
            path, versions.version_holder()).add_min(f, min_version)
        return f
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
        game_config: config._main.obj_type,
        print_http_log: bool = False,
        *args, **kwargs,
    ) -> None:
        self.game_config = game_config
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
        if not host:
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
        self.urlsplit = parse.urlsplit(self.url)
        self.query = {
            i: v[0]
            for i, v in parse.parse_qs(self.urlsplit.query).items()
        }
        return True

    def do_GET(self) -> None:
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

    def do_POST(self) -> None:
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
        self.end_headers()
        self.wfile.write(data)

    def __process_func(self, func, *args, **kwargs) -> bool:
        if not func:
            return False
        version_func = func.get(self.game_config.game_setup.roblox_version)
        if not version_func:
            return False
        return version_func(self, *args, **kwargs)

    def __open_from_static(self) -> bool:
        func = SERVER_FUNCS[func_mode.STATIC].get(self.urlsplit.path, None)
        return self.__process_func(func)

    def __open_from_regex(self) -> bool:
        for pattern, func in SERVER_FUNCS[func_mode.REGEX].items():
            match = re.search(pattern, self.urlsplit.path)
            if not match:
                continue
            return self.__process_func(func, match)
        return False

    def __open_from_file(self) -> bool:
        return False
        # TODO: remove completely or find a new use for this piece of code.
        fn = os.path.realpath(os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            '../www', self.urlsplit.path,
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
