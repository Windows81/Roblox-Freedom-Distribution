from . import (
    rbxl,
    mesh,
)

import urllib3
import os


class asseter:
    def __init__(self, dir_path: str) -> None:
        self.dir_path = dir_path

    def get_asset_path(self, aid: int) -> str:
        return os.path.join(self.dir_path, f'{aid:011d}')

    def resolve_asset_id(self, id_str: str | None) -> int | None:
        if id_str is None:
            return None
        try:
            return int(id_str)
        except ValueError:
            return None

    def resolve_asset_version_id(self, id_str: str | None) -> int | None:
        # Don't assume this is true for production Rōblox:
        # RFD treats 'asset version ids' the same way as just plain 'version ids'.
        return self.resolve_asset_id(id_str)

    def load_online_asset(self, asset_id: int) -> bytes | None:
        for key in {'id'}:
            url = f'https://assetdelivery.roblox.com/v1/asset/?{
                key}={asset_id}'
            http = urllib3.PoolManager()
            response = http.request('GET', url)
            if response.status == 200:
                break
        else:
            return

        data = response.data
        data = rbxl.parse(data)
        data = mesh.parse(data)
        return data

    def load_asset(self, asset_id: int) -> bytes | None:
        '''
        Loads cached asset by ID, else load from online.
        '''
        path = self.get_asset_path(asset_id)
        cached = os.path.isfile(path)

        if cached:
            with open(path, 'rb') as f:
                return f.read()

        online_data = self.load_online_asset(asset_id)
        if online_data is None:
            return

        with open(path, 'wb') as f:
            f.write(online_data)

        return online_data
