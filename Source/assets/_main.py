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


def load_online_asset(asset_id: int) -> bytes | None:
    url = f'https://assetdelivery.roblox.com/v1/asset/?id={asset_id}'
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    if response.status != 200:
        return

    data = response.data
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
