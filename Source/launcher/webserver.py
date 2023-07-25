from webserver._main import make_server
import subprocess
import threading
import versions
import time


class WebserverWrap(subprocess.Popen):
    httpds = []
    threads = []

    def __make_httpd(self, port: int, *args, **kwargs) -> None:
        self.httpds.append(ht := make_server(port, *args, **kwargs))
        self.threads.append(th := threading.Thread(target=ht.serve_forever))
        th.start()

    def __init__(self, *args, version: versions.Version, **kwargs) -> None:
        self.server_running = True
        try:
            config = {
                'version': version,
            }
            self.__make_httpd(80, is_ssl=False, **config)
            self.__make_httpd(443, is_ssl=True, **config)
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
