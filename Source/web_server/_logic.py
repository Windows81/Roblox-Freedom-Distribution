from typing import Callable, Optional
import util.versions as versions
import util.const as const
from urllib import parse
import util.ssl_context
import OpenSSL.crypto
import config._main
import http.server
import mimetypes
import game.user
import base64
import socket
import enum
import json
import re
import os


class func_mode(enum.Enum):
    STATIC = 0
    REGEX = 1


SERVER_FUNCS = {m: dict[str, versions.version_holder]() for m in func_mode}


def server_path(path: str, regex: bool = False, min_version: int = 0):
    def inner(f: Callable[[http.server.BaseHTTPRequestHandler, Optional[re.Match]], bool]):
        dict_mode: dict = func_mode.REGEX if regex else func_mode.STATIC
        SERVER_FUNCS[dict_mode].setdefault(path, versions.version_holder()).add_min(f, min_version)
        return f
    return inner


def rbx_sign(data: bytes, key: bytes, prefix: bytes = b'--rbxsig') -> bytes:
    data = b'\r\n' + data
    key = f"-----BEGIN RSA PRIVATE KEY-----\n{key}\n-----END RSA PRIVATE KEY-----"
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
        server_address: tuple[str, int],
        server_config: config._main.obj_type,
        bind_and_activate=True,
        is_ssl: bool = False,
    ) -> None:
        super().__init__(
            server_address,
            web_server_handler,
            bind_and_activate,
        )
        self.game_config = server_config
        self.users = game.user.user_dict(self.game_config)
        self.is_ssl = is_ssl

        if is_ssl:
            ssl_context = util.ssl_context.get_ssl_context()
            self.socket = ssl_context.wrap_socket(
                self.socket,
                server_side=True,
            )


class web_server_handler(http.server.BaseHTTPRequestHandler):
    default_request_version = "HTTP/1.1"
    sockname: tuple[str, int]
    request: socket.socket
    server: web_server

    def parse_request(self) -> bool:
        self.is_valid_request = False
        if not super().parse_request():
            return False
        self.is_valid_request = True
        self.game_config = self.server.game_config

        self.sockname = self.headers.get('Host').split(':')
        self.domain = \
            'localhost'\
            if self.sockname[0] == '127.0.0.1'\
            else self.sockname[0]

        self.hostname = \
            f'http{"s" if self.server.is_ssl else ""}://' + \
            f'{self.domain}:{self.sockname[1]}'

        self.url = f'{self.hostname}{self.path}'
        self.urlsplit = parse.urlsplit(self.url)
        self.query = {i: v[0] for i, v in parse.parse_qs(self.urlsplit.query).items()}
        return True

    def do_GET(self) -> None:
        if self.__open_from_static():
            return
        if self.__open_from_regex():
            return
        if self.__open_from_file():
            return
        self.send_error(404)

    def do_POST(self) -> None:
        if self.__open_from_static():
            return
        if self.__open_from_regex():
            return
        if self.__open_from_file():
            return
        self.send_error(404)

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
            key=const.JOIN_GAME_PRIVATE_KEY,
            prefix=sign_prefix,
            data=byts,
        ) or byts

        self.send_response(status)
        if content_type:
            self.send_header('content-type', content_type)
        self.send_header('content-length', len(data))
        self.end_headers()
        self.wfile.write(data)

    def __process_func(self, func, *a, **kwa):
        if not func:
            return False
        return func[self.game_config.game_setup.roblox_version](self, *a, **kwa)

    def __open_from_static(self) -> bool:
        func = SERVER_FUNCS[func_mode.STATIC].get(self.urlsplit.path, None)
        return self.__process_func(func)

    def __open_from_regex(self) -> bool:
        for pattern, func in SERVER_FUNCS[func_mode.REGEX].items():
            match = re.search(pattern, self.urlsplit.path)
            if not match:
                continue
            return self.__process_func(func, match)

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
        if not const.HTTPD_SHOW_LOGS:
            return
        if not self.is_valid_request:
            return
        # if not self.requestline.startswith('\x16\x03'):
            # super().log_message(format, *args)
        print(self.url)
