# Source is taken from https://github.com/tuwid/darkc0de-old-stuff/blob/76f002efe42dce80a1f5be7870650cd2a8ead43e/BladeProxy.py.

from http.server import BaseHTTPRequestHandler, HTTPServer, ThreadingHTTPServer
from socketserver import ThreadingMixIn
import urllib.parse
import select
import socket
import re

__version__ = "1.0"
encode_way = 0
# send_way = 0


class bridge_handler(BaseHTTPRequestHandler):
    __base = BaseHTTPRequestHandler
    __base_handle = __base.handle

    server_version = "BladeProxy/" + __version__
    rbufsize = 0

    def handle(self):
        (ip, port) = self.client_address
        if hasattr(self, 'allowed_clients') and ip not in self.allowed_clients:
            self.raw_requestline = self.rfile.readline()
            if self.parse_request():
                self.send_error(403)
        else:
            self.__base_handle()

    def _connect_to(self, netloc, soc):
        i = netloc.find(':')
        if i >= 0:
            host_port = (netloc[:i], int(netloc[i + 1:]))
        else:
            host_port = (netloc, 80)
        try:
            soc.connect(host_port)
        except socket.error as arg:
            try:
                msg = arg[1]
            except:
                msg = arg
            self.send_error(404, msg)
            return 0
        return 1

    def do_CONNECT(self):
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            if self._connect_to(self.path, soc):
                self.log_request(200)
                self.wfile.write('\r\n'.join([
                    f"{self.protocol_version} 200 Connection established",
                    f"Proxy-agent: {self.version_string()}",
                    "", "",
                ]))
                self._read_write(soc, 300)
        finally:
            soc.close()
            self.connection.close()

    def select_encode(self, s: str) -> str:
        if encode_way == 1:  # asc_encode
            return self.asc_encode(s)
        elif encode_way == 2:  # unicode_encode
            return self.unicode_encode(s)
        elif encode_way == 3:  # halfper_encode
            return self.halfper_encode(s)
        elif encode_way == 0:  # do not encode
            return s

    def do_encode(self, s: str):
        return s

    def asc_encode(self, s):
        def ss(s): return ''.join(map(lambda c: "%%%X" % ord(c), s))
        return ss(s)

    def unicode_encode(self, s) -> str:
        def ss(s): return ''.join(map(lambda c: "%%u00%X" % ord(c), s))
        return ss(s)

    def halfper_encode(self, s) -> str:
        def ss(s): return ''.join(map(lambda c: "%%%%%%%c" % c, s))
        return ss(s)

    def do_POST(self) -> None:
        (scm, netloc, path, params, query, fragment) = urllib.parse.urlparse(self.path, 'http')

        if self.command == 'POST' and not self.headers.has_key('content-length'):
            self.send_error(400, "Missing Content-Length for POST method")

        length = int(self.headers.get('content-length', 0))
        # print 'lenth is'+ self.headers['content-length']
        if length > 0:
            content = self.do_encode(self.rfile.read(length))
            self.headers['content-length'] = repr(len(content))

        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            if self._connect_to(netloc, soc):
                self.log_request()
                soc.send("%s %s %s\r\n" % (
                    self.command,
                    urllib.parse.urlunparse(('', '', path, params, '', '')),
                    self.request_version,
                ))
                self.headers['Connection'] = 'close'
                del self.headers['Proxy-Connection']
                for key_val in self.headers.items():
                    soc.send("%s: %s\r\n" % key_val)
                soc.send("\r\n")
                soc.send(content)
                self._read_write(soc)
        finally:
            soc.close()
            self.connection.close()

    def do_GET(self) -> None:
        (scm, netloc, path, params, query, fragment) = urllib.parse.urlparse(
            self.path, 'http')
        if query:
            query = self.do_encode(query)

        if scm != 'http' or fragment or not netloc:
            self.send_error(400, "bad url %s" % self.path)
            return
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            if self._connect_to(netloc, soc):
                self.log_request()
                soc.send("%s %s %s\r\n" % (
                    self.command,
                    urllib.parse.urlunparse(('', '', path, params, query, '')),
                    self.request_version,
                ))
                self.headers['Connection'] = 'close'
                del self.headers['Proxy-Connection']
                for key_val in self.headers.items():
                    soc.send("%s: %s\r\n" % key_val)
                soc.send("\r\n")
                self._read_write(soc)
        finally:
            soc.close()
            self.connection.close()

    def _read_write(self, soc, max_idling=20):
        iw = [self.connection, soc]
        ow = []
        count = 0
        while 1:
            count += 1
            (ins, _, exs) = select.select(iw, ow, iw, 3)
            if exs:
                break
            if ins:
                for i in ins:
                    if i is soc:
                        out = self.connection
                    else:
                        out = soc
                    data = i.recv(8192)
                    if data:
                        out.send(data)
                        count = 0
            if count == max_idling:
                break

    do_HEAD = do_GET,
    do_PUT = do_GET,
    do_DELETE = do_GET,


class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    pass
