import util.resource
import util.versions
import functools
import tomllib

TYPE_CALLS = {
    util.versions.rōblox: util.versions.rōblox.from_name,
}


class allocateable:
    def __init__(self, **kwargs) -> None:
        for k, cls in self.__class__.__annotations__.items():
            setattr(self, k, TYPE_CALLS.get(cls, cls)(kwargs[k]))
        for k, cls in self.__class__.__dict__.items():
            if isinstance(cls, type) and issubclass(cls, allocateable):
                setattr(self, k, TYPE_CALLS.get(cls, cls)(**kwargs[k]))


class _configtype(allocateable):
    def __init__(self, path: str = util.resource.DEFAULT_CONFIG_PATH) -> None:
        with open(util.resource.get_config_full_path(path), 'rb') as f:
            self.data_dict: dict = tomllib.load(f)
        super().__init__(**self.data_dict)


class configtype(_configtype):
    '''
    Configuration specification, according by default to "GameConfig.toml".
    '''
    class server_assignment(allocateable):
        class players(allocateable):
            maximum: int
            preferred: int

        class instances(allocateable):
            count: int

    class place_setup(allocateable):
        path: str
        roblox_version: util.versions.rōblox


@functools.cache
def get_config(path: str = util.resource.DEFAULT_CONFIG_PATH) -> configtype:
    return configtype(path)
