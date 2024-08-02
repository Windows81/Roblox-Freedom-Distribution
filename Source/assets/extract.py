import functools
from . import download, material, serialisers
import util.const
import shutil
import os


class extractor:
    def __init__(self, dir_path: str,  clear_on_start: bool = False) -> None:
        self.dir_path = dir_path
        os.makedirs(dir_path, exist_ok=True)
        if clear_on_start:
            shutil.rmtree(dir_path)

    @functools.cache
    def get_asset_path(self, asset_id: int | str) -> str:
        return os.path.normpath(
            os.path.join(
                self.dir_path,
                (
                    f'{asset_id:011d}'
                    if isinstance(asset_id, int) else
                    asset_id
                ),
            )
        )

    def load_online_asset(self, asset_id: int) -> bytes | None:
        data = download.download_rōblox_asset(asset_id)
        if data is None:
            return None

        data = serialisers.parse(data)
        return data

    def load_file(self, path: str) -> bytes | None:
        if not os.path.isfile(path):
            return None

        with open(path, 'rb') as f:
            return f.read()

    @functools.cache
    def _blacklist(self, asset_id: int | str) -> bool:
        asset_path = self.get_asset_path(asset_id)
        place_path = self.get_asset_path(util.const.PLACE_ID_CONST)
        if asset_path == place_path:
            return True
        return False

    def save_file(self, path: str, data: bytes) -> None:
        with open(path, 'wb') as f:
            f.write(data)

    def load_asset_num(self, asset_id: int) -> bytes | None:
        return self.load_online_asset(asset_id)

    def load_asset_str(self, asset_id: str) -> bytes | None:
        if asset_id.startswith(material.const.ID_PREFIX):
            return material.load_asset(asset_id)
        return None

    def load_asset(self, asset_id: int | str, bypass_blacklist: bool = False) -> bytes | None:
        if not bypass_blacklist and self._blacklist(asset_id):
            return None

        path = self.get_asset_path(asset_id)
        local_data = self.load_file(path)
        if local_data:
            return local_data

        if isinstance(asset_id, str):
            return self.load_asset_str(asset_id)
        elif isinstance(asset_id, int):
            return self.load_asset_num(asset_id)

    def save_asset(self, asset_id: int | str, data: bytes) -> None:
        path = self.get_asset_path(asset_id)
        self.save_file(path, data)
