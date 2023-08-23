import launcher.routines.logic as logic
import webserver.main as main
import dataclasses
import threading
import time


@dataclasses.dataclass
class port:
    def __hash__(self) -> int:
        return self.port_num
    port_num: int
    is_ssl: bool


@dataclasses.dataclass
class _argtype(logic.subparser_argtype):
    port: port


class webserver(logic.entry):
    httpds = list[main.webserver]()

    def __make_server(self, *args, **kwargs) -> None:
        self.httpds.append(ht := main.make_server(*args, **kwargs))
        self.threads.append(th := threading.Thread(target=ht.serve_forever))
        th.start()

    def __init__(self, global_args: logic.global_argtype, args: _argtype) -> None:
        self.server_running = True
        try:
            self.__make_server(
                **args.port.__dict__,
                roblox_version=global_args.roblox_version,
            )
        except PermissionError:
            print('WARNING: webserver was unable to start.')
            self.server_running = False
        except Exception as e:
            pass

    def __del__(self) -> None:
        if not self.server_running:
            return
        for ht in self.httpds:
            ht.shutdown()


class argtype(_argtype):
    obj_type = webserver
