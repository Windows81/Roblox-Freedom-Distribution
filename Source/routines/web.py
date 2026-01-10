# Standard library imports
import dataclasses
import threading
from typing import override

# Local application/library specific imports
import web_server._logic as web_server_logic
from . import _logic as logic
import web_server
import logger


@dataclasses.dataclass(kw_only=True, unsafe_hash=True)
class obj_type(logic.gameconfig_entry, logic.loggable_entry):
    web_port: int
    is_ipv6: bool
    is_ssl: bool

    server_mode: web_server_logic.server_mode
    httpd: web_server_logic.web_server | None = None

    def __post_init__(self) -> None:
        self.threads: list[threading.Thread] = []

    @override
    def process(self) -> None:
        self.httpd = web_server.make_server(
            self.web_port,
            self.is_ssl,
            self.is_ipv6,
            self.game_config,
            self.server_mode,
            self.log_filter,
        )

        th = threading.Thread(
            target=self.httpd.serve_forever,
            daemon=True,
        )
        self.threads.append(th)
        th.start()

    @override
    def stop(self) -> None:
        if self.httpd is None:
            return
        self.httpd.shutdown()
        super().stop()
