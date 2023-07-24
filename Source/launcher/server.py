import launcher.webserver
import webserver.assets
import versions
import const
import json
import io


class Server(launcher.webserver.WebserverWrap):
    def __init__(
        self,
        version: versions.Version,
        data: io.BufferedReader,
        rcc_port: int = 2005,
        web_port: int = 80,
        **kwargs,
    ) -> None:
        folder = f'{version.binary_folder()}/Server'

        place_path = webserver.assets.get_asset_path(const.PLACE_ID)
        with open(place_path, 'wb') as f:
            f.write(data.read())

        gameserver_path = f'{folder}/gameserver.json'
        with open(gameserver_path, 'w') as f:
            json.dump({
                "Mode": "GameServer",
                "GameId": 13058,
                "Settings": {
                    "Type": "Avatar",
                    "PlaceId": const.PLACE_ID,
                    "GameId": "Test",
                    "MachineAddress": f"http://localhost:{web_port}",
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
                    "BaseUrl": "localhost/.localhost",
                    "JobId": "Test",
                    "script": "print('Initializing NetworkServer.')",
                    "PreferredPort": rcc_port,
                },
                "Arguments": {},
            }, f)

        super().__init__([
            f'{folder}/RCC.exe',
            '-Console', '-Verbose', '-placeid:1818',
            '-localtest', gameserver_path, '-port 64989',
        ], version=version)
