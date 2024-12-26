import util.versions
import functools
import enum
import sys
import os

MADE_WITH_PYINSTALLER = hasattr(sys, '_MEIPASS')


@functools.cache
def get_top_dir() -> str:
    if MADE_WITH_PYINSTALLER:
        return os.path.dirname(sys.executable)

    base_file = None
    # Path for top-level `_main.py`.
    if hasattr(sys.modules['__main__'], '__file__'):
        base_file = sys.modules['__main__'].__file__

    # Otherwise, get the path for `~/util`.
    if base_file is None:
        base_file = os.path.dirname(__file__)

    # Traverse through parent directory twice.
    for _ in range(2):
        base_file = os.path.dirname(base_file)
    return base_file


class dir_type(enum.Enum):
    RŌBLOX = 0
    SSL = 1
    MISC = 2


class bin_subtype(enum.Enum):
    SERVER = 'Server'
    PLAYER = 'Player'
    STUDIO = 'Studio'


DEFAULT_CONFIG_PATH = './GameConfig.toml'


def get_path_pieces(d: dir_type) -> list[str]:
    match (MADE_WITH_PYINSTALLER, d):

        case (True, dir_type.RŌBLOX):
            return [get_top_dir(), 'Roblox']
        case (False, dir_type.RŌBLOX):
            return [get_top_dir(), 'Roblox']

        # If running from `exe`, stores TLS certiifcates in a temporary directory.
        case (True, dir_type.SSL):
            return [getattr(sys, '_MEIPASS', '')]
        case (False, dir_type.SSL):
            return [get_top_dir(), 'Source', 'ssl']

        case (True, dir_type.MISC):
            return [get_top_dir()]
        case (False, dir_type.MISC):
            return [get_top_dir()]
    return []


@functools.cache
def make_dirs(full_path: str) -> None:
    pieces = []
    head = os.path.abspath(full_path)
    tail = True
    while tail:
        (head, tail) = os.path.split(head)
        pieces.append(head)

    for head in reversed(pieces):
        if not os.path.isdir(head):
            os.mkdir(head)


def retr_full_path(d: dir_type, *paths: str) -> str:
    full_path = os.path.join(*get_path_pieces(d), *paths)
    make_dirs(full_path)
    return full_path


def retr_rōblox_full_path(version: util.versions.rōblox, bin_type: bin_subtype, *paths: str) -> str:
    return retr_full_path(dir_type.RŌBLOX, version.name, bin_type.value, *paths)


def retr_config_full_path(path: str = DEFAULT_CONFIG_PATH) -> str:
    if os.path.isdir(path):
        path = os.path.join(
            path,
            DEFAULT_CONFIG_PATH,
        )
    elif not os.path.isabs(path):
        path = os.path.join(
            retr_full_path(dir_type.MISC),
            path,
        )
    return os.path.normpath(path)
