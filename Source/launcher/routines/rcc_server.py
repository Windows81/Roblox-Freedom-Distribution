import web_server._logic as web_server_logic
import web_server as web_server

from ..startup_scripts import rcc_server
import assets.serialisers.rbxl as rbxl
from . import _logic as logic
import util.const as const
import config.structure
import util.resource
import util.versions
import dataclasses
import subprocess
import functools
import util.ssl
import config
import assets
import json
import os


class obj_type(logic.bin_ssl_entry, logic.server_entry):
    local_args: 'arg_type'
    BIN_SUBTYPE = util.resource.bin_subtype.SERVER

    @functools.cache
    def retr_version(self) -> util.versions.rōblox:
        return self.game_config.game_setup.roblox_version

    def save_place_file(self) -> None:
        config = self.game_config

        from_path = config.game_setup.place.path
        if from_path is None:
            return
        to_path = config.asset_cache.get_asset_num_path(const.DEFAULT_PLACE_ID)

        with open(from_path, 'rb') as rf, open(to_path, 'wb') as wf:
            wf.write(rbxl.parse(rf.read()))

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

    def save_starter_scripts(self) -> None:
        server_path = self.get_versioned_path(os.path.join(
            'Content',
            'Scripts',
            'CoreScripts',
            'RFDStarterScript.lua',
        ))
        with open(server_path, 'w', encoding='utf-8') as f:
            rcc_script = rcc_server.get_script(self.game_config)
            f.write(rcc_script)

    def save_gameserver(self) -> str:
        base_url = self.local_args.get_base_url()
        path = self.get_versioned_path('GameServer.json')
        with open(path, 'w', encoding='utf-8') as f:
            json.dump({
                "Mode": "GameServer",
                "GameId": 13058,
                "Settings": {
                    "Type":
                        "Avatar",
                    "PlaceId":
                        const.DEFAULT_PLACE_ID,
                    "GameId":
                        "Test",
                    "MachineAddress":
                        base_url,
                    "PlaceFetchUrl":
                        f"{base_url}/asset/?id={const.DEFAULT_PLACE_ID}",
                    "MaxPlayers":
                        self.game_config.server_assignment.players.maximum,
                    "PreferredPlayerCapacity":
                        self.game_config.server_assignment.players.preferred,
                    "CharacterAppearance":
                        f"{base_url}/v1.1/avatar-fetch",
                    "MaxGameInstances":
                        self.game_config.server_assignment.instances.count,
                    "GsmInterval":
                        5,
                    "ApiKey":
                        "",
                    "DataCenterId":
                        "69420",
                    "PlaceVisitAccessKey":
                        "",
                    "UniverseId":
                        13058,
                    "MatchmakingContextId":
                        1,
                    "CreatorId":
                        1,
                    "CreatorType":
                        "User",
                    "PlaceVersion":
                        1,
                    "BaseUrl":
                        f"{base_url}/.127.0.0.1",
                    "JobId":
                        "Test",
                    "PreferredPort":
                        self.local_args.rcc_port_num,
                },
                "Arguments": {},
            }, f)
        return path

    def make_rcc_popen(self):
        return self.make_popen(
            [
                self.get_versioned_path('RCCService.exe'),

                f'-placeid:{const.DEFAULT_PLACE_ID}',

                '-localtest', self.get_versioned_path(
                    'GameServer.json',
                ),

                '-settingsfile', self.get_versioned_path(
                    'DevSettingsFile.json',
                ),

                '-port 64989',
                *(('-verbose',) if self.local_args.verbose else ()),
            ],
            stdin=subprocess.PIPE,
            cwd=self.get_versioned_path(),

            # This suppresses the "To enable debug output, run with the -verbose flag"
            # which prints if verbosity is disabled.
            stdout=None if self.local_args.verbose else subprocess.PIPE,
        )

    def process(self) -> None:
        self.save_starter_scripts()
        self.save_place_file()
        self.save_app_setting()
        self.save_ssl_cert()

        self.save_gameserver()
        if not self.local_args.skip_popen:
            self.make_rcc_popen()


@dataclasses.dataclass
class arg_type(logic.bin_ssl_arg_type):
    obj_type = obj_type

    game_config: config.obj_type
    rcc_port_num: int = 2005
    skip_popen: bool = False
    verbose: bool = False
    web_port: web_server_logic.port_typ = \
        web_server_logic.port_typ(
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
