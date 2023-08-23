import launcher.routines.webserver as webserver
import launcher.routines.logic as logic
import webserver.assets as assets
import util.const as const
import dataclasses
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
    def __init__(self, global_args: logic.global_argtype, args: _argtype) -> None:
        folder = f'{global_args.roblox_version.binary_folder()}/Server'

        place_path = assets.get_asset_path(const.PLACE_ID)
        shutil.copyfile(args.place_path, place_path)
        web_port_num = args.web_port.port_num

        gameserver_path = f'{folder}/gameserver.json'
        with open(gameserver_path, 'w') as f:
            json.dump({
                "Mode": "GameServer",
                "GameId": 13058,
                "Settings": {
                    "Type": "Avatar",
                    "PlaceId": const.PLACE_ID,
                    "GameId": "Test",
                    "MachineAddress": f"https://localhost:{web_port_num}",
                    "PlaceFetchUrl": f"https://localhost:{web_port_num}/asset/?id={const.PLACE_ID}",
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
                    "BaseUrl": f"https://localhost:{web_port_num}/.127.0.0.1",
                    "JobId": "Test",
                    "script": "print('Initializing NetworkServer.')",
                    "PreferredPort": args.rcc_port_num,
                },
                "Arguments": {},
            }, f)

        self.make_popen([
            f'{folder}/RCC.exe',
            '-verbose',
            f'-placeid:{const.PLACE_ID}',
            '-localtest', gameserver_path,
            '-settingsfile', f'{folder}/DevSettingsFile.json',
            '-port 64989',
        ])


class argtype(_argtype):
    obj_type = server
