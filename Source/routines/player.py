# Standard library imports
import dataclasses
import ipaddress
import time
import urllib.parse
import json

# Typing imports
from typing import override

# Local application imports
import logger
import util.resource
import util.versions
from . import _logic as logic


class obj_type(logic.bin_entry):
    local_args: 'arg_type'
    BIN_SUBTYPE = util.resource.bin_subtype.PLAYER
    DIRS_TO_ADD = ['logs', 'LocalStorage']

    @override
    def retr_version(self) -> util.versions.rōblox:
        res = self.local_args.send_request('/rfd/roblox-version')
        return util.versions.rōblox.from_name(
            str(res.read(), encoding='utf-8'),
        )

    def update_fflags(self) -> None:
        '''
        Updates the FFlags in the game configuration.
        '''
        # TODO: move FFlag loading to an API endpoint.
        new_flags = {
            **self.local_args.log_filter.rcc_logs.get_level_table(),
        }

        path = self.get_versioned_path(
            'ClientSettings',
            'ClientAppSettings.json',
        )
        with open(path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)

        json_data |= new_flags
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent='\t')

    def bootstrap(self) -> None:
        self.save_app_settings()
        self.make_aux_directories()
        self.update_fflags()

    def make_client_popen(self) -> None:
        base_url = self.local_args.get_base_url()
        self.make_popen(
            self.get_versioned_path('RobloxPlayerBeta.exe'),
            (
                '-a', f'{base_url}/login/negotiate.ashx',
                '-j', f'{base_url}/game/PlaceLauncher.ashx?' +
                urllib.parse.urlencode({k: v for k, v in {
                    'rcc-host-addr':
                    self.local_args.rcc_host,
                    'rcc-port':
                    self.local_args.rcc_port,
                    'user-code':
                    self.local_args.user_code,
                }.items() if v}),
                '-t', '1',
            ))

    @override
    def process(self) -> None:
        self.bootstrap()
        time.sleep(self.local_args.launch_delay)
        self.local_args.finalise_user_code()
        self.make_client_popen()

    @override
    def restart(self) -> None:
        self.stop()
        self.bootstrap()
        self.make_client_popen()


@dataclasses.dataclass
class arg_type(logic.bin_arg_type, logic.loggable_arg_type):
    obj_type = obj_type

    rcc_host: str
    rcc_port: int
    web_host: str
    web_port: int

    log_filter: logger.filter.filter_type
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
        This method is separate from `sanitise` because
        it needs to be executed after `launch_delay` seconds.
        The `sanitise` method gets executed before that delay.
        '''
        if self.user_code is not None:
            return
        res = self.send_request('/rfd/default-user-code')
        self.user_code = str(res.read(), encoding='utf-8')

    @override
    def get_base_url(self) -> str:
        return f'https://{self.web_host}:{self.web_port}'

    @override
    def get_app_base_url(self) -> str:
        return f'https://{self.app_host}:{self.web_port}'
