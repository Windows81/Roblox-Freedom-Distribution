import launcher.subparsers._logic as sub_logic
import launcher.routines.download as download
import launcher.routines.rcc_server as rcc_server
import launcher.routines.player as player
import launcher.routines._logic as logic
import util.versions
import argparse


@sub_logic.add_args(sub_logic.launch_mode.DOWNLOAD)
def _(
    parser: argparse.ArgumentParser,
    subparser: argparse.ArgumentParser,
) -> None:
    subparser.add_argument(
        '--version', '-v',
        type=util.versions.rōblox.from_name,
        help='Version to download.',
    )
    subparser.add_argument(
        '--dir_name', '-d',
        type=str, choices=[
            player.obj_type.DIR_NAME,
            rcc_server.obj_type.DIR_NAME,
        ],
        help='Directories to download.',
        nargs='+',
    )


@sub_logic.serialise_args(sub_logic.launch_mode.DOWNLOAD)
def _(
    parser: argparse.ArgumentParser,
    args: argparse.Namespace,
) -> list[logic.arg_type]:

    return [
        download.arg_type(
            rōblox_version=args.version,
            dir_name=d
        )
        for d in args.dir_name
    ]
