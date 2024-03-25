import launcher.aux_tasks.download
import config._main
import util.versions
import util.resource
import dataclasses
import subprocess
import threading
import os


@dataclasses.dataclass
class port:
    def __hash__(self) -> int:
        return self.port_num
    port_num: int
    is_ssl: bool = True
    is_ipv6: bool = False


class _entry:
    def initialise(self):
        raise NotImplementedError()


class arg_type:
    obj_type: type[_entry]

    def sanitise(self) -> None:
        pass


class server_arg_type(arg_type):
    server_config: config._main.obj_type


class bin_arg_type(arg_type):
    auto_download: bool

    def get_base_url(self) -> str:
        raise NotImplementedError()


class entry(_entry):
    local_args: arg_type
    threads: list[threading.Thread]

    def __init__(self, local_args: arg_type) -> None:
        self.local_args = local_args
        self.threads = []

    def wait(self) -> None:
        for t in self.threads:
            while t.is_alive():
                t.join(1)


class popen_entry(entry, subprocess.Popen):
    '''
    Routine entry class that corresponds to a Popen subprocess object.
    '''

    def make_popen(self, *args, **kwargs) -> None:
        subprocess.Popen.__init__(self, *args, **kwargs)

    def __del__(self) -> None:
        if hasattr(self, '_handle'):
            subprocess.Popen.__del__(self)

    def wait(self) -> None:
        subprocess.Popen.wait(self)


class ver_entry(entry):
    '''
    Routine entry abstract class that corresponds to a versioned directory of Rōblox.
    '''
    rōblox_version: util.versions.rōblox

    def retr_version(self) -> util.versions.rōblox:
        raise NotImplementedError()

    def get_versioned_path(self, *paths: str) -> str:
        return util.resource.retr_rōblox_full_path(
            self.rōblox_version, *paths,
        )


class bin_entry(ver_entry, popen_entry):
    '''
    Routine entry abstract class that corresponds to a versioned binary of Rōblox.
    '''
    local_args: bin_arg_type
    DIR_NAME: str

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.rōblox_version = self.retr_version()
        if not os.path.isdir(self.get_versioned_path()):
            if self.local_args.auto_download:
                dl = launcher.aux_tasks.download.obj_type(
                    self.rōblox_version, self.DIR_NAME)
                dl.initialise()
            else:
                raise FileNotFoundError(f'"{self.DIR_NAME}" not found for Rōblox version {
                                        self.rōblox_version}.')

    def get_versioned_path(self, *paths: str) -> str:
        return super().get_versioned_path(
            self.DIR_NAME, *paths,
        )


class server_entry(entry):
    '''
    Routine entry class that corresponds to a server-sided component.
    '''
    server_config: config._main.obj_type
    local_args: server_arg_type

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.server_config = self.local_args.server_config


class routine:
    entries: list[entry]

    def __init__(self, *args_list: arg_type) -> None:
        self.entries = []
        for args in args_list:
            args.sanitise()
            e = args.obj_type(args)
            self.entries.append(e)
            e.initialise()

    def wait(self):
        for e in self.entries:
            e.wait()

    def __del__(self):
        for e in self.entries:
            del e
