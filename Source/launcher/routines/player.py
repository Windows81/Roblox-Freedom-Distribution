import launcher.routines.webserver as webserver
import launcher.routines.logic as logic
import util.const as const
import urllib.parse
import dataclasses
import functools
import os


@functools.cache
def app_setting(base_url: str) -> str:
    return '\n'.join([
        """<?xml version="1.0" encoding="UTF-8"?>\n<Settings>""",
        """<ContentFolder>content</ContentFolder>""",
        f"""<BaseUrl>{base_url}</BaseUrl>""",
        """</Settings>""",
    ])


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


class player(logic.popen_entry):
    def __init__(self, global_args: logic.global_argtype, args: _argtype) -> None:
        web_host, rcc_host = args.web_host or args.rcc_host, args.rcc_host or args.web_host
        base_url = f'http{"s" if args.web_port.is_ssl else""}://{web_host}:{args.web_port.port_num}'
        player_path = os.path.join(global_args.roblox_version.binary_folder(), 'Player')
        print(base_url)

        # Modifies settings to point to correct host name
        with open(f'{player_path}/AppSettings.xml', 'w') as f:
            f.write(app_setting(base_url))

        qs = urllib.parse.urlencode({
            'placeid': const.PLACE_ID,
            'ip': rcc_host,
            'port': args.rcc_port_num,
            'id': 1630228,
            'app': args.appearance,
            'user': args.username,
        })

        self.make_popen([
            f'{player_path}/RobloxPlayerBeta.exe',
            '-a', f'{base_url}/login/negotiate.ashx',
            '-j', f'{base_url}/game/placelauncher.ashx?{qs}',
            '-t', '1',
        ])


class argtype(_argtype):
    obj_type = player
