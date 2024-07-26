from .._logic import base_type as config_base_type
from typing_extensions import Self
import util.const as const
import fnmatch
import os


def dicter(key_typ: type, key: str):
    '''
    Converts a list of entries into a dictionary which can be indexed by `key`.
    '''
    def submethod(item_typ: type):
        class subclass(dict[key_typ, item_typ]):
            decorator = dicter
            key_type = key_typ
            item_type = item_typ

            def __init__(self, item_list: list[key_typ]):
                for item in item_list:
                    self[getattr(item, key)] = item
        return subclass
    return submethod


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
