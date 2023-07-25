import urllib.parse
import subprocess
import versions
import const


def app_setting(base_url: str) -> str:
    return f"""
<?xml version="1.0" encoding="UTF-8"?>
<Settings>
	<ContentFolder>content</ContentFolder>
	<BaseUrl>{base_url}</BaseUrl>
</Settings>"""


class Player(subprocess.Popen):
    def __init__(
        self,
        version: versions.Version,
        rcc_host: str = 'localhost',
        rcc_port: int = 2005,
        web_host: str = None,
        web_port: int = 80,
        web_ssl: bool = False,
        username: str = 'Byfron\'s Bad Byrother',
        appearance: str = const.DEFAULT_APPEARANCE,
        **kwargs,
    ) -> None:
        web_host, rcc_host = web_host or rcc_host, rcc_host or web_host
        base_url = f'http{"s" if web_ssl else""}://{web_host}:{web_port}'
        print(base_url)

        # Modifies settings to point to correct host name
        with open(f'{version.binary_folder()}/Player/AppSettings.xml', 'w') as f:
            f.write(app_setting(base_url))

        qs = urllib.parse.urlencode({
            'placeid': const.PLACE_ID,
            'ip': rcc_host,
            'port': rcc_port,
            'id': 1630228,
            'app': appearance,
            'user': username,
        })

        super().__init__([
            f'{version.binary_folder()}/Player/RobloxPlayerBeta.exe',
            '-j', f'{base_url}/game/placelauncher.ashx?{qs}',
            '-t', '1', '-a', f'{base_url}/login/negotiate.ashx',
        ])
