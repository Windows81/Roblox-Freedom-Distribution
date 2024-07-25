from .._logic import base_type as config_base_type
from typing_extensions import Self
import util.const as const
import fnmatch
import os


class path_str(str):
    def __new__(cls, config: config_base_type, val: str) -> Self:
        root = os.path.dirname(config.config_path)
        return str.__new__(cls, os.path.join(root, val))


class uri_obj:
    '''
    Supports either a file path or an `http` URL.
    Unlike the `path_str` class, is **not** a subclass of `str`.
    '''
    is_online: bool
    value: str

    def __init__(self, config: config_base_type, input: str) -> None:
        if input.startswith('http://') or input.startswith('https://'):
            self.is_online = True
            self.value = input
            return

        self.is_online = False
        self.value = path_str(config, input)


class rfd_version_check(str):
    def __new__(cls, val: str) -> Self:
        if not fnmatch.fnmatch(const.GIT_RELEASE_VERSION, val):
            raise Exception(
                "The RFD version you're using doesn't match " +
                "what was specified in the file."
            )
        return str.__new__(cls, val)
