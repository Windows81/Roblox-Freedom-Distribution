import util.versions
import enum
import sys
import os

MADE_WITH_PYINSTALLER = hasattr(sys, '_MEIPASS')
# TODO: don't make things depend on parent directories.
TOP_DIR = \
    os.path.dirname(sys.executable) \
    if MADE_WITH_PYINSTALLER else \
    os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


class dir_type(enum.Enum):
    RŌBLOX = 0
    CONFIG = 1
    ASSET = 2
    SSL = 3


DEFAULT_CONFIG_PATH = './GameConfig.toml'


def get_paths(d: dir_type) -> str:
    match (MADE_WITH_PYINSTALLER, d):

        case (True, dir_type.RŌBLOX):
            return [TOP_DIR, 'Roblox']
        case (False, dir_type.RŌBLOX):
            return [TOP_DIR, 'Roblox']

        case (True, dir_type.CONFIG):
            return [TOP_DIR]
        case (False, dir_type.CONFIG):
            return [TOP_DIR]

        case (True, dir_type.ASSET):
            return [TOP_DIR, 'AssetCaché']
        case (False, dir_type.ASSET):
            return [TOP_DIR, 'AssetCaché']

        # We're storing TLS certiifcates in temporary directory "_MEIPASS".
        case (True, dir_type.SSL):
            return [sys._MEIPASS]
        case (False, dir_type.SSL):
            return [TOP_DIR, 'Source', 'ssl']


def get_full_path(d: dir_type, *paths: str) -> str:
    return os.path.join(*get_paths(d), *paths)


def get_rōblox_full_path(version: util.versions.rōblox, *paths: str) -> str:
    return get_full_path(dir_type.RŌBLOX, version.name, *paths)


def get_config_full_path(path: str = DEFAULT_CONFIG_PATH) -> str:
    if not os.path.isabs(path):
        path = os.path.join(
            get_full_path(dir_type.CONFIG),
            path,
        )
    return os.path.normpath(path)
