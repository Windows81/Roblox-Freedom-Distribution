import subprocess
import urllib3
import os

COOKIE = os.environ.get('ROBLOSECURITY', '')


def download_item(url: str, cookie: str = COOKIE) -> bytes | None:
    headers = {
        'User-Agent': 'Roblox/WinInet',
        'Referer': 'https://www.roblox.com/',
        'Cookie': "; ".join(
            str(x)+"="+str(y)
            for x, y in {
                '.ROBLOSECURITY': cookie,
            }
        ),
    }
    try:
        http = urllib3.PoolManager()
        response = http.request('GET', url, headers=headers)
        if response.status != 200:
            return None
        return response.data
    except urllib3.exceptions.HTTPError as e:
        return None


def download_rōblox_asset(asset_id: int, cookie: str = COOKIE) -> bytes | None:
    for key in {'id'}:
        result = download_item(
            'https://assetdelivery.roblox.com/v1/asset/?%s=%s' %
            (key, asset_id)
        )
        if result is not None:
            return result


def process_command_line(cmd_line: str) -> bytes:
    popen = subprocess.Popen(
        args=cmd_line,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        shell=True,
    )
    (stdout, _) = popen.communicate()
    return stdout
