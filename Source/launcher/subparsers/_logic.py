from typing import Callable
import enum


class launch_mode(enum.Enum):
    ALWAYS = 'always'
    SERVER = 'server'
    PLAYER = 'player'
    DOWNLOAD = 'download'
    TEST = 'test'


ENABLED_LAUNCH_MODES = {
    launch_mode.SERVER,
    launch_mode.PLAYER,
    launch_mode.DOWNLOAD,
    launch_mode.TEST,
}


MODE_ALIASES = {
    n: m
    for m in ENABLED_LAUNCH_MODES
    for n in [
        m.value,
    ]
}


ADD_MODE_ARGS: dict[launch_mode, list[Callable]] = {
    m: [] for m in launch_mode
}
SERIALISE_ARGS: dict[launch_mode, list[Callable]] = {
    m: [] for m in launch_mode
}
SERIALISE_TYPE_SETS: dict[launch_mode, set[type]] = {
    m: set() for m in launch_mode
}


def call_auxs(args_table: dict[launch_mode, list[Callable]], l_mode: launch_mode, *args, **kwargs) -> list:
    return [
        result
        for func in args_table[launch_mode.ALWAYS]
        for result in (func(l_mode, *args, **kwargs) or [])
    ]


def call_subparser(args_table: dict[launch_mode, list[Callable]], l_mode: launch_mode, *args, **kwargs) -> list:
    return [
        result
        for func in args_table[l_mode]
        for result in (func(*args, **kwargs) or [])
    ]


def add_args(launch_mode: launch_mode):
    def inner(func):
        ADD_MODE_ARGS[launch_mode].append(func)
        return func
    return inner


def serialise_args(launch_mode: launch_mode, types: set[type]):
    resolved_types = {t for typ in types for t in typ.mro()}

    def inner(func):
        SERIALISE_TYPE_SETS[launch_mode].update(resolved_types)
        SERIALISE_ARGS[launch_mode].append(func)
        return func
    return inner
