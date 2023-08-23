from webserver.main import make_server
import util.versions as versions
import dataclasses
import subprocess
import threading
import time


@dataclasses.dataclass
class port:
    def __hash__(self) -> int:
        return self.port_num
    port_num: int
    is_ssl: bool


class webserver_wrap(subprocess.Popen):
    httpds = []
    threads = []

    def __make_server(self, *args, **kwargs) -> None:
        self.httpds.append(ht := make_server(*args, **kwargs))
        self.threads.append(th := threading.Thread(target=ht.serve_forever))
        th.start()

    def __init__(self, *args, ports: set[port], roblox_version: versions.Version, **kwargs) -> None:
        self.server_running = True
        try:
            for d in ports:
                self.__make_server(**d.__dict__, roblox_version=roblox_version)
            time.sleep(1)
        except PermissionError:
            print('WARNING: webserver was unable to start.')
            self.server_running = False
        except Exception as e:
            pass
        super().__init__(*args, **kwargs)

    def __clear(self) -> None:
        if not self.server_running:
            return
        for ht in self.httpds:
            ht.shutdown()

    def __del__(self) -> None:
        super().__del__()
        self.__clear()
