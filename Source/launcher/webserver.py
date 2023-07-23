from webserver.main import make_httpd
import subprocess
import threading
import time


class WebserverWrap(subprocess.Popen):
    httpds = []
    threads = []

    def __make_httpd(self, port: int, *args, **kwargs) -> None:
        self.httpds.append(ht := make_httpd(port, *args, **kwargs))
        self.threads.append(th := threading.Thread(target=ht.serve_forever))
        th.start()

    def __init__(self, *args, **kwargs) -> None:
        self.server_running = True
        try:
            self.__make_httpd(80)
            self.__make_httpd(443, is_ssl=True)
            time.sleep(1)
        except PermissionError:
            print('WARNING: webserver was unable to start.')
            self.server_running = False
        except Exception as e:
            pass
        super().__init__(*args, **kwargs)

    def __clear(self):
        if not self.server_running:
            return
        for ht in self.httpds:
            ht.shutdown()

    def __del__(self) -> None:
        super().__del__()
        self.__clear()
