# Standard library imports
import dataclasses
import threading
from typing import override

# Local application/library specific imports
import game_config as config
import game_config.structure
import logger
import web_server
import web_server._logic as web_server_logic
from . import _logic as logic


class obj_type(logic.server_entry):
    game_config: config.obj_type
    httpd: web_server_logic.web_server | None = None
    local_args: 'arg_type'

    @override
    def process(self) -> None:
        self.httpd = web_server.make_server(
            self.local_args.web_port,
            self.local_args.is_ssl,
            self.local_args.is_ipv6,
            self.game_config,
            self.local_args.server_mode,
            self.local_args.log_filter,
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


@dataclasses.dataclass
class arg_type(logic.arg_type):
    obj_type = obj_type

    web_port: int
    is_ipv6: bool
    is_ssl: bool

    game_config: game_config.obj_type
    server_mode: web_server_logic.server_mode
    log_filter: logger.filter.filter_type
