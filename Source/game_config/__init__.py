from config_type import _logic
import data_transfer.transferer
from assets import asseter
from . import structure
import util.resource
import util.versions
import functools
import storage


class obj_type(structure.config_type, _logic.base_type):
    def __init__(self, path: str = util.resource.DEFAULT_CONFIG_PATH) -> None:
        '''
        High-level call: reads the game configuration data from a file and serialises it.
        '''
        _logic.base_type.__init__(
            self,
            path=path,
        )

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
    obj = obj_type(path)
    return obj
