import data_transfer.transferer
from config_type import _logic
from assets import asseter
from . import structure
import util.resource
import util.versions
import functools
import os.path
import tomllib
import storage


class obj_type(structure.config_type, _logic.base_type):
    def __init__(self, data_dict: dict, base_dir: str) -> None:
        '''
        High-level call: reads the game configuration data from a file and serialises it.
        '''
        _logic.base_type.__init__(self, data_dict, base_dir)

        structure.config_type.__init__(
            self,
            root=self,
            current_typ=structure.config_type,
            **self.data_dict,
        )

        self.storage = storage.storager(
            self.game_setup.persistence.sqlite_path,
            force_init=self.game_setup.persistence.clear_on_start,
        )

        self.data_transferer = data_transfer.transferer.obj_type()

        self.asset_cache = asseter(
            dir_path=self.game_setup.asset_cache.dir_path,
            redirect_func=self.remote_data.asset_redirects,
            clear_on_start=self.game_setup.asset_cache.clear_on_start,
        )


@functools.cache
def get_cached_config(path: str = util.resource.DEFAULT_CONFIG_PATH) -> obj_type:
    file_path = util.resource.retr_config_full_path(path)
    with open(file_path, 'rb') as f:
        return obj_type(tomllib.load(f), base_dir=os.path.dirname(file_path))


@functools.cache
def generate_config(rbxl_file: str) -> obj_type:
    # The dictionary structure should adjust with changes to the `structure.py` file.
    skeleton = {
        'server_core': {'place_file': {'rbxl_uri': rbxl_file}},
        # This is a placeholder value.
        'game_setup': {'roblox_version': '2021'},
    }
    base_dir = util.resource.retr_full_path(util.resource.dir_type.MISC)
    config = obj_type(skeleton, base_dir)
    return config
