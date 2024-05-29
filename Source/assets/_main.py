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
        b'(https://assetdelivery.roblox.com(.{,35}))[\x10-\xff]\x00([\xf0-\xff][\x00-\x10])',
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
