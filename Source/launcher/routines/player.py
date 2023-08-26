import launcher.routines.webserver as webserver
import launcher.routines.logic as logic
import util.const as const
import urllib.request
import util.resource
import urllib.parse
import dataclasses
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


def get_path(global_args: logic.global_argtype, args: _argtype, * paths: str):
    return util.resource.rōblox_full_path(global_args.roblox_version, 'Player', *paths)


def get_base_url(global_args: logic.global_argtype, args: _argtype):
    return f'http{"s" if args.web_port.is_ssl else""}://{args.web_host}:{args.web_port.port_num}'


def gen_app_setting(global_args: logic.global_argtype, args: _argtype) -> str:
    return '\n'.join([
        """<?xml version="1.0" encoding="UTF-8"?>""",
        """<Settings>""",
        """\t<ContentFolder>content</ContentFolder>""",
        f"""\t<BaseUrl>{get_base_url(global_args, args)}/.</BaseUrl>""",
        """</Settings>""",
    ])


def save_ssl(global_args: logic.global_argtype, args: _argtype) -> None:
    if not args.web_port.is_ssl:
        return
    ssl_path = get_path(global_args, args, 'SSL', 'cacert.pem')

    # Slly hack that disables SSL verification.
    ssl._create_default_https_context = ssl._create_unverified_context
    urllib.request.urlretrieve(
        f'{get_base_url(global_args, args)}/retrieve_ssl',
        ssl_path,
    )


class player(logic.popen_entry):
    def __init__(self, global_args: logic.global_argtype, args: _argtype) -> None:
        settings_path = get_path(global_args, args, 'AppSettings.xml')
        exe_path = get_path(global_args, args, 'RobloxPlayerBeta.exe')

        # Modifies settings to point to correct host name.
        with open(settings_path, 'w') as f:
            f.write(gen_app_setting(global_args, args))
        save_ssl(global_args, args)

        qs = urllib.parse.urlencode({
            'placeid': const.PLACE_ID,
            'ip': args.rcc_host,
            'port': args.rcc_port_num,
            'id': 1630228,
            'app': args.appearance,
            'user': args.username,
        })

        base_url = get_base_url(global_args, args)
        self.make_popen([
            exe_path,
            '-a', f'{base_url}/login/negotiate.ashx',
            '-j', f'{base_url}/game/placelauncher.ashx?{qs}',
            '-t', '1',
        ])


class argtype(_argtype):
    obj_type = player
