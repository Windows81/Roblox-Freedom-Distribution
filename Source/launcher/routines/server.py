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


class server(logic.popen_entry):
    local_args: _argtype

    def get_path(self, *paths: str) -> str:
        return util.resource.rōblox_full_path(
            self.global_args.roblox_version,
            'Server', *paths,
        )

    def get_base_url(self) -> str:
        return \
            f'http{"s" if self.local_args.web_port.is_ssl else""}://' + \
            f'localhost:{self.local_args.web_port.port_num}'

    def save_app_setting(self) -> str:
        '''
        Modifies settings to point to correct host name.
        '''
        path = self.get_path('RCCSettings.xml')
        with open(path, 'w') as f:
            f.writelines([
                """<?xml version="1.0" encoding="UTF-8"?>""",
                """<Settings>""",
                """\t<ContentFolder>content</ContentFolder>""",
                f"""\t<BaseUrl>{self.get_base_url()}/.</BaseUrl>""",
                """</Settings>""",
            ])
        return path

    def save_gameserver(self) -> str:
        base_url = self.get_base_url()
        path = self.get_path('gameserver.json')
        with open(path, 'w') as f:
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
                        "PreferredPort": self.local_args.rcc_port_num,
                },
                "Arguments": {},
            }, f)
        return path

    def make(self) -> None:
        place_path = assets.get_asset_path(const.PLACE_ID)
        shutil.copyfile(self.local_args.place_path, place_path)

        self.make_popen([
            self.get_path('RCC.exe'),
            '-verbose',
            f'-placeid:{const.PLACE_ID}',
            '-localtest', self.save_gameserver(),
            '-settingsfile', self.get_path('DevSettingsFile.json'),
            '-port 64989',
        ], stdin=subprocess.PIPE)


class argtype(_argtype):
    obj_type = server
