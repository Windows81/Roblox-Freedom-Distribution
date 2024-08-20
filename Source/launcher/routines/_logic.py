import web_server._logic as web_server_logic
from .. import downloader as downloader
import config.structure
import urllib.request
import util.versions
import util.resource
import urllib.error
import urllib.parse
import http.client
import subprocess
import threading
import certifi
import config
import copy
import ssl
import os


class _entry:
    def process(self):
        raise NotImplementedError()


class arg_type:
    obj_type: type['entry']

    def sanitise(self) -> None:
        pass

    def reconstruct(self):
        result = copy.copy(self)
        result.sanitise()
        return result


class popen_arg_type(arg_type):
    debug_x96: bool


class server_arg_type(arg_type):
    game_config: config.obj_type


class bin_arg_type(popen_arg_type):
    auto_download: bool

    def get_base_url(self) -> str:
        raise NotImplementedError()

    def get_app_base_url(self) -> str:
        raise NotImplementedError()


class bin_ssl_arg_type(bin_arg_type):
    web_host: str
    web_port: web_server_logic.port_typ

    def send_request(self, path: str, timeout: float = 7) -> http.client.HTTPResponse:
        assert self.web_port.port_num is not None
        try:
            return urllib.request.urlopen(
                f'{self.get_base_url()}{path}',
                context=bin_ssl_entry.get_none_ssl(),
                timeout=timeout,
            )
        except urllib.error.URLError as e:
            raise Exception(
                'No server is currently running on %s:%d (%s).' %
                (self.web_host, self.web_port.port_num, path),
            )


class host_arg_type(arg_type):
    rcc_host: str
    rcc_port_num: int

    web_host: str
    web_port: web_server_logic.port_typ
    user_code: str | None = None
    launch_delay: float = 0

    def sanitise(self) -> None:
        super().sanitise()

        if self.rcc_host == 'localhost':
            self.rcc_host = '127.0.0.1'
        elif ':' in self.rcc_host:
            self.rcc_host = f'[{self.rcc_host}]'

        if self.rcc_host == 'localhost':
            self.rcc_host = '127.0.0.1'
        elif ':' in self.rcc_host:
            self.rcc_host = f'[{self.rcc_host}]'

        self.app_host = self.web_host
        if self.web_host == 'localhost':
            self.web_host = self.app_host = '127.0.0.1'

        elif self.web_host and ':' in self.web_host:
            # The ".ipv6-literal.net" replacement only works on Windows and might not translate well on Wine.
            # It's strictly necessary for 2021E because some CoreGUI stuff will crash if the BaseUrl doesn't have a dot in it.
            unc_ip_str = self.web_host.replace(':', '-')
            self.web_host = self.app_host = f'{unc_ip_str}.ipv6-literal.net'


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


class popen_entry(entry):
    '''
    Routine entry class that corresponds to a Popen subprocess object.
    '''
    local_args: popen_arg_type
    debug_popen: subprocess.Popen
    popen_mains: list[subprocess.Popen]
    popen_daemons: list[subprocess.Popen]

    def __init__(self, local_args: arg_type) -> None:
        super().__init__(local_args)
        # Arrays are initialised in case `make_popen` raises an exception.
        self.popen_mains = []
        self.popen_daemons = []

    def make_popen(self, cmd_args: list, *args, **kwargs) -> None:
        # TODO: test native support for RFD on systems with Wine.
        if os.name != 'nt':
            cmd_args[:0] = ['wine']

        self.principal = subprocess.Popen(cmd_args, *args, **kwargs)
        self.popen_mains = [
            self.principal,
        ]
        self.popen_daemons = [
            *(
                [
                    subprocess.Popen([
                        'x32dbg-unsigned',
                        '-p', str(self.principal.pid),
                    ])
                ]
                if self.local_args.debug_x96
                else []
            ),
        ]

    def __del__(self) -> None:
        for p in self.popen_mains:
            p.terminate()
        for p in self.popen_daemons:
            p.terminate()

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
        '''
        Gets called once on `bin_entry.__init__` to initialise `self.rōblox_version`
        '''
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
            print("Rōblox installation exists, skipping...")
            return
        elif self.local_args.auto_download:
            print(
                'Downloading zipped "%s" for Rōblox version %s...' %
                (self.BIN_SUBTYPE.name, self.rōblox_version.get_number())
            )
            downloader.bootstrap_binary(self.rōblox_version, self.BIN_SUBTYPE)
            print('Download completed!')
        else:
            raise Exception(
                'Zipped file "%s" not found for Rōblox version %s.' %
                (self.BIN_SUBTYPE.name, self.rōblox_version.get_number())
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

    def save_ssl_cert(self, include_system_certs: bool = False) -> None:
        if not self.local_args.web_port.is_ssl:
            return

        res = self.local_args.send_request(f'/rfd/certificate')
        path = self.get_versioned_path('SSL', 'cacert.pem')

        cert_content = res.read().decode()
        if include_system_certs:
            cert_content += certifi.contents()

        with open(path, 'w') as f:
            f.write(cert_content)


class server_entry(entry):
    '''
    Routine entry class that corresponds to a server-sided component.
    '''
    game_config: config.obj_type
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

    def wait(self) -> None:
        for e in self.entries:
            e.wait()

    def __del__(self) -> None:
        for e in self.entries:
            del e
