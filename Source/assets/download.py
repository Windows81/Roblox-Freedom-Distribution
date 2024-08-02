import urllib3


def download_item(url: str) -> bytes | None:
    try:
        http = urllib3.PoolManager()
        response = http.request('GET', url)
        if response.status != 200:
            return None
        return response.data
    except urllib3.exceptions.HTTPError as e:
        return None


def download_rōblox_asset(asset_id: int) -> bytes | None:
    for key in {'id'}:
        result = download_item(
            f'https://assetdelivery.roblox.com/v1/asset/?%s=%s' %
            (key, asset_id)
        )
        if result is not None:
            return result
