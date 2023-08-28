import launcher.routines.webserver as webserver
import launcher.routines.logic as logic
import webserver.assets as assets
import launcher.gameconfig
import util.const as const
import launcher.gameconfig
import util.ssl_context
import util.versions
import dataclasses
import subprocess
import shutil
import json


@dataclasses.dataclass
class _argtype(logic.subparser_argtype):
    server_config: launcher.gameconfig.configtype
    rcc_port_num: int = 2005
    web_port: webserver.port = \
        webserver.port(
            port_num=80,
            is_ssl=False,
        ),


class server(logic.bin_entry, logic.server_entry):
    local_args: _argtype
    DIR_NAME = 'Server'

    def retrieve_version(self) -> util.versions.rōblox:
        return self.config.place_setup.roblox_version

    def get_base_url(self) -> str:
        return \
            f'http{"s" if self.local_args.web_port.is_ssl else""}://' + \
            f'localhost:{self.local_args.web_port.port_num}'

    def save_app_setting(self) -> str:
        '''
        Modifies settings to point to correct host name.
        '''
        path = self.get_versioned_path('RCCSettings.xml')
        with open(path, 'w') as f:
            f.write('\n'.join([
                """<?xml version="1.0" encoding="UTF-8"?>""",
                """<Settings>""",
                f"""\t<BaseUrl>{self.get_base_url()}/</BaseUrl>""",
                """</Settings>""",
            ]))
        return path

    def save_gameserver(self) -> str:
        base_url = self.get_base_url()
        path = self.get_versioned_path('gameserver.json')
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
                    "MaxPlayers": self.config.server_assignment.players.maximum,
                    "PreferredPlayerCapacity": self.config.server_assignment.players.preferred,
                    "MaxGameInstances": self.config.server_assignment.instances.count,
                    "GsmInterval": 5,
                    "ApiKey": "",
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

    def save_ssl(self) -> None:
        if not self.local_args.web_port.is_ssl:
            return
        path = self.get_versioned_path('SSL', 'cacert.pem')
        with open(path, 'wb') as f:
            f.write(util.ssl_context.get_client_cert())

    def initialise(self) -> None:
        place_path = assets.get_asset_path(const.PLACE_ID)

        shutil.copyfile(self.config.place_setup.path, place_path)
        self.save_app_setting()
        self.save_ssl()

        self.make_popen([
            self.get_versioned_path('RCC.exe'),
            '-verbose',
            f'-placeid:{const.PLACE_ID}',
            '-localtest', self.save_gameserver(),
            '-settingsfile', self.get_versioned_path('DevSettingsFile.json'),
            '-port 64989',
        ], stdin=subprocess.PIPE)


class argtype(_argtype):
    obj_type = server
