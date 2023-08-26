import launcher.routines.webserver as webserver
import launcher.routines.logic as logic
import webserver.assets as assets
import util.const as const
import util.resource
import dataclasses
import subprocess
import shutil
import json


@dataclasses.dataclass
class _argtype(logic.subparser_argtype):
    place_path: str
    rcc_port_num: int = 2005
    web_port: webserver.port = \
        webserver.port(
            port_num=80,
            is_ssl=False,
        ),
    additional_web_ports: set[webserver.port] = dataclasses.field(default_factory=set)


def get_base_url(global_args: logic.global_argtype, args: _argtype):
    return f'http{"s" if args.web_port.is_ssl else""}://localhost:{args.web_port.port_num}'


def gen_app_setting(global_args: logic.global_argtype, args: _argtype) -> str:
    return '\n'.join([
        """<?xml version="1.0" encoding="UTF-8"?>""",
        """<Settings>""",
        """\t<ContentFolder>content</ContentFolder>""",
        f"""\t<BaseUrl>{get_base_url(global_args, args)}/.</BaseUrl>""",
        """</Settings>""",
    ])


class server(logic.popen_entry):
    def __init__(self, global_args: logic.global_argtype, args: _argtype) -> None:

        prefix_args = (global_args.roblox_version, 'Server')
        settings_path = util.resource.rōblox_full_path(*prefix_args, 'RCCSettings.xml')
        gameserver_path = util.resource.rōblox_full_path(*prefix_args, 'gameserver.json')
        devsettings_path = util.resource.rōblox_full_path(*prefix_args, 'DevSettingsFile.json')
        exe_path = util.resource.rōblox_full_path(*prefix_args, 'RCC.exe')

        place_path = assets.get_asset_path(const.PLACE_ID)
        shutil.copyfile(args.place_path, place_path)
        web_port_num = args.web_port.port_num

        # Modifies settings to point to correct host name.
        with open(settings_path, 'w') as f:
            f.write(gen_app_setting(global_args, args))

        base_url = get_base_url(global_args, args)
        with open(gameserver_path, 'w') as f:
            json.dump({
                "Mode": "GameServer",
                "GameId": 13058,
                "Settings": {
                    "Type": "Avatar",
                    "PlaceId": const.PLACE_ID,
                    "GameId": "Test",
                    "MachineAddress": base_url,
                    "PlaceFetchUrl": f"{base_url}/asset/?id={const.PLACE_ID}",
                    "GsmInterval": 5,
                    "MaxPlayers": 4096,
                    "MaxGameInstances": 1,
                    "ApiKey": "",
                    "PreferredPlayerCapacity": 666,
                    "DataCenterId": "69420",
                    "PlaceVisitAccessKey": "",
                    "UniverseId": 13058,
                    "MatchmakingContextId": 1,
                    "CreatorId": 1,
                    "CreatorType": "User",
                    "PlaceVersion": 1,
                    "BaseUrl": f"{base_url}/.127.0.0.1",
                    "JobId": "Test",
                    "script": "print('Initializing NetworkServer.')",
                    "PreferredPort": args.rcc_port_num,
                },
                "Arguments": {},
            }, f)

        self.make_popen([
            exe_path,
            '-verbose',
            f'-placeid:{const.PLACE_ID}',
            '-localtest', gameserver_path,
            '-settingsfile', devsettings_path,
            '-port 64989',
        ], stdin=subprocess.PIPE)


class argtype(_argtype):
    obj_type = server
