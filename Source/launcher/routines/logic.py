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
    threads = list[threading.Thread]()

    def make(self, global_args: global_argtype, args: subparser_argtype):
        raise NotImplementedError()

    def wait(self):
        for t in self.threads:
            while t.is_alive():
                t.join(1)


class popen_entry(subprocess.Popen, entry):
    def make_popen(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def wait(self):
        self.communicate()

    def __del__(self):
        self.terminate()


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
