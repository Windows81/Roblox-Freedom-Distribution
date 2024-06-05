import web_server._logic as web_server_logic
import web_server as web_server

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
import os


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

    def save_ssl_cert(self):
        return super().save_ssl_cert({'user-code': self.local_args.user_code})

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
        self.save_ssl_cert()

        time.sleep(self.local_args.launch_delay)
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
class arg_type(logic.bin_ssl_arg_type):
    obj_type = obj_type

    rcc_host: str = 'localhost'
    rcc_port_num: int = 2005
    web_host: str | None = None
    web_port: web_server_logic.port_typ = web_server_logic.port_typ(
        port_num=80,
        is_ssl=False,
        is_ipv6=False,
    ),  # type: ignore
    user_code: str | None = None
    launch_delay: float = 0

    def sanitise_hosts(self):
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

    def sanitise_user_code(self):
        if self.user_code:
            return
        res = self.send_request('/rfd/default-user-code', timeout=120)
        self.user_code = str(res.read(), encoding='utf-8')

    def sanitise(self):
        super().sanitise()
        self.sanitise_hosts()
        self.sanitise_user_code()

    def get_base_url(self) -> str:
        return \
            f'http{"s" if self.web_port.is_ssl else ""}://' + \
            f'{self.web_host}:{self.web_port.port_num}'

    def get_app_base_url(self) -> str:
        return \
            f'http{"s" if self.web_port.is_ssl else ""}://' + \
            f'{self.app_host}:{self.web_port.port_num}'
