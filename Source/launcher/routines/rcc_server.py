import launcher.routines._logic as logic
import game.assets as assets
import util.const as const
import urllib.request
import util.versions
import config._main
import urllib.error
import dataclasses
import subprocess
import functools
import util.ssl
import shutil
import json


@dataclasses.dataclass
class _arg_type(logic.bin_ssl_arg_type):
    server_config: config._main.obj_type
    rcc_port_num: int = 2005
    skip_popen: bool = False
    web_port: logic.port = \
        logic.port(
            port_num=80,
            is_ssl=False,
            is_ipv6=False,
        ),  # type: ignore

    def get_base_url(self) -> str:
        return \
            f'http{"s" if self.web_port.is_ssl else ""}://' + \
            f'localhost:{self.web_port.port_num}'

    def get_app_base_url(self) -> str:
        return f'{self.get_base_url()}/'


class obj_type(logic.bin_ssl_entry, logic.server_entry):
    local_args: _arg_type
    DIR_NAME = 'Server'

    @functools.cache
    def retr_version(self) -> util.versions.rōblox:
        return self.server_config.game_setup.roblox_version

    def save_app_setting(self) -> str:
        '''
        Modifies settings to point to correct host name.
        '''
        path = self.get_versioned_path('AppSettings.xml')
        app_base_url = self.local_args.get_app_base_url()
        with open(path, 'w') as f:
            f.write('\n'.join([
                """<?xml version="1.0" encoding="UTF-8"?>""",
                """<Settings>""",
                f"""\t<BaseUrl>{app_base_url}</BaseUrl>""",
                """</Settings>""",
            ]))
        return path

    def save_gameserver(self) -> str:
        base_url = self.local_args.get_base_url()
        path = self.get_versioned_path('GameServer.json')
        with open(path, 'w') as f:
            json.dump({
                "Mode": "GameServer",
                "GameId": 13058,
                "Settings": {
                    "Type": "Avatar",
                    "PlaceId": const.DEFAULT_PLACE_ID,
                    "GameId": "Test",
                    "MachineAddress": base_url,
                    "PlaceFetchUrl": f"{base_url}/asset/?id={const.DEFAULT_PLACE_ID}",
                    "MaxPlayers": self.server_config.server_assignment.players.maximum,
                    "PreferredPlayerCapacity": self.server_config.server_assignment.players.preferred,
                    "MaxGameInstances": self.server_config.server_assignment.instances.count,
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

    def make_rcc_popen(self):
        return self.make_popen(
            [
                'wine',
                self.get_versioned_path('RCCService.exe'),
                '-verbose',
                f'-placeid:{const.DEFAULT_PLACE_ID}',
                '-localtest', self.gameserver_path,
                '-settingsfile', self.get_versioned_path(
                    'DevSettingsFile.json'),
                '-port 64989',
            ],
            stdin=subprocess.PIPE,
            cwd=self.get_versioned_path(),
        )

    def initialise(self) -> None:
        place_path = assets.get_asset_path(const.DEFAULT_PLACE_ID)

        shutil.copyfile(self.server_config.game_setup.place_path, place_path)
        self.save_app_setting()
        self.save_ssl_cert()

        self.gameserver_path = self.save_gameserver()
        if not self.local_args.skip_popen:
            self.make_rcc_popen()


class arg_type(_arg_type):
    obj_type = obj_type
