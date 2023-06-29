import subprocess
import time


class UwAmp(subprocess.Popen):
    def __init__(self) -> None:
        super().__init__(['start', '/min', './Webserver/UwAmp.exe'], shell=True)


class UwAmpWrap(subprocess.Popen):
    def __init__(self, *a, **kwa) -> None:
        super().__init__(*a, **kwa)
        self.uwamp = UwAmp()
        time.sleep(3)

    def __del__(self):
        del self.uwamp
