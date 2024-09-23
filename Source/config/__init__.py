import data_transfer.transferer
from . import structure
import util.resource
import util.versions
import tomli


class obj_type(structure.config_type):
    def __init__(
        self,
        data_transferer: data_transfer.transferer.obj_type,
        file_path: str = util.resource.DEFAULT_CONFIG_PATH,
    ) -> None:
        '''
        High-level call: reads the game configuration data from a file and serialises it.
        '''
        self.data_transferer = data_transferer
        self.file_path = util.resource.retr_config_full_path(file_path)
        with open(self.file_path, 'rb') as f:
            self.data_dict: dict = tomli.load(f)

        structure.config_type.__init__(
            self,
            root=self,
            current_typ=structure.config_type,
            **self.data_dict,
        )
