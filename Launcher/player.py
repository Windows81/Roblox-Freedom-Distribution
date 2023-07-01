import urllib.parse
import subprocess
import versions
import uwamp

DEFAULT_APP = "rbxassetid://6445262286;rbxassetid://2510230574;rbxassetid://2510233257;rbxassetid://2510236649;rbxassetid://2510238627;rbxassetid://6969309778;rbxassetid://2846257298;rbxassetid://6340101;rbxassetid://34247191;rbxassetid://48474294;rbxassetid://107458429;rbxassetid://121390054;rbxassetid://154386348;rbxassetid://183808364;rbxassetid://190245296;rbxassetid://192483960;rbxassetid://201733574;rbxassetid://261826995;rbxassetid://9120251003;rbxassetid://9481782649;rbxassetid://9482991343;rbxassetid://5731052645;rbxassetid://10726856854;password=1630228|Cyan;Cyan;Cyan;Cyan;Cyan;Cyan"


class Player(subprocess.Popen):
    def __init__(self, version: versions.Version, ip: str = '127.0.0.1', port: int = 2005, appearance: str = DEFAULT_APP, **kwargs) -> None:
        qs = urllib.parse.urlencode({
            'year': 2018,
            'placeid': uwamp.PLACE_ID,
            'ip': ip,
            'port': port,
            'id': 1630228,
            'app': appearance,
            'user': 'VisualPlugin',
        })
        super().__init__([
            f'{version.folder()}/Player/RobloxPlayerBeta.exe',
            '-t', '1', '-a', 'http://localhost/login/negotiate.ashx',
            '-j', f'http://localhost/game/placelauncher.ashx?{qs}',
        ])
