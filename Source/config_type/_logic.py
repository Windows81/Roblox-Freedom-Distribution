import util.resource
import util.versions
import tomllib


class base_type:
    def __init__(self, path: str) -> None:
        self.file_path = util.resource.retr_config_full_path(path)
        with open(self.file_path, 'rb') as f:
            self.data_dict: dict = tomllib.load(f)
