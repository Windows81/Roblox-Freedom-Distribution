import util.versions as versions
import dataclasses
import subprocess
import threading
import time


@dataclasses.dataclass
class global_argtype:
    roblox_version: versions.roblox


class _entry:
    pass


class subparser_argtype:
    obj_type: type[_entry]


class entry:
    global_args: global_argtype
    local_args: subparser_argtype
    threads = list[threading.Thread]()

    def __init__(self, global_args: global_argtype, local_args: subparser_argtype) -> None:
        self.global_args = global_args
        self.local_args = local_args
        self.make()

    def make(self):
        raise NotImplementedError()

    def wait(self) -> None:
        for t in self.threads:
            while t.is_alive():
                t.join(1)


class popen_entry(entry, subprocess.Popen):
    def make_popen(self, *args, **kwargs) -> None:
        subprocess.Popen.__init__(self, *args, **kwargs)

    def __del__(self) -> None:
        super().terminate()


class routine:
    entries: list[entry]

    def __init__(self, global_args: global_argtype, *args_list: subparser_argtype) -> None:
        self.entries = [
            args.obj_type(global_args, args)
            for args in args_list
        ]

    def wait(self):
        for e in self.entries:
            e.wait()

    def __del__(self):
        for e in self.entries:
            del e
