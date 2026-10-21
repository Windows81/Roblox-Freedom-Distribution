from collections.abc import Generator
from typing import Any
import urllib.request
import urllib.error
import subprocess
import functools
import base64
import json
import gzip
import os
import re


def _get_cookie_from_system() -> str | None:
    '''
    Attempts to retrieve and decrypt the Rōblox security cookie from the
    local system on Windows.

    Only works on Windows systems.
    Do not count on a valid cookie being returned on a remote server.
    https://github.com/Ramona-Flower/Roblox-Client-Cookie-Stealer/blob/main/main.py
    '''
    roblox_cookies_path = os.path.join(
        os.getenv('USERPROFILE', ''),
        'AppData', 'Local', 'Roblox',
        'LocalStorage', 'RobloxCookies.dat',
    )
    if not os.path.exists(roblox_cookies_path):
        return None

    with open(roblox_cookies_path, 'r', encoding='utf-8') as f:
        file_content = json.load(f)

    encoded_cookies = file_content.get('CookiesData')
    if encoded_cookies is None:
        return None

    try:
        import win32crypt
    except ImportError:
        return None

    decoded_cookies = base64.b64decode(encoded_cookies)
    decrypted_cookies: bytes = win32crypt.CryptUnprotectData(
        DataIn=decoded_cookies,
        OptionalEntropy=None,
        Reserved=None,
        PromptStruct=None,
        Flags=0x00000000,
    )[1]

    match = re.search(br'\.ROBLOSECURITY\t([^;]+)', decrypted_cookies)
    if match is None:
        return None
    return match[1].decode('utf-8', errors='ignore')


def test_cookie(cookie: str | None) -> bool:
    return cookie is not None


@functools.cache
def get_rōblox_cookie() -> str | None:
    return next(
        (
            v for v in (
                os.environ.get('ROBLOSECURITY', None),
                _get_cookie_from_system(),
            )
            if test_cookie(v)
        ),
        None,
    )


def unzip(data: bytes) -> bytes:
    try:
        return gzip.decompress(data)
    except gzip.BadGzipFile:
        return data


def download_item(
    url: str,
    cookie: str | None = None,
    place_id: int | None = None,
) -> bytes | None:

    if cookie is None:
        cookie = get_rōblox_cookie()

    headers: dict[str, str] = {
        'User-Agent': 'Roblox/WinInet',
        'Referer': 'https://www.roblox.com/',
        'Cookie': f'.ROBLOSECURITY={cookie}',
        # CDN may return gzip-compressed data; request it explicitly.
        'Accept-Encoding': 'gzip',
    }

    if place_id is not None:
        headers['Roblox-Place-Id'] = str(place_id)
        headers['Roblox-Browser-Asset-Request'] = 'false'

    try:
        req = urllib.request.Request(url)
        req.headers.update(headers)
        with urllib.request.urlopen(req) as response:
            if response.status != 200:
                return None
            return unzip(response.read())
    except urllib.error.HTTPError:
        return None


@functools.cache
def get_creator_place_idens(asset_iden: int) -> list[int]:
    '''
    Creator place-iden lookup.

    Sends queries to `economy.roblox.com` for the asset's creator (User or Group),
    then games.roblox.com for every place they own, and returns the root
    place idens.

    Results are cached for the lifetime of the process; creator ownership
    doesn't change mid-session, and the same asset is often requested many
    times by different clients.

    Credit to https://github.com/mytailcaughtonfire for this ingenious idea.
    '''
    headers = {
        'User-Agent': 'Roblox/WinInet',
        'Accept': 'application/json',
    }

    try:
        url = f'https://economy.roblox.com/v2/assets/{asset_iden}/details'
        req = urllib.request.Request(url)
        req.headers.update(headers)
        with urllib.request.urlopen(req) as response:
            if response.status != 200:
                return []
            details = json.loads(response.read())
    except Exception:
        return []

    creator = details.get('Creator', {})
    creator_id = creator.get('CreatorTargetId')
    creator_type = creator.get('CreatorType', 'user').lower()

    if not creator_id:
        return []

    if creator_type == 'group':
        games_url = f'https://games.roblox.com/v2/groups/{creator_id}/games?limit=50&sortOrder=Asc'
    else:
        games_url = f'https://games.roblox.com/v2/users/{creator_id}/games?limit=50&sortOrder=Asc'

    try:
        req = urllib.request.Request(games_url)
        req.headers.update(headers)
        with urllib.request.urlopen(req) as response:
            if response.status != 200:
                return []
            games = json.loads(response.read())
    except Exception:
        return []

    result = []
    for game in games.get('data', []):
        v = game.get('rootPlace', {}).get('id')
        if v is None:
            continue
        result.append(v)

    return result


def download_rōblox_asset(
    asset_iden: int,
    cookie: str | None = None,
) -> bytes | None:

    url = f'https://assetdelivery.roblox.com/v1/asset/?id={asset_iden}'
    if cookie is None:
        cookie = get_rōblox_cookie()

    def gen_place_idens_candidates() -> Generator[int | None, Any, None]:
        # Step 1: no place iden.
        yield None

        # Skip later steps if no cookie is given, as no benefit is given in this case.
        if cookie is None:
            return

        # Step 2: user-defined `rfdplaceid` environment variable.
        try:
            yield int(os.environ.get('rfdplaceid', ''))
        except Exception:
            pass

        # Step 3: creator's place idens.
        for iden in get_creator_place_idens(asset_iden):
            yield iden

    for place_id in gen_place_idens_candidates():
        return download_item(
            url=url,
            cookie=cookie,
            place_id=place_id,
        )

    # Genuinely inaccessible with any known place iden.
    return None


def process_command_line(cmd_line: str) -> bytes:
    '''
    Command-line asset processor.
    '''
    popen = subprocess.Popen(
        args=cmd_line,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        shell=True,
    )
    stdout, _ = popen.communicate()
    return stdout
