import versions
import uwamp
import json
import io


class Server(uwamp.UwAmpWrap):
    def __init__(self, version: versions.Version, data: io.BufferedReader, **kwargs) -> None:
        folder = f'{version.folder()}/Server'

        place_path = f'Webserver/www/_CACHE/{uwamp.PLACE_ID}'
        with open(place_path, 'wb') as f:
            f.write(data.read())

        gameserver_path = f'{folder}/gameserver.json'
        with open(gameserver_path, 'w') as f:
            json.dump({
                "Mode": "GameServer",
                "GameId": 13058,
                "Settings": {
                    "Type": "Avatar",
                    "PlaceId": uwamp.PLACE_ID,
                    "GameId": "Test",
                    "MachineAddress": "http://127.0.0.1",
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
                    "PreferredPort": 2005
                },
                "Arguments": {}
            }, f)

        super().__init__([
            f'{folder}/RCC.exe',
            '-Console', '-Verbose', '-placeid:1818',
            '-localtest', gameserver_path, '-port 64989',
        ])
