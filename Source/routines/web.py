# Standard library imports
import dataclasses
import threading
from typing import override

# Local application/library specific imports
import web_server._logic as web_server_logic
from . import _logic as logic
import util.const
import web_server

SERVER_MODE_TYPE = web_server_logic.server_mode


@dataclasses.dataclass(kw_only=True, unsafe_hash=True)
class obj_type(logic.gameconfig_entry, logic.loggable_entry):
    web_port: int = util.const.RFD_DEFAULT_PORT
    is_ipv6: bool
    is_ssl: bool

    server_mode: SERVER_MODE_TYPE
    httpd: web_server_logic.web_server | None = None

    def __post_init__(self) -> None:
        super().__post_init__()
        self.threads: list[threading.Thread] = []

    @override
    def process(self) -> None:
        super().process()
        self.httpd = web_server.make_server(
            self.web_port,
            self.is_ssl,
            self.is_ipv6,
            self.game_config,
            self.server_mode,
            self.logger,
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
        self.httpd.server_close()
        self.httpd = None
        super().stop()
