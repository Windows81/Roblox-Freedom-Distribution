import launcher.routines.logic as logic
import webserver.main as main
import launcher.gameconfig
import dataclasses
import threading


@dataclasses.dataclass
class port:
    def __hash__(self) -> int:
        return self.port_num
    port_num: int
    is_ssl: bool


@dataclasses.dataclass
class _argtype(logic.subparser_argtype):
    server_config: launcher.gameconfig.configtype
    web_ports: set[port] = dataclasses.field(default_factory=set)


class webserver(logic.server_entry):
    server_config: launcher.gameconfig.configtype
    httpds = list[main.webserver.logic.webserver]()
    local_args: _argtype

    def __make_server(self, port_num: int = 80, *args, **kwargs) -> None:
        try:
            self.httpds.append(ht := main.make_server(port_num, *args, **kwargs))
            self.threads.append(th := threading.Thread(target=ht.serve_forever))
            th.start()
        except PermissionError:
            print(f'WARNING: webserver was unable to start at port {port_num}.')
            self.server_running = False

    def initialise(self) -> None:
        self.server_running = True
        for p in self.local_args.web_ports:
            self.__make_server(
                **p.__dict__,
                roblox_version=self.config.place_setup.roblox_version,
            )

    def __del__(self) -> None:
        if not self.server_running:
            return
        for ht in self.httpds:
            ht.shutdown()


class argtype(_argtype):
    obj_type = webserver
