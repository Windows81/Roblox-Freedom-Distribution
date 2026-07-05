# pyright: reportImportCycles=false

# Standard library imports
import functools
import json
import os.path
import sys
import tomllib

# Typing imports
from typing import Any, Callable

# Third-party or external imports
import storage

# Local application imports
import data_transfer.transferer
from config_type import _logic
from assets import asseter
from . import structure
import util.resource
import util.versions


PARSERS: dict[str, Callable[[bytes], dict[Any, Any]]] = {
    'toml': lambda f: tomllib.loads(f.decode('utf-8')),
    'json': lambda f: json.loads(f),
}


class obj_type(structure.config_type, _logic.base_type):
    def __init__(
        self,
        data_dict: dict[Any, Any],
        base_dir: str,
        cache_directory: str | None = None,
    ) -> None:
        '''
        High-level call: reads the game configuration data from a file and serialises it.
        '''
        effective_data_dict = dict(data_dict)
        if cache_directory is not None:
            game_setup = effective_data_dict.get('game_setup')
            if isinstance(game_setup, dict):
                effective_data_dict['game_setup'] = dict(game_setup)
                effective_data_dict['game_setup']['cache_directory'] = cache_directory
            else:
                effective_data_dict['game_setup'] = {'cache_directory': cache_directory}

        _logic.base_type.__init__(self, effective_data_dict, base_dir)

        structure.config_type.__init__(
            self,
            root=self,
            # `current_typ` must be defined separately since this `__init__` call is a super constructor.
            current_typ=structure.config_type,
            **effective_data_dict,
        )

        self.storage = storage.storager(
            self.game_setup.persistence.sqlite_path,
            force_init=self.game_setup.persistence.clear_on_start,
        )

        self.data_transferer = data_transfer.transferer.obj_type()

        cache_dir = self.game_setup.cache_directory
        if cache_dir is None:
            cache_dir = self.game_setup.asset_cache.dir_path
        self.game_setup.asset_cache.dir_path = cache_dir

        self.asset_cache = asseter(
            dir_path=cache_dir,
            redirect_func=self.remote_data.asset_redirects,
            asset_name_func=self.game_setup.asset_cache.name_template,
            clear_on_start=self.game_setup.asset_cache.clear_on_start,
        )

    def retr_version(self) -> util.versions.rōblox:
        return self.game_setup.roblox_version


STDIN_NAME = '-'


def get_config_dir_path(path: str = STDIN_NAME) -> str:
    if path == STDIN_NAME:
        return util.resource.retr_full_path(util.resource.dir_type.WORKING_DIR)
    return os.path.dirname(util.resource.retr_config_full_path(path))


@functools.cache
def read_file_data(path: str) -> bytes:
    # Reads from stdin if `-` is passed in.
    # This takes precedent from FFmpeg.
    if path == STDIN_NAME:
        return sys.stdin.buffer.read()
    file_path = util.resource.retr_config_full_path(path)
    with open(file_path, 'rb') as f:
        return f.read()


@functools.cache
def get_cached_config(
    path: str = util.resource.DEFAULT_CONFIG_PATH,
    cache_directory: str | None = None,
) -> obj_type:
    base_dir = get_config_dir_path(path)
    file_data = read_file_data(path)
    for parse in PARSERS.values():
        try:
            data_dict = parse(file_data)
        except Exception:
            continue
        return obj_type(
            data_dict=data_dict,
            base_dir=base_dir,
            cache_directory=cache_directory,
        )
    raise Exception(f'The file at {path} is in an invalid format')


@functools.cache
def generate_config(
    rbxl_file: str,
    version: util.versions.rōblox = util.versions.rōblox.v463,
    cache_directory: str | None = None,
) -> obj_type:
    # The dictionary structure should adjust with changes to the `structure.py` file.
    skeleton = {
        'server_core': {'place_file': {'rbxl_uri': rbxl_file}},
        'game_setup': {'roblox_version': version.name},
    }
    obj_type.server_core.place_file
    base_dir = util.resource.retr_full_path(util.resource.dir_type.MISC)
    config = obj_type(skeleton, base_dir, cache_directory=cache_directory)
    return config
    