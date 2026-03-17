# Standard library imports
import dataclasses
import socket
import ssl
import threading
import time
import unittest
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import override

# Local application imports
import game_config
import logger
import routines
import util.resource
from routines import web


def get_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(('127.0.0.1', 0))
        return sock.getsockname()[1]


class frontend_handler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    @override
    def do_GET(self) -> None:
        if (
            self.path.startswith('/_next/webpack-hmr') and
            self.headers.get('Upgrade', '').lower() == 'websocket'
        ):
            self.send_response_only(101, 'Switching Protocols')
            self.send_header('Upgrade', 'websocket')
            self.send_header('Connection', 'Upgrade')
            self.send_header('Sec-WebSocket-Accept', 'test-accept')
            self.end_headers()
            self.wfile.flush()

            payload = self.connection.recv(64 * 1024)
            if payload:
                self.connection.sendall(payload)
            return

        if self.path.startswith('/stream'):
            self.send_response(200)
            self.send_header('content-type', 'text/event-stream; charset=utf-8')
            self.send_header('cache-control', 'no-cache')
            self.send_header('x-proxy-target', 'frontend')
            self.end_headers()
            self.wfile.write(b'data: one\n\n')
            self.wfile.flush()
            time.sleep(1.5)
            self.wfile.write(b'data: two\n\n')
            self.wfile.flush()
            return

        body = f'frontend:{self.path}'.encode('utf-8')
        self.send_response(200)
        self.send_header('content-type', 'text/plain; charset=utf-8')
        self.send_header('x-proxy-target', 'frontend')
        self.send_header('content-length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    @override
    def log_message(self, format, *args) -> None:
        return


class TestWebProxy(unittest.TestCase):
    @override
    @classmethod
    def setUpClass(cls) -> None:
        cls.frontend_port = get_free_port()
        cls.web_port = get_free_port()
        cls.logged_lines: list[str] = []
        cls.test_logger = dataclasses.replace(
            logger.PRINT_REASONABLE,
            web_logs=logger.filter.filter_type_web(
                urls=True,
                errors=True,
            ),
            bcolors=logger.bc.BCOLORS_INVISIBLE,
            action=cls.logged_lines.append,
        )
        cls.frontend_server = ThreadingHTTPServer(
            ('127.0.0.1', cls.frontend_port),
            frontend_handler,
        )
        cls.frontend_thread = threading.Thread(
            target=cls.frontend_server.serve_forever,
            daemon=True,
        )
        cls.frontend_thread.start()

        cls.routine = routines.routine(
            web.obj_type(
                web_port=cls.web_port,
                logger=cls.test_logger,
                game_config=game_config.obj_type(
                    data_dict={
                        'server_core': {'place_file': {'rbxl_uri': 'dummy.rbxl'}},
                    },
                    base_dir=util.resource.retr_full_path(util.resource.dir_type.WORKING_DIR),
                ),
                server_mode=web.SERVER_MODE_TYPE.RCC,
                is_ipv6=False,
                is_ssl=True,
                frontend_proxy=f'http://127.0.0.1:{cls.frontend_port}',
            ),
        )
        time.sleep(1)

        cls.ssl_context = ssl.create_default_context()
        cls.ssl_context.check_hostname = False
        cls.ssl_context.verify_mode = ssl.CERT_NONE

    @override
    @classmethod
    def tearDownClass(cls) -> None:
        cls.routine.stop()
        cls.frontend_server.shutdown()
        cls.frontend_server.server_close()

    @classmethod
    def read_url(cls, path: str) -> tuple[int, str, str]:
        with urllib.request.urlopen(
            f'https://127.0.0.1:{cls.web_port}{path}',
            context=cls.ssl_context,
            timeout=5,
        ) as response:
            return (
                response.status,
                response.headers['x-proxy-target'],
                response.read().decode('utf-8'),
            )

    def test_root_is_forwarded_to_frontend(self) -> None:
        status, proxy_target, body = self.read_url('/')
        self.assertEqual(status, 200)
        self.assertEqual(proxy_target, 'frontend')
        self.assertEqual(body, 'frontend:/')

    def test_unknown_path_is_forwarded_to_frontend(self) -> None:
        status, proxy_target, body = self.read_url('/app/dashboard')
        self.assertEqual(status, 200)
        self.assertEqual(proxy_target, 'frontend')
        self.assertEqual(body, 'frontend:/app/dashboard')

    def test_event_stream_is_forwarded_without_buffering(self) -> None:
        request = urllib.request.Request(
            f'https://127.0.0.1:{self.web_port}/stream',
            headers={'Accept': 'text/event-stream'},
        )
        start = time.perf_counter()
        with urllib.request.urlopen(
            request,
            context=self.ssl_context,
            timeout=5,
        ) as response:
            first_chunk = response.read(11)
            elapsed = time.perf_counter() - start

            self.assertEqual(response.status, 200)
            self.assertEqual(response.headers['x-proxy-target'], 'frontend')
            self.assertEqual(response.headers['transfer-encoding'], 'chunked')
            self.assertEqual(first_chunk.decode('utf-8'), 'data: one\n\n')
            self.assertLess(elapsed, 1.0)

    def test_websocket_upgrade_is_tunneled(self) -> None:
        request_bytes = (
            f'GET /_next/webpack-hmr HTTP/1.1\r\n'
            f'Host: 127.0.0.1:{self.web_port}\r\n'
            'Upgrade: websocket\r\n'
            'Connection: Upgrade\r\n'
            'Sec-WebSocket-Key: test-key\r\n'
            'Sec-WebSocket-Version: 13\r\n'
            '\r\n'
        ).encode('utf-8')

        with socket.create_connection(('127.0.0.1', self.web_port), timeout=5) as raw_socket:
            with self.ssl_context.wrap_socket(
                raw_socket,
                server_hostname='127.0.0.1',
            ) as client_socket:
                client_socket.sendall(request_bytes)
                response_head = bytearray()
                while b'\r\n\r\n' not in response_head:
                    response_head.extend(client_socket.recv(4096))

                self.assertIn(b'101 Switching Protocols', response_head)
                self.assertIn(b'Upgrade: websocket', response_head)

                payload = b'hello-through-tunnel'
                client_socket.sendall(payload)
                echoed = client_socket.recv(len(payload))
                self.assertEqual(echoed, payload)

    def test_frontend_proxy_uses_dedicated_log_tag(self) -> None:
        self.logged_lines.clear()
        self.read_url('/frontend-log-check')

        self.assertTrue(
            any('[Frontend Proxy]' in line for line in self.logged_lines),
        )
