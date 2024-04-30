import launcher.routines._logic as logic
import web_server._main as _main
import config._main
import config._main
import dataclasses
import threading


@dataclasses.dataclass
class _arg_type(logic.arg_type):
    server_config: config._main.obj_type
    web_ports: list[logic.port] = dataclasses.field(default_factory=list)


class obj_type(logic.server_entry):
    server_config: config._main.obj_type
    httpds = list[_main.web_server._logic.web_server]()
    local_args: _arg_type

    def __add_server(self, web_port: logic.port, *args, **kwargs) -> None:
        try:
            # Unpacks the 'port' struct here because its usefulness is only in the 'launcher' supermodule.
            ht = _main.make_server(*args, **web_port.__dict__, **kwargs)
            th = threading.Thread(target=ht.serve_forever)
            self.threads.append(th)
            th.start()

        except PermissionError:
            print(
                'WARNING: web servers were unable to start at port %d.' %
                (web_port.port_num)
            )
            self.server_running = False

    def __add_servers(self, web_ports: list[logic.port], *args, **kwargs) -> None:
        hts = [
            _main.make_server(*args, port, **kwargs)
            for port in web_ports
        ]
        self.httpds.extend(hts)

        for ht in hts:
            th = threading.Thread(target=ht.serve_forever)
            self.threads.append(th)
            th.start()

    def process(self) -> None:
        self.server_running = True
        self.__add_servers(
            web_ports=self.local_args.web_ports,
            server_config=self.server_config,
        )

    def __del__(self) -> None:
        if not self.server_running:
            return
        for ht in self.httpds:
            ht.shutdown()


class arg_type(_arg_type):
    obj_type = obj_type
