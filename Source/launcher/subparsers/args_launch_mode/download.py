# Standard library imports
import argparse

# Local application imports
import logger
import util.resource
import util.versions

from routines import player, rcc, studio
from routines import _logic as logic
from pretasks import download

import launcher.subparsers._logic as sub_logic


@sub_logic.add_args(sub_logic.launch_mode.DOWNLOAD)
def _(
    parser: argparse.ArgumentParser,
    subparser: argparse.ArgumentParser,
) -> None:
    subparser.add_argument(
        '--rbx_version', '-v',
        type=util.versions.rōblox.from_name,
        help='Version to download.',
    )
    subparser.add_argument(
        '--bin_subtype', '-b',
        type=util.resource.bin_subtype,
        choices=[
            player.obj_type.BIN_SUBTYPE.value,
            rcc.obj_type.BIN_SUBTYPE.value,
            studio.obj_type.BIN_SUBTYPE.value,
        ],
        help='Directories to download.',
        nargs='+',
    )


@sub_logic.serialise_args(sub_logic.launch_mode.DOWNLOAD)
def _(
    parser: argparse.ArgumentParser,
    args_ns: argparse.Namespace,
) -> list[logic.base_entry]:

    log_filter = logger.filter.FILTER_REASONABLE
    for b in args_ns.bin_subtype:
        download.bootstrap_binary(
            rōblox_version=args_ns.rbx_version,
            log_filter=log_filter,
            bin_type=b,
        )
    return []
