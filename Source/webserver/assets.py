import util.resource
import urllib3
import os


def get_asset_path(aid: int) -> str:
    return util.resource.get_full_path(util.resource.dir_type.ASSET, f'{aid:011d}')


def load_asset(aid: int) -> bytes | None:
    path = get_asset_path(aid)
    cached = os.path.isfile(path)

    if cached:
        with open(path, 'rb') as f:
            return f.read()

    url = f'https://assetdelivery.roblox.com/v1/asset/?id={aid}'
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    if response.status != 200:
        return

    with open(path, 'wb') as f:
        f.write(response.data)
    return response.data
