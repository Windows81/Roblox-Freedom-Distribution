import launcher.subparsers._logic as sub_logic
import launcher.routines.download as download
import launcher.routines.rcc_server as rcc_server
import launcher.routines.player as player
from ...routines import _logic as logic
import util.resource
import util.versions
import argparse


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
            rcc_server.obj_type.BIN_SUBTYPE.value,
        ],
        help='Directories to download.',
        nargs='+',
    )


@sub_logic.serialise_args(sub_logic.launch_mode.DOWNLOAD, {download.arg_type})
def _(
    parser: argparse.ArgumentParser,
    args: argparse.Namespace,
) -> list[logic.arg_type]:

    return [
        download.arg_type(
            rōblox_version=args.rbx_version,
            bin_subtype=b,
        )
        for b in args.bin_subtype
    ]
