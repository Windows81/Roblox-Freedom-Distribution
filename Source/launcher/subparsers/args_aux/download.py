import argparse
import sys
import os

import launcher.subparsers._logic as sub_logic
from routines import _logic as logic
import util.const

AUX_MODES = (
    sub_logic.launch_mode.PLAYER,
    sub_logic.launch_mode.SERVER,
    sub_logic.launch_mode.STUDIO,
)


@sub_logic.add_aux_args(*AUX_MODES)
def _(
    mode: sub_logic.launch_mode,
    parser: argparse.ArgumentParser,
    subparser: argparse.ArgumentParser,
) -> None:
    subparser.add_argument(
        '--skip_download',
        action='store_true',
        help='disable auto-download of RFD binaries from the internet',
    )
    subparser.add_argument(
        '--force_update_bins',
        action='store_true',
        help='forcibly overwrite the RFD binary\'s directory if one already exists',
    )


@sub_logic.serialise_aux_args(*AUX_MODES)
def _(
    mode: sub_logic.launch_mode,
    args_ns: argparse.Namespace,
    args_list: list[logic.base_entry],
) -> list[logic.base_entry]:

    # Enables auto_download flags for every routine, but adds *no* new routines of its own.
    for a in args_list:
        if not isinstance(a, logic.bin_entry):
            continue
        a.auto_download = not args_ns.skip_download
        a.overwrite_auto_download_dir = args_ns.force_update_bins
    return []
