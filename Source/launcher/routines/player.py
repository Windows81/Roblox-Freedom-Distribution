import launcher.routines.webserver as webserver
import launcher.routines.logic as logic
from random import randrange
import util.const as const
import urllib.request
import util.versions
import urllib.parse
import urllib.error
import dataclasses
import ctypes
import ssl


@dataclasses.dataclass
class _argtype(logic.subparser_argtype):
    rcc_host: str = 'localhost'
    rcc_port_num: int = 2005
    web_host: str = None
    web_port: webserver.port = webserver.port(
        port_num=80,
        is_ssl=False,
    ),
    username: str = 'Byfron\'s Bad Byrother'
    appearance: str = const.DEFAULT_APPEARANCE
    delay: int = 0


class player(logic.bin_entry):
    local_args: _argtype
    DIR_NAME = 'Player'

    def retrieve_version(self) -> util.versions.rōblox:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        try:
            res = urllib.request.urlopen(
                f'{self.get_base_url()}/roblox_version',
                context=ctx,
            )
        except urllib.error.URLError:
            raise urllib.error.URLError(
                'No server is currently running on ' +
                f'"{self.local_args.web_host}:{self.local_args.web_port.port_num}".',
            )

        return util.versions.rōblox.from_name(str(res.read(), encoding='utf-8'))

    def get_base_url(self) -> str:
        return \
            f'http{"s" if self.local_args.web_port.is_ssl else""}://' + \
            f'{self.local_args.web_host}:{self.local_args.web_port.port_num}'

    def save_app_setting(self) -> str:
        '''
        Modifies settings to point to correct host name.
        '''
        path = self.get_versioned_path('AppSettings.xml')
        with open(path, 'w') as f:
            f.write('\n'.join([
                """<?xml version="1.0" encoding="UTF-8"?>""",
                """<Settings>""",
                f"""\t<BaseUrl>{self.get_base_url()}/.</BaseUrl>""",
                """</Settings>""",
            ]))
        return path

    def enable_mutex(self) -> str:
        '''
        Enables multiple instances of Rōblox to run concurrently.
        '''
        ctypes.windll.kernel32.CreateSemaphoreW(0, 1000, "ROBLOX_singletonEvent")

    def save_ssl(self) -> None:
        if not self.local_args.web_port.is_ssl:
            return

        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        try:
            res = urllib.request.urlopen(
                f'{self.get_base_url()}/retrieve_ssl',
                context=ctx,
            )
        except urllib.error.URLError:
            raise urllib.error.URLError(
                'No server is currently running on ' +
                f'"{self.local_args.web_host}:{self.local_args.web_port.port_num}".',
            )

        path = self.get_versioned_path('SSL', 'cacert.pem')
        with open(path, 'wb') as f:
            f.write(res.read())

    def initialise(self) -> None:
        self.save_app_setting()
        self.enable_mutex()
        self.save_ssl()

        base_url = self.get_base_url()
        self.make_popen([
            self.get_versioned_path('RobloxPlayerBeta.exe'),
            '-a', f'{base_url}/login/negotiate.ashx',
            '-j', f'{base_url}/game/placelauncher.ashx?' +
            urllib.parse.urlencode({
                'placeid': const.PLACE_ID,
                'ip': self.local_args.rcc_host,
                'id': randrange(1, 666),
                'port': self.local_args.rcc_port_num,
                'app': self.local_args.appearance,
                'user': self.local_args.username,
            }),
            '-t', '1',
        ])


class argtype(_argtype):
    obj_type = player
