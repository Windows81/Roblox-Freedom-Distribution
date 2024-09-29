import web_server._logic as web_server_logic
from . import _logic as logic
import urllib.request
import util.resource
import util.versions
import urllib.parse
import urllib.error
import dataclasses
import util.const
import ctypes
import time


class obj_type(logic.bin_ssl_entry):
    local_args: 'arg_type'
    BIN_SUBTYPE = util.resource.bin_subtype.PLAYER

    def retr_version(self) -> util.versions.rōblox:
        res = self.local_args.send_request('/rfd/roblox-version')
        return util.versions.rōblox.from_name(str(res.read(), encoding='utf-8'))

    def save_app_setting(self) -> str:
        '''
        Modifies settings to point to correct host name.
        '''
        path = self.get_versioned_path('AppSettings.xml')
        app_base_url = self.local_args.get_app_base_url()
        with open(path, 'w', encoding='utf-8') as f:
            f.write('\n'.join([
                """<?xml version="1.0" encoding="UTF-8"?>""",
                """<Settings>""",
                f"""\t<BaseUrl>{app_base_url}</BaseUrl>""",
                """</Settings>""",
            ]))
        return path

    def enable_mutex(self) -> None:
        '''
        Enables multiple instances of Rōblox to run concurrently.
        '''
        if self.rōblox_version.get_number() > 400:
            return
        ctypes.windll.kernel32.CreateMutexW(0, 1, "ROBLOX_singletonEvent")

    def process(self) -> None:
        self.save_app_setting()
        self.enable_mutex()
        self.save_ssl_cert(
            include_system_certs=False,
        )

        time.sleep(self.local_args.launch_delay)
        self.local_args.finalise_user_code()
        base_url = self.local_args.get_base_url()
        self.make_popen([
            self.get_versioned_path('RobloxPlayerBeta.exe'),
            '-a', f'{base_url}/login/negotiate.ashx',
            '-j', f'{base_url}/game/PlaceLauncher.ashx?' +
            urllib.parse.urlencode({k: v for k, v in {
                'rcc-host-addr':
                    self.local_args.rcc_host,
                'rcc-port':
                    self.local_args.rcc_port_num,
                'user-code':
                    self.local_args.user_code,
            }.items() if v}),
            '-t', '1',
        ])


@dataclasses.dataclass
class arg_type(logic.bin_ssl_arg_type, logic.host_arg_type):
    obj_type = obj_type

    rcc_host: str
    rcc_port_num: int
    web_host: str
    web_port: web_server_logic.port_typ
    user_code: str | None = None
    launch_delay: float = 0

    def finalise_user_code(self) -> None:
        '''
        This method is seaprate from `sanitise` because
        it needs to be executed after `launch_delay` seconds.
        The `sanitise` method gets executed before that delay.
        '''
        if self.user_code is not None:
            return
        res = self.send_request('/rfd/default-user-code')
        self.user_code = str(res.read(), encoding='utf-8')

    def get_base_url(self) -> str:
        return \
            f'http{"s" if self.web_port.is_ssl else ""}://' + \
            f'{self.web_host}:{self.web_port.port_num}'

    def get_app_base_url(self) -> str:
        return \
            f'http{"s" if self.web_port.is_ssl else ""}://' + \
            f'{self.app_host}:{self.web_port.port_num}'

    def send_request(self, path: str, timeout: float = 7):
        return super().send_request(
            f'{path}?rcc-port={self.rcc_port_num}',
            timeout,
        )
