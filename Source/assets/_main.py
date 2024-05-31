import re
import assets.mesh_convert
import util.resource
import urllib3
import os


def resolve_asset_id(id_str: str | None) -> int | None:
    if not id_str:
        return None
    try:
        return int(id_str)
    except ValueError:
        return None


def resolve_asset_version_id(id_str: str | None) -> int | None:
    # Don't assume this is true for production Rōblox:
    # RFD treats 'asset version ids' the same way as just plain 'version ids'.
    return resolve_asset_id(id_str)


def get_asset_path(aid: int) -> str:
    return util.resource.retr_full_path(util.resource.dir_type.ASSET, f'{aid:011d}')


# TODO: replace:
# 50 52 4F 50 5A 00 00 00 72 00 00 00 00 00 00 00 FF 36 00 00 00 00 08 00 00 00 46 6F 6E 74 46 61 63 65 20 2C 00 00 00 72 62 78 61 73 73 65 74 3A 2F 2F 66 6F 6E 74 73 2F 66 61 6D 69 6C 69 65 73 2F 53 6F 75 72 63 65 53 61 6E 73 50 72 6F 2E 6A 73 6F 6E 90 01 00 2A 33 00 01 09 2A 00 C0 2D 52 65 67 75 6C 61 72 2E 74 74 66
# with
# 50 52 4F 50 13 00 00 00 11 00 00 00 00 00 00 00 F0 02 00 00 00 00 04 00 00 00 46 6F 6E 74 12 00 00 00 03


def replace_rōblox_links(data: bytes) -> bytes:
    '''
    Redirects `assetdelivery.roblox.com` links within any `rbxm` data container to your local URL.
    Solution was derived from trial, error, and hacky patching.
    '''
    def replace_func(m):
        group = m.group(1)
        pad_prefix = b'rbxhttp://asset'
        pad_suffix = b''
        # Having lots of slashes in your path apparently doesn't matter.
        padding = b'/' * (len(group) - len(pad_prefix) - len(pad_suffix))
        return b''.join([
            pad_prefix,
            padding,
            pad_suffix,
            b'\x10\x00',
            m.group(3),
        ])

    return re.sub(
        b'(https://assetdelivery.roblox.com(.{,35}))[\x00-\xff]\x00([\xf0-\xff][\x00-\x10])',
        replace_func, data,
    )


def load_online_asset(asset_id: int) -> bytes | None:
    url = f'https://assetdelivery.roblox.com/v1/asset/?id={asset_id}'
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    if response.status != 200:
        return

    data = response.data
    data = replace_rōblox_links(data)
    try:
        data = assets.mesh_convert.convert_mesh(data)
    except Exception:
        pass
    return data


def load_asset(asset_id: int) -> bytes | None:
    '''
    Loads cached asset by ID, else load from online.
    '''
    path = get_asset_path(asset_id)
    cached = os.path.isfile(path)

    if cached:
        with open(path, 'rb') as f:
            return f.read()

    online_data = load_online_asset(asset_id)
    if not online_data:
        return

    with open(path, 'wb') as f:
        f.write(online_data)

    return online_data
