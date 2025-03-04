import launcher.routines.clear_cache as clear_cache
import launcher.subparsers._logic as sub_logic
from ...routines import _logic as logic
import functools
import argparse

CACHEABLE_ARG_SUPERTYPE = logic.bin_arg_type


@functools.cache
def check_mode(mode: sub_logic.launch_mode) -> bool:
    return CACHEABLE_ARG_SUPERTYPE in sub_logic.SERIALISE_TYPE_SETS[mode]


@sub_logic.add_args(sub_logic.launch_mode.ALWAYS)
def _(
    mode: sub_logic.launch_mode,
    parser: argparse.ArgumentParser,
    sub_parser: argparse.ArgumentParser,
) -> None:
    if not check_mode(mode):
        return

    sub_parser.add_argument(
        '--keep_cache',
        action='store_true',
        help=r'Skips deleting cached content specific to the host you're connecting to.  Searches in the % %LocalAppData % %\Temp\Roblox\http directory.',
    )


@sub_logic.serialise_args(sub_logic.launch_mode.ALWAYS, {clear_cache.arg_type})
def _(
    mode: sub_logic.launch_mode,
    args_ns: argparse.Namespace,
    args_list: list[logic.arg_type],
) -> list[logic.arg_type]:
    if not check_mode(mode):
        return []

    base_args = [
        a.reconstruct()
        for a in args_list
        if isinstance(a, logic.bin_arg_type)
    ]

    if base_args is None:
        return []

    args_list[:0] = [
        clear_cache.arg_type(
            base_url=base.get_app_base_url(),
        )
        for base in base_args
    ]

    return []
