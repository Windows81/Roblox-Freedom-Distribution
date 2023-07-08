import subprocess
import time

PLACE_ID = 1818


class UwAmp(subprocess.Popen):
    def __init__(self) -> None:
        # https://stackoverflow.com/a/32121910
        super().__init__(
            './Webserver/UwAmp.exe',
            startupinfo=subprocess.STARTUPINFO(
                dwFlags=subprocess.STARTF_USESHOWWINDOW,
                wShowWindow=subprocess.SW_HIDE,
            ),
        )


class UwAmpWrap(subprocess.Popen):
    def __init__(self, *a, **kwa) -> None:
        self.uwamp = UwAmp()
        time.sleep(3)
        super().__init__(*a, **kwa)

    def __del__(self):
        self.uwamp.terminate()
