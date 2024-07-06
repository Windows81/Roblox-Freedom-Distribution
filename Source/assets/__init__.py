from .serialisers import (
    rbxl,
    mesh,
)

from . import material
from . import grabber
import itertools
import shutil
import os


class asseter:
    def __init__(self, dir_path: str, clear_on_start: bool = False) -> None:
        self.dir_path = dir_path
        os.makedirs(dir_path, exist_ok=True)
        if clear_on_start:
            shutil.rmtree(dir_path)

    def get_asset_num_path(self, aid: int) -> str:
        return self.get_asset_str_path(f'{aid:011d}')

    def get_asset_str_path(self, aid: str) -> str:
        return os.path.join(self.dir_path, aid)

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

    def resolve_asset_query(self, query: dict[str, str]) -> int | str | None:
        funcs = [
            (query.get('id', None), self.resolve_asset_id),
            (query.get('assetversionid', None), self.resolve_asset_version_id),
        ]

        return next(
            itertools.islice(itertools.chain(
                (
                    result
                    for (prop_val, func) in funcs
                    if prop_val and (result := func(prop_val))
                ),
                (
                    prop_val
                    for (prop_val, func) in funcs
                    if prop_val
                ),
            ), 1
            ), None,
        )

    def load_online_asset(self, asset_id: int) -> bytes | None:
        data = grabber.load_rōblox_asset(asset_id)
        if data is None:
            return None

        data = rbxl.parse(data)
        data = mesh.parse(data)
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
        local_data = self.load_local_asset(path)
        if local_data:
            return local_data

        id_num = None
        if asset_id.startswith(material.const.ID_PREFIX):
            id_num = material.transform_to_id_num(asset_id)

        if id_num:
            return self.load_asset_num(id_num)
