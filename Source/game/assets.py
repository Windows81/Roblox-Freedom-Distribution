import util.resource
import urllib3
import os


def get_asset_path(aid: int) -> str:
    return util.resource.retr_full_path(util.resource.dir_type.ASSET, f'{aid:011d}')


def load_online_asset(asset_id: int) -> bytes | None:
    url = f'https://assetdelivery.roblox.com/v1/asset/?id={asset_id}'
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    if response.status != 200:
        return
    return response.data


def load_asset(asset_id: int) -> bytes | None:
    '''
    Loads cached asset by ID, else load from online.
    '''
    path = get_asset_path(asset_id)
    cached = os.path.isfile(path)

    if cached:
        with open(path, 'rb') as f:
            return f.read()

    online = load_online_asset(asset_id)
    if not online:
        return
    with open(path, 'wb') as f:
        f.write(online)
