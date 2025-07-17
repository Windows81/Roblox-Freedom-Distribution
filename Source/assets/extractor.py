import subprocess
import functools
import urllib3
import base64
import json
import gzip
import os
import re


def get_cookie_from_system() -> str | None:
    """
    Attempts to retrieve and decrypt the Roblox security cookie from the local system on Windows.
    
    Returns:
        The `.ROBLOSECURITY` cookie string if found and successfully decrypted; otherwise, `None`.
    """
    roblox_cookies_path = os.path.join(
        os.getenv("USERPROFILE", ""),
        "AppData",
        "Local",
        "Roblox",
        "LocalStorage",
        "RobloxCookies.dat",
    )

    if not os.path.exists(roblox_cookies_path):
        return

    with open(roblox_cookies_path, 'r', encoding='utf-8') as file:
        file_content = json.load(file)

    encoded_cookies = file_content.get("CookiesData")
    if encoded_cookies is None:
        return

    try:
        import win32crypt
    except ImportError:
        return

    decoded_cookies = base64.b64decode(encoded_cookies)
    decrypted_cookies: bytes = win32crypt.CryptUnprotectData(
        decoded_cookies, None, None, None, 0,
    )[1]

    match = re.search(br'\.ROBLOSECURITY\t([^;]+)', decrypted_cookies)
    if match == None:
        return
    return match[1].decode('utf-8', errors='ignore')


@functools.cache
def get_rōblox_cookie() -> str | None:
    return next(
        v for v in
        (
            get_cookie_from_system(),
            os.environ.get('ROBLOSECURITY', None),
        )
        if v is not None
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
    try:
        http = urllib3.PoolManager()
        response = http.request('GET', url, headers=headers)
        if response.status != 200:
            return None
        return response.data

    except urllib3.exceptions.HTTPError as e:
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
