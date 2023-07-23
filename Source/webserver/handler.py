from OpenSSL.crypto import sign, load_privatekey, FILETYPE_PEM
from http.server import BaseHTTPRequestHandler
from typing import Callable, Optional
from urllib import parse
import mimetypes
import base64
import const
import json
import re
import os


REGEX_FUNCS = {}
STATIC_FUNCS = {}


def server_path(path: str, regex: bool = False):
    def inner(f: Callable[[BaseHTTPRequestHandler, Optional[re.Match]], bool]):
        (regex and REGEX_FUNCS or STATIC_FUNCS)[path] = f
        return f
    return inner


def rbx_sign(data: bytes, key: bytes) -> bytes:
    data = b'\r\n' + data
    key = f"-----BEGIN RSA PRIVATE KEY-----\n{key}\n-----END RSA PRIVATE KEY-----"
    signature = sign(load_privatekey(FILETYPE_PEM, key), data, 'sha1')
    return b"--rbxsig%" + base64.b64encode(signature) + b'%' + data


class webserver_handler(BaseHTTPRequestHandler):
    default_request_version = "HTTP/1.1"

    def parse_request(self) -> bool:
        if not super().parse_request():
            return False
        self.urlsplit = parse.urlsplit(self.path)
        self.query = {i: v[0] for i, v in parse.parse_qs(self.urlsplit.query).items()}
        sockname = self.request.getsockname()
        self.host = f'{sockname[0]}:{sockname[1]}'
        return True

    def do_GET(self) -> None:
        if self._open_from_static():
            return
        if self._open_from_regex():
            return
        if self._open_from_file():
            return
        self.send_error(404)

    def do_POST(self) -> None:
        if self._open_from_static():
            return
        if self._open_from_regex():
            return
        if self._open_from_file():
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

    def _open_from_static(self) -> bool:
        func = STATIC_FUNCS.get(self.urlsplit.path, None)
        return func and func(self) or False

    def _open_from_regex(self) -> bool:
        for pattern, func in REGEX_FUNCS.items():
            match = re.search(pattern, self.urlsplit.path)
            if not match:
                continue
            return func(self, match)

    def _open_from_file(self) -> bool:
        fn = os.path.realpath(os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            '../www', self.urlsplit.path,
        ))

        if "." not in fn.split(os.path.sep)[-1]:
            fn = os.path.join(fn, "index.php")
        mime_type = mimetypes.guess_type(fn)[0]

        if os.path.exists(fn):
            self.send_header('content-type', mime_type)
            self.send_data(open(fn, "rb").read())
            return True

    def log_message(self, format, *args) -> None:
        if not const.HTTPD_SHOW_LOGS:
            return
        if not self.requestline.startswith('\x16\x03'):
            super().log_message(format, *args)
