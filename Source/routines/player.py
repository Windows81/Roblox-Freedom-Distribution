# Standard library imports
import dataclasses
import time
import urllib.parse
import json

# Typing imports
from typing import override

# Local application imports
import logger
from textwrap import dedent
import util.resource
import util.versions
from . import _logic as logic


class obj_type(logic.bin_web_entry):
    local_args: 'arg_type'
    BIN_SUBTYPE = util.resource.bin_subtype.PLAYER

    @override
    def retr_version(self) -> util.versions.rōblox:
        res = self.local_args.send_request('/rfd/roblox-version')
        return util.versions.rōblox.from_name(
            str(res.read(), encoding='utf-8'),
        )

    def save_app_setting(self) -> str:
        '''
        Modifies settings to point to correct host name.
        '''
        path = self.get_versioned_path('AppSettings.xml')
        app_base_url = self.local_args.get_app_base_url()
        with open(path, 'w', encoding='utf-8') as f:
            f.write(dedent(f'''\
                <?xml version="1.0" encoding="UTF-8"?>
                <Settings>
                    <ContentFolder>Content</ContentFolder>
                    <BaseUrl>{app_base_url}</BaseUrl>
                </Settings>
            '''))
        return path

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
        self.save_app_setting()
        self.update_fflags()

    def make_client_popen(self) -> None:
        base_url = self.local_args.get_base_url()
        self.make_popen([
            self.get_versioned_path('RobloxPlayerBeta.exe'),
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
        ])

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
class arg_type(
    logic.host_arg_type,
    logic.loggable_arg_type,
):
    obj_type = obj_type

    rcc_host: str
    rcc_port: int
    web_host: str
    web_port: int
    log_filter: logger.filter.filter_type
    user_code: str | None = None
    launch_delay: float = 0

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
