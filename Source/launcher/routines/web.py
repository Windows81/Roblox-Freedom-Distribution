import web_server._logic as web_server_logic
import web_server

from . import _logic as logic
import game_config.structure
import game_config as config
import dataclasses
import threading
import logger


class obj_type(logic.server_entry):
    game_config: config.obj_type
    httpds: list[web_server_logic.web_server]
    local_args: 'arg_type'

    def __run_servers(
        self,
        web_ports: list[web_server_logic.port_typ],
        game_config: config.obj_type,
        *args, **kwargs,
    ) -> None:
        self.httpds = [
            web_server.make_server(
                port,
                game_config,
                self.local_args.server_mode,
                self.local_args.log_filter,
                *args,
                **kwargs,
            )
            for port in web_ports
        ]

        for ht in self.httpds:
            th = threading.Thread(
                target=ht.serve_forever,
                daemon=True,
            )
            self.threads.append(th)
            th.start()

    def process(self) -> None:
        self.__run_servers(
            web_ports=self.local_args.web_ports,
            game_config=self.game_config,
        )

    def stop(self) -> None:
        if self.httpds is None:
            return
        for ht in self.httpds:
            ht.shutdown()


@dataclasses.dataclass
class arg_type(logic.arg_type):
    obj_type = obj_type

    game_config: game_config.obj_type
    server_mode: web_server_logic.server_mode
    web_ports: list[web_server_logic.port_typ] = dataclasses.field(
        default_factory=list,
    )
    log_filter: logger.filter.filter_type = logger.DEFAULT_FILTER
