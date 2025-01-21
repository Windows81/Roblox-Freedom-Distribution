from typing import Self, TypeVar, get_args
import util.const as const
import extractor
import fnmatch
import urllib3
import enum
import os


item_typ = TypeVar('item_typ')
key_typ = TypeVar('key_typ')


class dicter[item_typ, key_typ](dict[key_typ, item_typ]):
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
        # `typed_base` should be something like `dicter[config.types.structs.gamepass, int]`.
        # We're extracting the generic types which `__init__` will cast the
        # input values into.
        typed_base = next(
            c
            for c in getattr(cls, '__orig_bases__', [])
            if getattr(c, '__origin__', None) == dicter
        )
        (cls.item_type, cls.key_type) = get_args(typed_base)

    def __init__(self, item_list: list[item_typ]):
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

        if value.startswith('http://') or value.startswith('https://'):
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
            http = urllib3.PoolManager()
            response = http.request('GET', self.value)

            if response.status != 200:
                raise Exception("File couldn't be loaded.")

            return response.data

        elif self.uri_type == uri_type.RŌBLOX:
            return extractor.download_item(self.value)


class rfd_version_check(str):
    def __new__(cls, val: str) -> Self:
        if not fnmatch.fnmatch(const.GIT_RELEASE_VERSION, val):
            raise Exception(
                "The RFD version you're using doesn't match " +
                "what was specified in the file."
            )
        return str.__new__(cls, val)
