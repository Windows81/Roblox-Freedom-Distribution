import enum
import sys
import os

MADE_WITH_PYINSTALLER = hasattr(sys, '_MEIPASS')
# TODO: don't make things depend on parent directories.
TOP_DIR = \
    sys._MEIPASS \
    if MADE_WITH_PYINSTALLER else \
    os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


class dir_type(enum.Enum):
    RŌBLOX = 0
    ASSET = 1
    SSL = 2


def get_paths(d: dir_type) -> str:
    match (MADE_WITH_PYINSTALLER, d):

        case (True, dir_type.RŌBLOX):
            return ['Roblox']

        case (False, dir_type.RŌBLOX):
            return ['Roblox']

        case (True, dir_type.ASSET):
            return ['AssetCaché']

        case (False, dir_type.ASSET):
            return ['AssetCaché']

        case (True, dir_type.SSL):
            return []

        case (False, dir_type.SSL):
            return ['Source', 'ssl']


def get_full_path(d: dir_type, *paths: str) -> str:
    return os.path.join(TOP_DIR, * get_paths(d), *paths)
