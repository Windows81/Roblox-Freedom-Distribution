# Standard library imports
import dataclasses
import enum
import functools
import http.server
import json
import os
import re
import select
import socket
import ssl
import traceback
import urllib.error
import urllib.request
from urllib import parse

# Typing imports
from typing import Any, Callable, override

# Local application imports
import util.versions as versions
import game_config
import logger


VERSION_TYPE = next(
    value
    for value in vars(versions).values()
    if isinstance(value, type) and issubclass(value, enum.Enum)
)


class func_mode(enum.Enum):
    STATIC = 0
    REGEX = 1


class server_mode(enum.Enum):
    RCC = 0
    STUDIO = 1


@dataclasses.dataclass(frozen=True)
class server_func_key:
    mode: func_mode
    version: VERSION_TYPE
    path: str
    command: str


SERVER_FUNCS = dict[server_func_key, Callable[..., Any]]()
DEFAULT_COMMANDS = {'POST', 'GET'}
ALL_VERSIONS = set(VERSION_TYPE)
HOP_BY_HOP_HEADERS = {
    'connection',
    'keep-alive',
    'proxy-authenticate',
    'proxy-authorization',
    'te',
    'trailer',
    'transfer-encoding',
    'upgrade',
}


def server_path(
    path: str,
    regex: bool = False,
    versions: set[VERSION_TYPE] = ALL_VERSIONS,
    commands: set[str] = DEFAULT_COMMANDS
):
    def inner(func):
        match regex:
            case True:
                dict_mode = func_mode.REGEX
            case False:
                dict_mode = func_mode.STATIC

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


class web_server(http.server.ThreadingHTTPServer):
    def __init__(
        self,
        port: int,
        is_ipv6: bool,
        game_config: game_config.obj_type,
        server_mode: server_mode,
        log_filter: logger.obj_type,
        frontend_proxy: str | None = None,
        *args, **kwargs,
    ) -> None:
        self.game_config = game_config
        self.data_transferer = game_config.data_transferer
        self.storage = game_config.storage
        self.server_mode = server_mode
        self.logger = log_filter
        self.is_ipv6 = is_ipv6
        self.frontend_proxy = (
            frontend_proxy.rstrip('/')
            if frontend_proxy is not None
            else None
        )
        self.address_family = (
            socket.AF_INET6
            if self.is_ipv6
            else socket.AF_INET
        )

        self.logger.log(
            (
                f"{self.logger.bcolors.BOLD}[TCP %d %s]{self.logger.bcolors.ENDC}: " +
                "initialising webserver"
            ) % (
                port,
                'IPv6' if self.is_ipv6 else 'IPv4',
            ),
            context=logger.log_context.PYTHON_SETUP,
        )

        super().__init__(
            ('', port),
            web_server_handler,
            *args, **kwargs,
        )


class web_server_ssl(web_server):
    def get_context(self):
        if not os.path.isfile(self.cert_path):
            raise FileNotFoundError(
                f"SSL certificate file was not found: {self.cert_path}"
            )
        if not os.path.isfile(self.key_path):
            raise FileNotFoundError(
                f"SSL private key file was not found: {self.key_path}"
            )

        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.load_cert_chain(
            certfile=self.cert_path,
            keyfile=self.key_path,
        )
        ctx.check_hostname = False
        return ctx

    def __init__(
        self,
        *args,
        cert_path: str = 'server.pem',
        key_path: str = 'server-key.pem',
        **kwargs,
    ) -> None:
        self.cert_path = cert_path
        self.key_path = key_path
        super().__init__(*args, **kwargs)
        self.socket = self.get_context().wrap_socket(
            self.socket,
            server_side=True,
        )


