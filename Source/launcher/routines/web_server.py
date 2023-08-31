import launcher.routines._logic as logic
import web_server._main as _main
import game_config._main
import game_config._main
import dataclasses
import threading


@dataclasses.dataclass
class _arg_type(logic.arg_type):
    server_config: game_config._main.obj_type
    web_ports: set[logic.port] = dataclasses.field(default_factory=set)


class obj_type(logic.server_entry):
    server_config: game_config._main.obj_type
    httpds = list[_main.web_server._logic.web_server]()
    local_args: _arg_type

    def __make_server(self, web_port: logic.port, *args, **kwargs) -> None:
        try:
            # We unpack the 'port' struct here because its usefulness is only in the 'launcher' supermodule.
            self.httpds.append(ht := _main.make_server(*args, **web_port.__dict__, **kwargs))
            self.threads.append(th := threading.Thread(target=ht.serve_forever))
            th.start()
        except PermissionError:
            print(f'WARNING: web server was unable to start at port {web_port.port_num}.')
            self.server_running = False

    def initialise(self) -> None:
        self.server_running = True
        for p in self.local_args.web_ports:
            self.__make_server(p, server_config=self.server_config)

    def __del__(self) -> None:
        if not self.server_running:
            return
        for ht in self.httpds:
            ht.shutdown()


class arg_type(_arg_type):
    obj_type = obj_type
