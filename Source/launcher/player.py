import launcher.webserver
import launcher.versions
import urllib.parse
import subprocess
import const


def app_setting(host: str = '127.0.0.1', port: int = 80) -> str:
    return f"""
<?xml version="1.0" encoding="UTF-8"?>
<Settings>
	<ContentFolder>content</ContentFolder>
	<BaseUrl>http://{host}:{port}</BaseUrl>
</Settings>
    """


class Player(subprocess.Popen):
    def __init__(
        self,
        version: launcher.versions.Version,
        rcc_host: str = 'localhost',
        rcc_port: int = 2005,
        web_host: str = None,
        web_port: int = 80,
        username: str = 'Byfron\'s Bad Byrother',
        appearance: str = const.DEFAULT_APPEARANCE,
        **kwargs,
    ) -> None:
        web_host, rcc_host = web_host or rcc_host, rcc_host or web_host

        # Modifies settings to point to correct host name
        with open(f'{version.folder()}/Player/AppSettings.xml', 'w') as f:
            f.write(app_setting(web_host, web_port))

        qs = urllib.parse.urlencode({
            'placeid': const.PLACE_ID,
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
