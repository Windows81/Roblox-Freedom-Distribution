import web_server._logic as web_server_logic
import web_server as web_server

from . import _logic as logic
import config.structure
import config
import config
import dataclasses
import threading


class obj_type(logic.server_entry):
    game_config: config.obj_type
    httpds = list[web_server_logic.web_server]()
    local_args: 'arg_type'

    def __run_servers(
        self,
        web_ports: list[web_server_logic.port_typ],
        game_config: config.obj_type,
        *args, **kwargs,
    ) -> None:
        hts = [
            web_server.make_server(
                *args, port, game_config, **kwargs)  # type: ignore
            for port in web_ports
        ]
        self.httpds.extend(hts)

        for ht in hts:
            th = threading.Thread(
                target=ht.serve_forever,
                daemon=True,
            )
            self.threads.append(th)
            th.start()

    def process(self) -> None:
        self.server_running = True
        self.__run_servers(
            web_ports=self.local_args.web_ports,
            print_http_log=self.local_args.verbose,
            game_config=self.game_config,
        )

    def __del__(self) -> None:
        if not self.server_running:
            return
        for ht in self.httpds:
            ht.shutdown()


@dataclasses.dataclass
class arg_type(logic.arg_type):
    obj_type = obj_type

    game_config: config.obj_type
    web_ports: list[web_server_logic.port_typ] = dataclasses.field(
        default_factory=list)
    verbose: bool = False
