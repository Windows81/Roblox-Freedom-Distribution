# Standard library imports
import argparse

# Local application imports
from routines import _logic as logic

import launcher.subparsers._logic as sub_logic

AUX_MODES = (
    sub_logic.launch_mode.PLAYER,
    sub_logic.launch_mode.SERVER,
    sub_logic.launch_mode.STUDIO,
)


@sub_logic.add_aux_args(*AUX_MODES)
def _(
    mode: sub_logic.launch_mode,
    parser: argparse.ArgumentParser,
    sub_parser: argparse.ArgumentParser,
) -> None:
    sub_parser.add_argument(
        '--clear_cache',
        action='store_true',
        help=r'Deletes cached content specific to the host you are connecting to.  Searches in the %%LocalAppData%%\Temp\Roblox\http directory.',
    )


@sub_logic.serialise_aux_args(*AUX_MODES)
def _(
    mode: sub_logic.launch_mode,
    args_ns: argparse.Namespace,
    args_list: list[logic.base_entry],
) -> list[logic.base_entry]:

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
