import launcher.gameconfig
import util.versions
import util.resource
import subprocess
import threading
import os


class _entry:
    def initialise(self):
        raise NotImplementedError()


class subparser_argtype:
    obj_type: type[_entry]


class server_argtype:
    server_config: launcher.gameconfig.configtype


class entry:
    local_args: subparser_argtype
    threads: list[threading.Thread]

    def __init__(self, local_args: subparser_argtype) -> None:
        self.local_args = local_args
        self.threads = []

    def wait(self) -> None:
        for t in self.threads:
            while t.is_alive():
                t.join(1)


class popen_entry(entry, subprocess.Popen):
    def make_popen(self, *args, **kwargs) -> None:
        subprocess.Popen.__init__(self, *args, **kwargs)

    def __del__(self) -> None:
        if hasattr(self, '_handle'):
            subprocess.Popen.__del__(self)

    def wait(self) -> None:
        subprocess.Popen.wait(self)


class bin_entry(popen_entry):
    rōblox_version: util.versions.rōblox
    local_args: server_argtype
    DIR_NAME: str

    def retrieve_version(self) -> util.versions.rōblox:
        raise NotImplementedError()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.rōblox_version = self.retrieve_version()
        if not os.path.isdir(self.get_versioned_path()):
            raise FileNotFoundError(f'"{self.DIR_NAME}" not found for Rōblox version {self.rōblox_version}.')

    def get_versioned_path(self, *paths: str) -> str:
        return util.resource.get_rōblox_full_path(
            self.rōblox_version,
            self.DIR_NAME, *paths,
        )


class server_entry(entry):
    config: launcher.gameconfig.configtype

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.config = launcher.gameconfig.configtype(
            self.local_args.server_config,
        )


class routine:
    entries: list[entry]

    def __init__(self, *args_list: subparser_argtype) -> None:
        self.entries = []
        for args in args_list:
            e = args.obj_type(args)
            self.entries.append(e)
            e.initialise()

    def wait(self):
        for e in self.entries:
            e.wait()

    def __del__(self):
        for e in self.entries:
            del e
