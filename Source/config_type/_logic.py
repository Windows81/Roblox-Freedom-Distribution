import util.resource
import util.versions
import tomllib


class base_type:
    def __init__(self, data_dict: dict, base_dir: str) -> None:
        self.base_dir = base_dir
        self.data_dict: dict = data_dict
