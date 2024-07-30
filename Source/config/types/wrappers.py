from typing_extensions import Self, Type, TypeVar, get_args
from .._logic import base_type as config_base_type
import util.const as const
import fnmatch
import os

item_typ = TypeVar('item_typ')
key_typ = TypeVar('key_typ')


class dicter[item_typ, key_typ](dict[key_typ, item_typ]):
    '''
    Inputs a list of `item_typ` values.
    Acts a subclass of `dict[key_typ, item_typ]`,
    where each key is equal to `getattr(item, 'key_name')`'''
    key_name: str
    item_type: type
    key_type: type

    # https://stackoverflow.com/a/71720366
    def __init_subclass__(cls) -> None:
        # `typed_base` should be something like `dicter[config.types.structs.gamepass, int]`.
        # We're extracting the generic types which `__init__` will cast the input values into.
        typed_base = next(
            c
            for c in getattr(cls, '__orig_bases__', [])
            if getattr(c, '__origin__', None) == dicter
        )
        (cls.item_type, cls.key_type) = get_args(typed_base)

    def __init__(self, item_list: list[item_typ]):
        for item in item_list:
            self[getattr(item, self.key_name)] = item


class path_str(str):
    def __new__(cls, value: str, config: config_base_type) -> Self:
        root = os.path.dirname(config.config_path)
        return str.__new__(cls, os.path.join(root, value))


class uri_obj:
    '''
    Supports either a file path or an `http` URL.
    Unlike the `path_str` class, is **not** a subclass of `str`.
    '''
    is_online: bool
    value: str

    def __init__(self, input: str, config: config_base_type) -> None:
        if input.startswith('http://') or input.startswith('https://'):
            self.is_online = True
            self.value = input
            return

        self.is_online = False
        self.value = path_str(input, config)


class rfd_version_check(str):
    def __new__(cls, val: str) -> Self:
        if not fnmatch.fnmatch(const.GIT_RELEASE_VERSION, val):
            raise Exception(
                "The RFD version you're using doesn't match "
                "what was specified in the file."
            )
        return str.__new__(cls, val)
