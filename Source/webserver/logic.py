from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
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


def rbx_sign(data: bytes, key: bytes) -> bytes:
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
    return b"--rbxsig%" + base64.b64encode(signature) + b'%' + data


class webserver(ThreadingHTTPServer):
    def __init__(
        self,
        server_address,
        roblox_version: versions.Version = versions.Version.v348,
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
        self.urlsplit = parse.urlsplit(self.path)
        self.query = {i: v[0] for i, v in parse.parse_qs(self.urlsplit.query).items()}
        sockname = self.request.getsockname()
        self.host = f'{sockname[0]}:{sockname[1]}'
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

    def send_json(self, j, sign=False) -> None:
        byts = json.dumps(j).encode('utf-8')
        self.send_data(byts, content_type='application/json', sign=sign)

    def send_data(self, byts: bytes, status: int = 200, content_type: str | None = None, sign=False) -> None:
        data = sign and rbx_sign(byts, const.JOIN_GAME_PRIVATE_KEY) or byts

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
        print(self.host, self.path)
