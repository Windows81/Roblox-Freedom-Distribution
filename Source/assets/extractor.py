import subprocess
import functools
import urllib3
import gzip
import os

import util.player_cookie_store


def _get_cookie_from_system() -> str | None:
    return util.player_cookie_store.get_cookie_value(
        preferred_hosts={".roblox.com", "roblox.com"},
    )


def test_cookie(cookie: str | None) -> bool:
    return (
        cookie is not None and
        cookie.startswith(
            "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_"
        )
    )


@functools.cache
def get_rōblox_cookie() -> str | None:
    return next(
        (
            v for v in
            (
                _get_cookie_from_system(),
                os.environ.get('ROBLOSECURITY', None),
            )
            if test_cookie(v)
        ), None,
    )


def unzip(data: bytes) -> bytes:
    try:
        return gzip.decompress(data)
    except gzip.BadGzipFile:
        return data


def download_item(url: str, cookie: str | None = None) -> bytes | None:
    if cookie is None:
        cookie = get_rōblox_cookie()
    headers = {
        'User-Agent': 'Roblox/WinInet',
        'Referer': 'https://www.roblox.com/',
        'Cookie': "; ".join(
            f'{x}={y}'
            for x, y in {
                '.ROBLOSECURITY': cookie,
            }.items()
        ),
    }

    place_id = os.environ.get("rfdplaceid")
    if place_id:
        headers["Roblox-Place-Id"] = place_id
        headers["Roblox-Browser-Asset-Request"] = "false"

    try:
        http = urllib3.PoolManager()
        response = http.request('GET', url, headers=headers)
        if response.status != 200:
            return None
        return response.data

    except urllib3.exceptions.HTTPError as _:
        return None


def download_rōblox_asset(asset_id: int, cookie: str | None = None) -> bytes | None:
    for key in {'id'}:
        result = download_item(
            'https://assetdelivery.roblox.com/v1/asset/?%s=%s' %
            (key, asset_id),
            cookie=cookie,
        )
        if result is not None:
            return unzip(result)


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
