# Standard library imports
import functools
import urllib.parse
import dataclasses
import ipaddress
import time

# Typing imports
from typing import ClassVar, override

# Local application imports
from .. import _logic as logic
import util.resource
import util.versions
import util.const


@dataclasses.dataclass(kw_only=True, unsafe_hash=True)
class obj_type(logic.bin_entry):
    BIN_SUBTYPE: ClassVar = util.resource.bin_subtype.PLAYER
    DIRS_TO_ADD: ClassVar = ['logs', 'LocalStorage']

    web_host: str = 'localhost'
    web_port: int = util.const.RFD_DEFAULT_PORT
    rcc_host: str | None
    rcc_port: int | None
    app_host: str = dataclasses.field(init=False)

    user_code: str | None
    launch_delay: float = 0

    @override
    def __post_init__(self) -> None:
        super().__post_init__()
        (
            self.web_host, self.rcc_host,
        ) = self.maybe_differenciate_web_and_rcc_stuff(
            self.web_host, self.rcc_host,
        )
        (
            self.web_port, self.rcc_port,
        ) = self.maybe_differenciate_web_and_rcc_stuff(
            self.web_port, self.rcc_port,
        )
        (
            self.rcc_host, self.rcc_port,
        ) = self.maybe_separate_host_and_port(
            self.rcc_host, self.rcc_port,
        )

        if self.rcc_host == 'localhost':
            self.rcc_host = '127.0.0.1'

        self.app_host = self.web_host
        if self.web_host == 'localhost':
            self.web_host = self.app_host = '127.0.0.1'

        elif self.app_host.startswith('['):
            # Converts
            # - "[2607:fb91:1b74:d4d8:3dfb:5a51:55c3:d516]" into
            # - "[2607:fb91:1b74:d4d8:3dfb:5a51:85.195.213.22]"
            # This is because Rōblox's CoreScripts do not like working with `BaseUrl` settings which don't have dots.
            prefix_len = 30
            ipv6_obj = ipaddress.IPv6Address(self.web_host[1:-1])
            ipv4_mapped = ipaddress.IPv4Address(int(ipv6_obj) & 0xFFFFFFFF)
            exploded_str = ipv6_obj.exploded
            self.app_host = f"[{exploded_str[:prefix_len]}{ipv4_mapped!s}]"

    def finalise_user_code(self) -> None:
        '''
        This method is separate from `__post_init__` because
        it needs to be executed after `launch_delay` seconds.
        The `__post_init__` method gets executed before that delay.
        '''
        if self.user_code != '':
            return
        res = self.send_request('/rfd/default-user-code')
        self.user_code = str(res.read(), encoding='utf-8')

    @override
    def get_base_url(self) -> str:
        return f'https://{self.web_host}:{self.web_port}'

    @override
    def get_app_base_url(self) -> str:
        return f'https://{self.app_host}:{self.web_port}'

    @override
    @functools.cache
    def retr_version(self) -> util.versions.rōblox:
        res = self.send_request('/rfd/roblox-version')
        return util.versions.rōblox.from_name(
            str(res.read(), encoding='utf-8'),
        )

    @override
    def bootstrap(self) -> None:
        super().bootstrap()
        time.sleep(self.launch_delay)
        self.finalise_user_code()
        self.make_client_popen()

    def make_client_popen(self) -> None:
        base_url = self.get_base_url()
        self.make_popen(
            self.get_versioned_path('RobloxPlayerBeta.exe'),
            (
                '-a', f'{base_url}/login/negotiate.ashx',
                '-j', f'{base_url}/game/PlaceLauncher.ashx?' +
                urllib.parse.urlencode({k: v for k, v in {
                    'MachineAddress': self.rcc_host,
                    'ServerPort': self.rcc_port,
                    'UserCode': self.user_code,
                }.items() if v}),
                '-t', '1',
            ))

    @override
    def restart(self) -> None:
        self.stop()
        self.bootstrap()
        self.make_client_popen()
