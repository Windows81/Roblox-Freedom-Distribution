import versions
import uwamp
import json


class Server(uwamp.UwAmpWrap):
    def __init__(self, version: versions.Version) -> None:
        folder = f'{version.folder()}/Server'
        gameserver_path = f'{folder}/gameserver.json'
        with open(gameserver_path, 'w') as j:
            json.dump({
                "Mode": "GameServer",
                "GameId": 13058,
                "Settings": {
                    "Type": "Avatar",
                    "PlaceId": 1818,
                    "GameId": "Test",
                    "MachineAddress": "http://127.0.0.1",
                    "GsmInterval": 5,
                    "MaxPlayers": 666,
                    "MaxGameInstances": 666,
                    "ApiKey": "",
                    "PreferredPlayerCapacity": 666,
                    "DataCenterId": "69420",
                    "PlaceVisitAccessKey": "",
                    "UniverseId": 13058,
                    "PlaceFetchUrl": "http://localhost/.localhost/asset/?id=1818",
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
            }, j)
        super().__init__([
            f'{folder}/RCC.exe',
            '-Console', '-Verbose', '-placeid:1818',
            '-localtest', gameserver_path, '-port 64989',
        ])
