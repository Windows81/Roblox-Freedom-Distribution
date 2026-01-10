# Standard library imports
import argparse
import functools

# Local application imports
import routines.clear_cache as clear_cache
from routines import _logic as logic

import launcher.subparsers._logic as sub_logic


CACHEABLE_ARG_SUPERTYPE = logic.bin_entry


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
        '--clear_cache',
        action='store_true',
        help=r'Deletes cached content specific to the host you are connecting to.  Searches in the %%LocalAppData%%\Temp\Roblox\http directory.',
    )


@sub_logic.serialise_args(sub_logic.launch_mode.ALWAYS, {clear_cache.obj_type})
def _(
    mode: sub_logic.launch_mode,
    args_ns: argparse.Namespace,
    args_list: list[logic.obj_type],
) -> list[logic.obj_type]:

    if not check_mode(mode):
        return []

    if not args_ns.clear_cache:
        return []

    base_args = [
        arg
        for arg in args_list
        if isinstance(arg, logic.bin_entry)
    ]

    if len(base_args) == 0:
        return []

    args_list[:0] = [
        clear_cache.obj_type(
            base_url=base.get_app_base_url(),
        )
        for base in base_args
    ]

    return []
