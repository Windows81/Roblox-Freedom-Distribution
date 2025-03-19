import game_config.structure
import game_config as config
from typing import override
import urllib.request
import util.versions
import util.resource
import urllib.error
import urllib.parse
import http.client
import downloader
import subprocess
import threading
import ipaddress
import shutil
import atexit
import logger
import copy
import ssl
import re


class _entry:
    def process(self) -> None:
        raise NotImplementedError()


class arg_type:
    obj_type: type['entry']

    def sanitise(self) -> None:
        pass


class popen_arg_type(arg_type):
    debug_x96: bool


class server_arg_type(arg_type):
    game_config: game_config.obj_type


class loggable_arg_type(arg_type):
    log_filter: logger.filter.filter_type


class bin_arg_type(popen_arg_type, loggable_arg_type):
    auto_download: bool

    def get_base_url(self) -> str:
        raise NotImplementedError()

    def get_app_base_url(self) -> str:
        raise NotImplementedError()


class bin_web_arg_type(bin_arg_type):
    web_host: str
    web_port: int

    @staticmethod
    def resolve_host_port(host: str, port: int) -> tuple[str, int]:
        if not host.startswith('[') and re.search(r':.*:', host) is not None:
            host = '[%s]' % host
            return (host, port)

        port_in_host = re.search(r':(\d{1,5})$', host)
        if port_in_host is not None:
            port = int(port_in_host.group(1))
            host = host[:port_in_host.start()]
        return (host, port)

    @override
    def sanitise(self) -> None:
        super().sanitise()
        (
            self.web_host, self.web_port,
        ) = self.resolve_host_port(
            self.web_host, self.web_port,
        )

    def send_request(
        self,
        path: str,
        timeout: float = 7,
    ) -> http.client.HTTPResponse:
        assert self.web_port is not None
        try:
            return urllib.request.urlopen(
                f'{self.get_base_url()}{path}',
                context=bin_web_entry.get_none_ssl(),
                timeout=timeout,
            )
        except urllib.error.URLError as _:
            raise Exception(
                'No server is currently running on %s (%s).' %
                (self.get_base_url(), path),
            )


class host_arg_type(bin_web_arg_type):
    rcc_host: str
    rcc_port: int

    web_host: str
    web_port: int
    user_code: str | None = None
    launch_delay: float = 0

    @override
    def sanitise(self) -> None:
        super().sanitise()
        (
            self.rcc_host, self.rcc_port,
        ) = self.resolve_host_port(
            self.rcc_host, self.rcc_port,
        )

        if self.rcc_host == 'localhost':
            self.rcc_host = '127.0.0.1'

        self.app_host = self.web_host
        if self.web_host == 'localhost':
            self.web_host = self.app_host = '127.0.0.1'

        elif self.web_host.startswith('['):
            # The ".ipv6-literal.net" replacement only works on Windows and might not translate well on Wine.
            # It's strictly necessary for 2021E because some CoreGUI stuff will
            # crash if the BaseUrl doesn't have a dot in it.
            unc_ip_str = (
                self.web_host[1:-1]
                .replace(':', '-')
                .replace('%', 's')
            )
            if unc_ip_str.startswith('-'):
                unc_ip_str = '0%s' % unc_ip_str
            self.web_host = self.app_host = '%s.ipv6-literal.net' % unc_ip_str


class entry(_entry):
    local_args: arg_type

    def __init__(self, local_args: arg_type) -> None:
        super().__init__()
        self.local_args = local_args
        self.threads: list[threading.Thread] = []

    def wait(self) -> None:
        for t in self.threads:
            while t.is_alive():
                t.join(1)

    def stop(self) -> None:
        entry.wait(self)

    def __del__(self) -> None:
        return self.stop()


class restartable_entry(entry):
    def restart(self) -> None:
        raise NotImplementedError()


class popen_entry(entry):
    '''
    Routine entry class that corresponds to a Popen subprocess object.
    '''
    local_args: popen_arg_type

    def __init__(self, local_args: arg_type) -> None:
        super().__init__(local_args)
        # Arrays are initialised in case `make_popen` raises an exception.
        self.debug_popen: subprocess.Popen[str]
        self.popen_mains: list[subprocess.Popen[str]] = []
        self.popen_daemons: list[subprocess.Popen[str]] = []
        self.is_terminated: bool = False

    def make_popen(self, cmd_args: list[str], *args, **kwargs) -> None:
        '''
        Creates new thread(s) for the Popen to operate under.
        '''

        # Checks if Wine is installed.  Redundant if using Windows.
        if shutil.which('wine') is not None:
            cmd_args[:0] = ['wine']

        self.is_terminated = False
        self.principal = subprocess.Popen(cmd_args, *args, **kwargs)
        self.popen_mains = [
            self.principal,
        ]
        self.popen_daemons = [
            *(
                [
                    subprocess.Popen[str]([
                        'x96dbg',
                        '-p', str(self.principal.pid),
                    ])
                ]
                if self.local_args.debug_x96
                else []
            ),
        ]

        # No current working use.
        # This may be necessary because the Popen object might not be terminated when RFD quites.
        atexit.register(lambda: self.stop())

    @override
    def stop(self) -> None:
        for p in self.popen_mains:
            p.terminate()
        for p in self.popen_daemons:
            p.terminate()
        self.is_terminated = True
        super().stop()

    @override
    def wait(self) -> None:
        for p in self.popen_mains:
            p.wait()
        for p in self.popen_daemons:
            p.terminate()
        self.is_terminated = True
        super().wait()


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

    def get_versioned_path(
            self,
            bin_type: util.resource.bin_subtype,
            *paths: str) -> str:
        return util.resource.retr_rōblox_full_path(
            self.rōblox_version, bin_type, *paths)


class loggable_entry(entry):
    local_args: loggable_arg_type

    def log(self, message: bytes | str) -> None:
        logger.log(
            message,
            context=logger.log_context.PYTHON_SETUP,
            filter=self.local_args.log_filter,
        )


class bin_entry(ver_entry, popen_entry, loggable_entry):
    '''
    Routine entry abstract class that corresponds to a versioned binary of Rōblox.
    '''
    local_args: bin_arg_type
    BIN_SUBTYPE: util.resource.bin_subtype

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.rōblox_version = self.retr_version()
        self.maybe_download_binary()

    @override
    def get_versioned_path(self, *paths: str) -> str:
        return super().get_versioned_path(
            self.BIN_SUBTYPE, *paths,
        )

    def maybe_download_binary(self) -> None:
        '''
        Check if Rōblox is not downloaded; else skip.
        '''
        if not self.local_args.auto_download:
            return
        downloader.bootstrap_binary(
            rōblox_version=self.rōblox_version,
            bin_type=self.BIN_SUBTYPE,
            log_filter=self.local_args.log_filter,
        )


class bin_web_entry(bin_entry):
    '''
    Routine entry abstract class that corresponds to a binary with a special `./SSL` directory.
    '''
    local_args: bin_web_arg_type

    @staticmethod
    def get_none_ssl() -> ssl.SSLContext:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return ctx


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
    Each of these objects points to a class whose `__init__` method is called with the data in that argument object.
    '''
    entries: list[entry]

    def __init__(self, *args_list: arg_type) -> None:
        super().__init__()
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
            e.stop()
