from ..downloader import _main as downloader
import urllib.request
import util.versions
import util.resource
import urllib.error
import config._main
import dataclasses
import subprocess
import functools
import threading
import ssl
import os


@dataclasses.dataclass
class port:
    def __hash__(self) -> int:
        return self.port_num
    port_num: int
    is_ssl: bool = True
    is_ipv6: bool = False


class _entry:
    def process(self):
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

    def get_app_base_url(self) -> str:
        raise NotImplementedError()


class bin_ssl_arg_type(bin_arg_type):
    web_host: str | None = None
    web_port: port = port(
        port_num=80,
        is_ssl=True,
        is_ipv6=False,
    )


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
        self.maybe_download_binary()

    def get_versioned_path(self, *paths: str) -> str:
        return super().get_versioned_path(
            self.DIR_NAME, *paths,
        )

    def maybe_download_binary(self) -> None:
        '''
        Check if Rōblox is not downloaded; else skip.
        '''
        if os.path.isdir(self.get_versioned_path()):
            return
        elif self.local_args.auto_download:
            print(
                'Downloading "%s" for Rōblox version %s' %
                (self.DIR_NAME, self.rōblox_version)
            )
            downloader.download_binary(self.rōblox_version, self.DIR_NAME)
        else:
            raise FileNotFoundError(
                '"%s" not found for Rōblox version %s.' %
                (self.DIR_NAME, self.rōblox_version)
            )


class bin_ssl_entry(bin_entry):
    '''
    Routine entry abstract class that corresponds to a binary with a special `./SSL` directory.
    '''
    local_args: bin_ssl_arg_type
    DIR_NAME: str

    @staticmethod
    @functools.cache
    def get_none_ssl() -> ssl.SSLContext:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return ctx

    def save_ssl_cert(self) -> None:
        if not self.local_args.web_port.is_ssl:
            return

        try:
            res = urllib.request.urlopen(
                f'{self.local_args.get_base_url()}/rfd/cert',
                context=bin_ssl_entry.get_none_ssl(),
            )
        except urllib.error.URLError:
            raise urllib.error.URLError(
                'No server is currently running on %s:%d.' %
                (self.local_args.web_host, self.local_args.web_port.port_num),
            )

        path = self.get_versioned_path('SSL', 'cacert.pem')
        with open(path, 'wb') as f:
            f.write(res.read())


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
            self.entries.append(e)  # type: ignore
            e.process()

    def wait(self):
        for e in self.entries:
            e.wait()

    def __del__(self):
        for e in self.entries:
            del e
