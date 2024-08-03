import dataclasses
import subprocess


class base_type:
    pass


@dataclasses.dataclass
class ret_none(base_type):
    error: str | None = None


@dataclasses.dataclass
class ret_data(base_type):
    data: bytes


@dataclasses.dataclass
class ret_relocate(base_type):
    url: str


class ret_cmd_stdout(base_type):
    def __init__(self, cmd_line: str) -> None:
        self.popen = subprocess.Popen(
            args=cmd_line,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        assert self.popen.stdout is not None
        self.stdout = self.popen.stdout

    def read(self) -> bytes:
        return self.stdout.read()

    def is_closed(self) -> bool:
        return self.popen.poll() is not None

    def __del__(self) -> None:
        self.popen.terminate()


def construct(
    data: bytes | None = None,
    redirect_url: str | None = None,
    cmd_line: str | None = None,
) -> base_type:
    if data is not None:
        return ret_data(data)
    elif redirect_url is not None:
        return ret_relocate(redirect_url)
    elif cmd_line is not None:
        return ret_cmd_stdout(cmd_line)
    return ret_none()
