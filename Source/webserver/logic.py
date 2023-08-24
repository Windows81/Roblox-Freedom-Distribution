from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import ssl
from typing import Callable, Optional
import util.versions as versions
import util.const as const
from urllib import parse
import OpenSSL.crypto
import mimetypes
import base64
import enum
import json
import re
import os


class FunctionMode(enum.Enum):
    STATIC = 0
    REGEX = 1


SERVER_FUNCS = {m: dict[str, versions.version_holder]() for m in FunctionMode}


def server_path(path: str, regex: bool = False, min_version: int = 0):
    def inner(f: Callable[[BaseHTTPRequestHandler, Optional[re.Match]], bool]):
        dict_mode: dict = FunctionMode.REGEX if regex else FunctionMode.STATIC
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


class webserver(ThreadingHTTPServer):
    def __init__(
        self,
        server_address,
        roblox_version: versions.roblox = versions.roblox.v348,
        bind_and_activate=True,
    ) -> None:
        super().__init__(server_address, webserver_handler, bind_and_activate)
        self.roblox_version = roblox_version


class webserver_handler(BaseHTTPRequestHandler):
    default_request_version = "HTTP/1.1"
    is_valid_request: bool = False
    server: webserver

    def parse_request(self) -> bool:
        if not super().parse_request():
            return False

        self.is_valid_request = True
        self.sockname = self.request.getsockname()
        self.is_ssl = isinstance(self.connection, ssl.SSLSocket)
        self.domain = \
            'localhost'\
            if self.sockname[0] == '127.0.0.1'\
            else self.sockname[0]

        self.host = f'http{"s" if self.is_ssl else ""}://{self.domain}:{self.sockname[1]}'
        self.url = f'{self.host}{self.path}'
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
        return func[self.server.roblox_version](self, *a, **kwa)

    def __open_from_static(self) -> bool:
        func = SERVER_FUNCS[FunctionMode.STATIC].get(self.urlsplit.path, None)
        return self.__process_func(func)

    def __open_from_regex(self) -> bool:
        for pattern, func in SERVER_FUNCS[FunctionMode.REGEX].items():
            match = re.search(pattern, self.urlsplit.path)
            if not match:
                continue
            return self.__process_func(func)

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
