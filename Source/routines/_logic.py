# Standard library imports
import textwrap
import urllib.request
import urllib.error
import http.client
import subprocess
import threading
import shutil
import ssl
import re

# Typing imports
from typing import Self, override

# Local application imports
import game_config as game_config_module
import downloader
import logger
import util.resource
import util.versions


class _entry:
    def process(self) -> None:
        raise NotImplementedError()


class arg_type:
    obj_type: type['entry']

    def sanitise(self) -> None:
        pass

    def __post_init__(self) -> None:
        self.sanitise()


class popen_arg_type(arg_type):
    debug_x96: bool


class gameconfig_arg_type(arg_type):
    game_config: game_config_module.obj_type


class loggable_arg_type(arg_type):
    log_filter: logger.filter.filter_type


class bin_arg_type(popen_arg_type, loggable_arg_type):
    auto_download: bool
    web_host: str
    web_port: int

    @staticmethod
    def get_none_ssl() -> ssl.SSLContext:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return ctx

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
                context=self.get_none_ssl(),
                timeout=timeout,
            )
        except urllib.error.URLError as _:
            raise Exception(
                'No server is currently running on %s (%s).' %
                (self.get_base_url(), path),
            )

    def get_base_url(self) -> str:
        raise NotImplementedError()

    def get_app_base_url(self) -> str:
        raise NotImplementedError()


class entry(_entry):
    local_args: arg_type

    def __init__(self, local_args: arg_type) -> None:
        super().__init__()
        self.local_args = local_args
        self.threads: list[threading.Thread] = []
        self.routine: 'routine | None' = None

    def wait(self) -> None:
        for t in self.threads:
            while t.is_alive():
                t.join(1)

    def stop(self) -> None:
        self.wait()

    def kill(self) -> None:
        if self.routine is not None:
            self.routine.stop()
        else:
            self.stop()

    def __del__(self) -> None:
        return self.stop()


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
        self.is_running: bool = False

    def make_popen(self, cmd_args: tuple[str, ...], *args, **kwargs) -> None:
        '''
        Creates new thread(s) for the Popen to operate under.
        '''
        # Checks if Wine is installed.  Redundant if using Windows.
        if shutil.which('wine') is not None:
            cmd_args = ('wine', *cmd_args)

        self.is_running = True
        if self.is_terminated:
            self.popen_mains.clear()
            self.popen_daemons.clear()
            self.is_terminated = False

        principal = subprocess.Popen(cmd_args, *args, **kwargs)
        self.popen_mains.append(principal)

        if self.local_args.debug_x96:
            popen_dbg = subprocess.Popen[str]([
                'x96dbg',
                '-p', str(principal.pid),
            ])
            self.popen_daemons.append(popen_dbg)

    @override
    def stop(self) -> None:
        if self.is_terminated:
            return
        if not self.is_running:
            return

        self.is_running = False
        for p in self.popen_mains:
            p.terminate()
        for p in self.popen_daemons:
            p.terminate()

        self.is_terminated = True
        super().stop()

    @override
    def wait(self) -> None:
        if self.is_terminated:
            return
        if not self.is_running:
            return

        for p in self.popen_mains:
            p.wait()
        for p in self.popen_daemons:
            p.terminate()

        self.is_running = False
        self.is_terminated = True
        super().wait()

    def restart(self) -> None:
        if not self.is_running:
            return

        self.is_running = False
        for p in self.popen_mains:
            p.terminate()
        for p in self.popen_daemons:
            p.terminate()

        self.is_running = True
        self.process()


class loggable_entry(entry):
    local_args: loggable_arg_type

    def log(self, message: bytes | str) -> None:
        logger.log(
            message,
            context=logger.log_context.PYTHON_SETUP,
            filter=self.local_args.log_filter,
        )


class bin_entry(popen_entry, loggable_entry):
    '''
    Routine entry abstract class that corresponds to a versioned binary of Rōblox.
    '''
    local_args: bin_arg_type
    rōblox_version: util.versions.rōblox
    BIN_SUBTYPE: util.resource.bin_subtype

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.rōblox_version = self.retr_version()
        self.maybe_download_binary()

    def get_versioned_path(self, *paths: str) -> str:
        return util.resource.retr_rōblox_full_path(self.rōblox_version, self.BIN_SUBTYPE, *paths)

    def retr_version(self) -> util.versions.rōblox:
        '''
        Gets called once on `bin_entry.__init__` to initialise `self.rōblox_version`
        '''
        raise NotImplementedError()

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

    def save_app_settings(self) -> str:
        '''
        Simply modifies `AppSettings.xml` to point to correct host name.
        '''
        path = self.get_versioned_path('AppSettings.xml')
        app_base_url = self.local_args.get_app_base_url()
        with open(path, 'w', encoding='utf-8') as f:
            f.write(textwrap.dedent(f'''\
                <?xml version="1.0" encoding="UTF-8"?>
                <Settings>
                    <ContentFolder>Content</ContentFolder>
                    <BaseUrl>{app_base_url}</BaseUrl>
                </Settings>
            '''))
        return path


class gameconfig_entry(entry):
    '''
    Routine entry class that maps to a GameConfig structure.
    '''
    game_config: game_config_module.obj_type
    local_args: gameconfig_arg_type

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.game_config = self.local_args.game_config


class routine:
    '''
    Contains a list of `entry` objects.
    A routine is initialised with a list of argument data-class objects.
    Each of these objects points to a class whose `__init__` method is called with the data in that argument object.

    Entries in `self.entries` have two stages of action:
    1) the time it takes to *complete* the `process` function, and
    2) the time it takes to join all subthreads in the `self.entries[*].threads` list field.

    For entries in the `self.entries` list field:
    - Entries evaluate stage (1) synchronously in forwards order.
    - Entries evaluate stage (2) asynchronously.
        - If an entry calls `kill` whilst in stage (2), forcibly terminate *all* the entries in the `self.entries` list field.
    '''
    entries: list[entry]

    def __init__(self, *args_list: arg_type) -> None:
        super().__init__()
        self.entries = []
        for args in args_list:
            e = args.obj_type(args)
            self.entries.append(e)
            e.routine = self
            e.process()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.stop()

    def wait(self) -> None:
        for e in self.entries:
            e.wait()

    def stop(self) -> None:
        for e in self.entries:
            e.stop()
