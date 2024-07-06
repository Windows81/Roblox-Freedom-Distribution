import urllib3


def load_rōblox_asset(asset_id: int) -> bytes | None:
    for key in {'id'}:
        url = (
            f'https://assetdelivery.roblox.com/v1/asset/?%s=%s' %
            (key, asset_id)
        )
        try:
            http = urllib3.PoolManager()
            response = http.request('GET', url)
            if response.status == 200:
                return response.data

        except urllib3.exceptions.HTTPError as e:
            return None