class web_server_handler(http.server.BaseHTTPRequestHandler):
    default_request_version = "HTTP/1.1"
    request: socket.socket
    server: web_server

    @functools.cache
    def read_content(self) -> bytes:
        length = int(self.headers.get('content-length', -1))
        return self.rfile.read(length)

    @override
    def parse_request(self) -> bool:
        self.is_valid_request = False
        self.is_frontend_proxy_request = False
        if not super().parse_request():
            return False

        host_header: str | None = self.headers.get('Host')
        if host_header is None:
            return False

        domain_str, port_str = host_header.rsplit(':', 1)
        self.port_num = int(port_str)

        if domain_str == '127.0.0.1':
            self.domain = 'localhost'
        elif domain_str.startswith('['):
            # Format IPv6 addresses.
            self.domain = domain_str[1:-1]
        else:
            self.domain = domain_str

        self.hostname = (
            f'http{"s" if isinstance(self.server, web_server_ssl) else ""}://' +
            f'{self.domain}:{self.port_num}'
        )

        self.is_valid_request = True
        self.game_config = self.server.game_config

        # Some endpoints should only allow the RCC to do stuff.
        # TODO: use a proper allow-listing system.
        self.is_privileged = self.domain == 'localhost'

        self.url = f'{self.hostname}{self.path}'
        assert isinstance(self.url, str)
        self.url_split = parse.urlsplit(self.url)

        # Optimised for query values which may contain more than one of the same field.
        self.query_lists = parse.parse_qs(self.url_split.query)

        # Optimised for quick access for query indicies which only show up once.
        self.query = {
            i: v[0]
            for i, v in self.query_lists.items()
        }
        return True

    def handle_request(self) -> None:
        should_print_exception = True

        try:
            if self.__open_from_static():
                return
            if self.__open_from_regex():
                return
            if self.try_proxy_frontend():
                return
            self.send_error(404)
            return

        except ssl.SSLEOFError:
            should_print_exception = False
        except ConnectionResetError:
            should_print_exception = False
        except ConnectionAbortedError:
            should_print_exception = False

        if should_print_exception:
            error_text = traceback.format_exc().encode('utf-8')
            if self.is_frontend_proxy_request:
                self.__log_frontend_proxy_error(error_text)
            else:
                self.server.logger.log(
                    error_text,
                    context=logger.log_context.WEB_SERVER,
                    is_error=True,
                )

    def do_GET(self) -> None: return self.handle_request()
    def do_POST(self) -> None: return self.handle_request()
    def do_HEAD(self) -> None: return self.handle_request()
    def do_PATCH(self) -> None: return self.handle_request()
    def do_DELETE(self) -> None: return self.handle_request()

    def send_json(
        self,
        json_data,
        status: int | None = 200,
        prefix: bytes = b'',
    ) -> None:
        byts = prefix + json.dumps(json_data).encode('utf-8')
        self.send_data(
            byts,
            content_type='application/json',
            status=status,
        )

    def send_data(
        self,
        text: bytes | str,
        status: int | None = 200,
        content_type: str | None = None,
    ) -> None:
        if isinstance(text, str):
            text = text.encode('utf-8')
        assert isinstance(text, bytes)

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

    def try_proxy_frontend(
        self,
        fallback_on_error: bool = False,
    ) -> bool:
        proxy_url = self.server.frontend_proxy
        if proxy_url is None:
            return False

        target_url = (
            f'{proxy_url}{self.path}'
            if self.path.startswith('/')
            else f'{proxy_url}/{self.path}'
        )
        if self.__is_frontend_websocket_request():
            return self.__proxy_frontend_websocket(
                target_url,
                fallback_on_error=fallback_on_error,
            )

        request_headers = {
            key: value
            for key, value in self.headers.items()
            if key.lower() not in HOP_BY_HOP_HEADERS | {'content-length', 'host'}
        }
        request_headers['Host'] = parse.urlsplit(proxy_url).netloc

        request_body = None
        content_length = self.headers.get('content-length')
        if content_length is not None and int(content_length) > 0:
            request_body = self.read_content()

        request = urllib.request.Request(
            target_url,
            data=request_body,
            headers=request_headers,
            method=self.command,
        )
        is_stream_request = self.__is_frontend_stream_request()
        ssl_context = None
        if target_url.startswith('https://'):
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE

        try:
            if is_stream_request:
                response_ctx = urllib.request.urlopen(
                    request,
                    context=ssl_context,
                )
            else:
                response_ctx = urllib.request.urlopen(
                    request,
                    timeout=10,
                    context=ssl_context,
                )

            with response_ctx as response:
                if is_stream_request:
                    self.is_frontend_proxy_request = True
                    self.__stream_proxy_response(
                        response.status,
                        response.headers.items(),
                        response,
                    )
                else:
                    self.is_frontend_proxy_request = True
                    self.__send_proxy_response(
                        response.status,
                        response.headers.items(),
                        response.read(),
                    )
                return True
        except urllib.error.HTTPError as response:
            self.is_frontend_proxy_request = True
            self.__send_proxy_response(
                response.code,
                response.headers.items(),
                response.read(),
            )
            return True
        except Exception:
            if fallback_on_error:
                return False
            self.is_frontend_proxy_request = True
            self.send_error(
                502,
                f'Failed to reach frontend proxy at {proxy_url}.',
            )
            return True

    def __is_frontend_websocket_request(self) -> bool:
        return self.headers.get('Upgrade', '').lower() == 'websocket'

    def __is_frontend_stream_request(self) -> bool:
        accept_header = self.headers.get('Accept', '')
        return 'text/event-stream' in accept_header

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
        return func(self)

    def __open_from_regex(self) -> bool:
        for key, func in SERVER_FUNCS.items():
            if key.mode != func_mode.REGEX:
                continue
            match = re.fullmatch(key.path, self.url_split.path)
            if match is None:
                continue
            if key.version != self.game_config.game_setup.roblox_version:
                continue

            try:
                return func(self, match)
            except Exception:
                continue
        return False

    def __send_proxy_response(
        self,
        status: int,
        headers,
        body: bytes,
    ) -> None:
        content_length = None

        self.send_response(status)
        for header, value in headers:
            header_lower = header.lower()
            if header_lower in HOP_BY_HOP_HEADERS:
                continue
            if header_lower == 'content-length':
                content_length = value
                continue
            self.send_header(header, value)

        if self.command == 'HEAD':
            self.send_header('content-length', content_length or '0')
            self.end_headers()
            return

        self.send_header('content-length', content_length or str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def __stream_proxy_response(
        self,
        status: int,
        headers,
        response,
    ) -> None:
        headers = list(headers)
        is_event_stream = any(
            header.lower() == 'content-type' and
            value.lower().startswith('text/event-stream')
            for header, value in headers
        )

        self.send_response(status)
        for header, value in headers:
            header_lower = header.lower()
            if header_lower in HOP_BY_HOP_HEADERS | {'content-length'}:
                continue
            self.send_header(header, value)

        if self.command == 'HEAD':
            self.end_headers()
            return

        self.send_header('transfer-encoding', 'chunked')
        self.end_headers()

        try:
            while True:
                if is_event_stream:
                    chunk = response.readline()
                elif hasattr(response, 'read1'):
                    chunk = response.read1(64 * 1024)
                else:
                    chunk = response.read(8 * 1024)
                if not chunk:
                    break
                self.wfile.write(f'{len(chunk):X}\r\n'.encode('ascii'))
                self.wfile.write(chunk)
                self.wfile.write(b'\r\n')
                self.wfile.flush()
            self.wfile.write(b'0\r\n\r\n')
            self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError, ssl.SSLEOFError):
            return

    def __proxy_frontend_websocket(
        self,
        target_url: str,
        fallback_on_error: bool = False,
    ) -> bool:
        upstream_socket = None

        try:
            target = parse.urlsplit(target_url)
            target_host = target.hostname
            if target_host is None:
                raise ValueError(f'Invalid frontend proxy target: {target_url}')

            target_port = target.port or (443 if target.scheme == 'https' else 80)
            target_path = parse.urlunsplit((
                '',
                '',
                target.path or '/',
                target.query,
                '',
            ))

            upstream_socket = socket.create_connection(
                (target_host, target_port),
                timeout=10,
            )
            if target.scheme == 'https':
                ssl_context = ssl.create_default_context()
                ssl_context.check_hostname = False
                ssl_context.verify_mode = ssl.CERT_NONE
                upstream_socket = ssl_context.wrap_socket(
                    upstream_socket,
                    server_hostname=target_host,
                )

            upstream_request = '\r\n'.join([
                f'{self.command} {target_path} HTTP/1.1',
                f'Host: {target.netloc}',
                *[
                    f'{key}: {value}'
                    for key, value in self.headers.items()
                    if key.lower() != 'host'
                ],
                '',
                '',
            ]).encode('utf-8')
            upstream_socket.sendall(upstream_request)

            response_head, response_tail = self.__read_proxy_response_head(upstream_socket)
            self.is_frontend_proxy_request = True
            self.connection.sendall(response_head)
            if response_tail:
                self.connection.sendall(response_tail)

            if b' 101 ' not in response_head.split(b'\r\n', 1)[0]:
                self.close_connection = True
                return True

            self.close_connection = True
            self.__proxy_socket_tunnel(self.connection, upstream_socket)
            return True
        except Exception:
            if upstream_socket is not None:
                upstream_socket.close()
            if fallback_on_error:
                return False
            self.send_error(
                502,
                f'Failed to establish frontend websocket proxy at {target_url}.',
            )
            return True

    def __read_proxy_response_head(
        self,
        upstream_socket: socket.socket,
    ) -> tuple[bytes, bytes]:
        response = bytearray()
        while b'\r\n\r\n' not in response:
            chunk = upstream_socket.recv(4096)
            if not chunk:
                break
            response.extend(chunk)

        head, separator, tail = response.partition(b'\r\n\r\n')
        return (bytes(head + separator), bytes(tail))

    def __proxy_socket_tunnel(
        self,
        client_socket: socket.socket,
        upstream_socket: socket.socket,
    ) -> None:
        sockets = [client_socket, upstream_socket]
        try:
            while True:
                readable, _, _ = select.select(sockets, [], [], 60)
                if not readable:
                    continue

                for source in readable:
                    target = (
                        upstream_socket
                        if source is client_socket
                        else client_socket
                    )
                    try:
                        payload = source.recv(64 * 1024)
                    except ssl.SSLWantReadError:
                        continue

                    if not payload:
                        return
                    target.sendall(payload)
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError, ssl.SSLEOFError, OSError):
            return
        finally:
            upstream_socket.close()

    def __log_frontend_proxy_error(self, text: bytes) -> None:
        log_filter = self.server.logger
        if not log_filter.web_logs.errors:
            return
        log_filter.action(
            (
                f'{log_filter.bcolors.FAIL}[Frontend Proxy Error]\n%s{log_filter.bcolors.ENDC}'
            ) % (
                text.decode('utf-8'),
            )
        )

    @override
    def log_message(self, format, *args) -> None:
        if not self.is_valid_request:

            return
        log_filter = self.server.logger
        log_text = (
            "%s{ %-5s}%s %s"
        ) % (
            log_filter.bcolors.BOLD,
            self.command,
            log_filter.bcolors.ENDC,
            self.url.rstrip('\r\n'),
        )

        if self.is_frontend_proxy_request:
            if not log_filter.web_logs.urls:
                return
            log_filter.action(
                f'{log_filter.bcolors.HEADER}[Frontend Proxy]{log_filter.bcolors.ENDC} {log_text}'
            )
            return

        log_filter.log(
            log_text,
            context=logger.log_context.WEB_SERVER,
            is_error=False,
        )
