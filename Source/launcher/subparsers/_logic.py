from typing import Any, Callable
import enum


class launch_mode(enum.Enum):
    SERVER = 'server'
    STUDIO = 'studio'
    PLAYER = 'player'
    SERIALISE_FILE = 'serialise'
    DOWNLOAD = 'download'
    TEST = 'test'
    SHOW_COOKIE = 'cookie'


ENABLED_LAUNCH_MODES = set(launch_mode)


MODE_ALIASES = {
    n: m
    for m in ENABLED_LAUNCH_MODES
    for n in [
        m.value,
    ]
}


def prepare_decorator_accumulator():
    result_table: dict[launch_mode, list[Callable[..., Any]]] = {
        m: [] for m in launch_mode
    }

    def outer(*launch_modes: launch_mode):
        def inner(func):
            for m in launch_modes:
                result_table[m].append(func)
            return func
        return inner

    return (outer, result_table)


(add_args, ADD_ARGS_FUNCS) = prepare_decorator_accumulator()
(add_aux_args, ADD_AUX_ARGS_FUNCS) = prepare_decorator_accumulator()
(serialise_args, SERIALISE_ARGS_FUNCS) = prepare_decorator_accumulator()
(serialise_aux_args, SERIALISE_AUX_ARGS_FUNCS) = prepare_decorator_accumulator()


def call_auxs(args_table: dict[launch_mode, list[Callable[..., Any]]], l_mode: launch_mode, *args, **kwargs) -> list[Any]:
    return [
        result
        for func in args_table[l_mode]
        for result in (func(l_mode, *args, **kwargs) or [])
    ]


def call_subparser(args_table: dict[launch_mode, list[Callable[..., Any]]], l_mode: launch_mode, *args, **kwargs) -> list[Any]:
    return [
        result
        for func in args_table[l_mode]
        for result in (func(*args, **kwargs) or [])
    ]
