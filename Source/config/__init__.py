
from . import structure, base_types
import util.resource
import util.versions
import functools
import tomli


class obj_type(structure.config_type, base_types._base_type):
    def __init__(self, path: str = util.resource.DEFAULT_CONFIG_PATH) -> None:
        '''
        Retrieves the game configuration data and serialises it.
        '''
        with open(util.resource.retr_config_full_path(path), 'rb') as f:
            self.data_dict: dict = tomli.load(f)

        super().__init__(
            root=self,
            current_typ=structure.config_type,
            **self.data_dict,
        )


@functools.cache
def get_cached_config(path: str = util.resource.DEFAULT_CONFIG_PATH) -> obj_type:
    obj = obj_type(path)
    return obj
