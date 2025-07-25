# Standard library imports
import enum
import fnmatch
import os
import urllib.request

# Typing imports
from typing import Self, get_args


# Local application imports
import util.const as const
import assets.extractor as extractor


class dicter[key_typ, item_typ](dict[key_typ, item_typ]):
    '''
    Inputs a list of `item_typ` values.
    Acts a subclass of `dict[key_typ, item_typ]`,
    where each key is equal to `getattr(item, 'key_name')`
    '''
    key_name: str
    item_type: type
    key_type: type

    # https://stackoverflow.com/a/71720366
    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        # `base_type` should be something like `dicter[int, config.types.structs.gamepass]`.
        # We're extracting the generic types which dicter's `__init__` will cast the input values into.
        base_type: type = next(
            c
            for c in getattr(cls, '__orig_bases__', [])
            if getattr(c, '__origin__', None) == dicter
        )
        (cls.key_type, cls.item_type) = get_args(base_type)

    def __init__(self, item_list: list[item_typ]) -> None:
        super().__init__()
        for item in item_list:
            self[getattr(item, self.key_name)] = item


class path_str(str):
    def __new__(cls, value: str, dir_root: str) -> Self:
        return str.__new__(cls, os.path.join(dir_root, value))


class uri_type(enum.Enum):
    LOCAL = 0
    ONLINE = 1
    RŌBLOX = 2


class uri_obj:
    '''
    Supports either a file path or an `http` URL.
    Unlike the `path_str` class, is **not** a subclass of `str`.
    '''

    def __init__(self, value: str | bytes, dir_root: str) -> None:
        super().__init__()
        if isinstance(value, bytes):
            value = value.decode(encoding='utf-8')
        assert isinstance(value, str)

        rbx_asset_prefix = 'rbxassetid://'
        if value.startswith(rbx_asset_prefix):
            self.uri_type = uri_type.RŌBLOX
            self.value = value[len(rbx_asset_prefix):]
            return

        elif value.startswith('http://') or value.startswith('https://'):
            self.uri_type = uri_type.ONLINE
            self.value = value
            return

        self.uri_type = uri_type.LOCAL
        self.value = path_str(value, dir_root)

    def extract(self) -> bytes | None:
        if self.uri_type == uri_type.LOCAL:
            with open(self.value, 'rb') as rf:
                return rf.read()

        elif self.uri_type == uri_type.ONLINE:
            with urllib.request.urlopen(self.value) as response:
                if response.status != 200:
                    raise Exception("File couldn't be loaded.")
                return response.read()

        elif self.uri_type == uri_type.RŌBLOX:
            return extractor.download_item(self.value)


class rfd_version_check(str):
    def __new__(cls, val: str) -> Self:
        if not fnmatch.fnmatch(const.GIT_RELEASE_VERSION, val):
            raise Exception(
                "The RFD version you're using doesn't match what was specified in the file (i.e. %s)." %
                (val,)
            )
        return str.__new__(cls, val)


class counter:
    def __init__(self) -> None:
        super().__init__()
        self.count = 0

    def __call__(self, *a) -> int:
        self.count += 1
        return self.count
