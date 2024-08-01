from .. import material, serialisers
from . import grabber
import util.const
import shutil
import os


class cacher:
    def __init__(self, dir_path: str,  clear_on_start: bool = False) -> None:
        self.dir_path = dir_path
        os.makedirs(dir_path, exist_ok=True)
        if clear_on_start:
            shutil.rmtree(dir_path)

    def get_asset_num_path(self, aid: int) -> str:
        return self.get_asset_str_path(f'{aid:011d}')

    def get_asset_str_path(self, aid: str) -> str:
        return os.path.join(self.dir_path, aid)

    def load_online_asset(self, asset_id: int) -> bytes | None:
        data = grabber.load_rōblox_asset(asset_id)
        if data is None:
            return None

        data = serialisers.parse(data)
        return data

    def load_local_asset(self, path: str) -> bytes | None:
        if not os.path.isfile(path):
            return None

        with open(path, 'rb') as f:
            return f.read()

    def save_local_asset(self, path: str, data: bytes) -> None:
        with open(path, 'wb') as f:
            f.write(data)

    def load_asset_num(self, asset_id: int) -> bytes | None:
        '''
        Loads cached asset by ID, else load from online.
        '''

        path = self.get_asset_num_path(asset_id)
        local_data = self.load_local_asset(path)
        if local_data:
            return local_data

        online_data = self.load_online_asset(asset_id)
        if online_data is None:
            return None

        self.save_local_asset(path, online_data)
        return online_data

    def load_asset_str(self, asset_id: str) -> bytes | None:
        path = self.get_asset_str_path(asset_id)
        if path == self.get_asset_num_path(util.const.PLACE_ID_CONST):
            return None

        local_data = self.load_local_asset(path)
        if local_data:
            return local_data

        if asset_id.startswith(material.const.ID_PREFIX):
            loaded = material.load_asset(asset_id)
            if loaded:
                return loaded
            else:
                id_num = material.transform_to_id_num(asset_id)
                return self.load_asset_num(id_num)