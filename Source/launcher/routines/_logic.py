from ..downloader import _main as downloader
import urllib.request
import util.versions
import util.resource
import urllib.error
import config._main
import urllib.parse
import http.client
import dataclasses
import subprocess
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
    obj_type: type['entry']

    def sanitise(self) -> None:
        pass


class popen_arg_type(arg_type):
    debug_x96: bool


class server_arg_type(arg_type):
    game_config: config._main.obj_type


class bin_arg_type(popen_arg_type):
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

    def send_request(self, path: str) -> http.client.HTTPResponse:
        try:
            return urllib.request.urlopen(
                f'{self.get_base_url()}{path}',
                context=bin_ssl_entry.get_none_ssl(),
                timeout=3,
            )
        except urllib.error.URLError:
            raise urllib.error.URLError(
                'No server is currently running on %s:%d.' %
                (self.web_host, self.web_port.port_num),
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
    local_args: popen_arg_type
    popen_mains: list[subprocess.Popen]
    popen_daemons: list[subprocess.Popen]
    debug_popen: subprocess.Popen

    def make_popen(self, *args, **kwargs) -> None:
        self.principal = subprocess.Popen(*args, **kwargs)
        self.popen_mains = [
            self.principal,
        ]
        self.popen_daemons = [
            *(
                [
                    subprocess.Popen([
                        'x96dbg',
                        '-p', str(self.principal.pid),
                    ])
                ]
                if self.local_args.debug_x96
                else []
            )
        ]

    def __del__(self) -> None:
        if hasattr(self, '_handle'):
            subprocess.Popen.__del__(self)

    def wait(self) -> None:
        for p in self.popen_mains:
            p.wait()
        for p in self.popen_daemons:
            p.terminate()


class ver_entry(entry):
    '''
    Routine entry abstract class that corresponds to a versioned directory of Rōblox.
    '''
    rōblox_version: util.versions.rōblox

    def retr_version(self) -> util.versions.rōblox:
        raise NotImplementedError()

    def get_versioned_path(self, bin_type: util.resource.bin_subtype, *paths: str) -> str:
        return util.resource.retr_rōblox_full_path(self.rōblox_version, bin_type, *paths)


class bin_entry(ver_entry, popen_entry):
    '''
    Routine entry abstract class that corresponds to a versioned binary of Rōblox.
    '''
    local_args: bin_arg_type
    BIN_SUBTYPE: util.resource.bin_subtype

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.rōblox_version = self.retr_version()
        self.maybe_download_binary()

    def get_versioned_path(self, *paths: str) -> str:
        return super().get_versioned_path(
            self.BIN_SUBTYPE, *paths,
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
                (self.BIN_SUBTYPE, self.rōblox_version.name)
            )
            downloader.download_binary(self.rōblox_version, self.BIN_SUBTYPE)
        else:
            raise FileNotFoundError(
                '"%s" not found for Rōblox version %s.' %
                (self.BIN_SUBTYPE, self.rōblox_version.name)
            )


class bin_ssl_entry(bin_entry):
    '''
    Routine entry abstract class that corresponds to a binary with a special `./SSL` directory.
    '''
    local_args: bin_ssl_arg_type

    @staticmethod
    def get_none_ssl() -> ssl.SSLContext:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return ctx

    def save_ssl_cert(self, query_args: dict = {}) -> None:
        if not self.local_args.web_port.is_ssl:
            return

        qs = urllib.parse.urlencode(query_args)
        res = self.local_args.send_request(f'/rfd/certificate?{qs}')
        path = self.get_versioned_path('SSL', 'cacert.pem')
        with open(path, 'wb') as f:
            f.write(res.read())


class server_entry(entry):
    '''
    Routine entry class that corresponds to a server-sided component.
    '''
    game_config: config._main.obj_type
    local_args: server_arg_type

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.game_config = self.local_args.game_config


class routine:
    '''
    Contains a list of `entry` objects.
    A routine is initialised with a list of argument data-class objects.
    Each of these objects points to a class, whose `__init__` method is called with the data in that argument object.

    '''
    entries: list[entry]

    def __init__(self, *args_list: arg_type) -> None:
        self.entries = []
        for args in args_list:
            args.sanitise()
            e = args.obj_type(args)
            self.entries.append(e)
            e.process()

    def wait(self):
        for e in self.entries:
            e.wait()

    def __del__(self):
        for e in self.entries:
            del e
