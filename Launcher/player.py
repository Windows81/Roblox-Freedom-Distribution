import urllib.parse
import subprocess
import versions
import uwamp


def app_setting(host: str = '127.0.0.1', port: int = 80) -> str:
    return f"""
<?xml version="1.0" encoding="UTF-8"?>
<Settings>
	<ContentFolder>content</ContentFolder>
	<BaseUrl>http://{host}:{port}</BaseUrl>
</Settings>
    """


DEFAULT_APPEARANCE = "rbxassetid://6445262286;rbxassetid://2510230574;rbxassetid://2510233257;rbxassetid://2510236649;rbxassetid://2510238627;rbxassetid://6969309778;rbxassetid://2846257298;rbxassetid://6340101;rbxassetid://34247191;rbxassetid://48474294;rbxassetid://107458429;rbxassetid://121390054;rbxassetid://154386348;rbxassetid://183808364;rbxassetid://190245296;rbxassetid://192483960;rbxassetid://201733574;rbxassetid://261826995;rbxassetid://9120251003;rbxassetid://9481782649;rbxassetid://9482991343;rbxassetid://5731052645;rbxassetid://10726856854;password=1630228|Cyan;Cyan;Cyan;Cyan;Cyan;Cyan"


class Player(subprocess.Popen):
    def __init__(
        self,
        version: versions.Version,
        rcc_host: str = 'localhost',
        web_host: str = None,
        rcc_port: int = 2005,
        web_port: int = 80,
        appearance: str = DEFAULT_APPEARANCE,
        username: str = 'Byfron\'s Bad Byrother',
        **kwargs,
    ) -> None:
        web_host, rcc_host = web_host or rcc_host, rcc_host or web_host

        # Modifies settings to point to correct host name
        with open(f'{version.folder()}/Player/AppSettings.xml', 'w') as f:
            f.write(app_setting(web_host, web_port))

        qs = urllib.parse.urlencode({
            'placeid': uwamp.PLACE_ID,
            'ip': rcc_host,
            'port': rcc_port,
            'id': 1630228,
            'app': appearance,
            'user': username,
        })

        super().__init__([
            f'{version.folder()}/Player/RobloxPlayerBeta.exe',
            '-j', f'http://{web_host}:{web_port}/game/placelauncher.ashx?{qs}',
            '-t', '1', '-a', f'http://{web_host}:{web_port}/login/negotiate.ashx',
        ])
