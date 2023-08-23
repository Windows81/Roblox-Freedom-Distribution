import util.versions as versions
import dataclasses
import subprocess
import threading
import time


@dataclasses.dataclass
class global_argtype:
    roblox_version: versions.Version


class _entry:
    pass


class subparser_argtype:
    obj_type: type[_entry]


class entry:
    threads = list[threading.Thread]()

    def make(self, global_args: global_argtype, args: subparser_argtype):
        raise NotImplementedError()

    def join(self):
        for t in self.threads:
            t.join()


class popen_entry(subprocess.Popen, entry):
    def make_popen(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def join(self):
        self.communicate()


class routine:
    entries: list[entry]

    def __init__(self, global_args: global_argtype, *args_list: subparser_argtype) -> None:
        self.entries = [
            args.obj_type(global_args, args)
            for args in args_list
        ]

    def __del__(self):
        try:
            for e in self.entries:
                e.join()
        except KeyboardInterrupt:
            pass
        finally:
            for e in self.entries:
                del e
