import launcher.routines.rcc_server as rcc_server
import launcher.subparsers._logic as sub_logic
import launcher.routines.download as download
import launcher.routines.player as player
import util.versions
import argparse


def subparse(
    parser: argparse.ArgumentParser,
    sub_parser: argparse.ArgumentParser,
    use_ssl: bool = False,
) -> list[download.arg_type]:
    sub_parser.add_argument(
        '--version', '-v',
        type=util.versions.rōblox.from_name,
        help='Version to download.',
    )
    sub_parser.add_argument(
        '--dir_name', '-d',
        type=str, choices=[
            player.obj_type.DIR_NAME,
            rcc_server.obj_type.DIR_NAME,
        ],
        help='Directories to download.',
        nargs='+',
    )
    args = parser.parse_args()

    return [
        download.arg_type(
            rōblox_version=args.version,
            dir_name=d
        )
        for d in args.dir_name
    ]


@sub_logic.add_args(sub_logic.launch_mode.PLAYER)
def _(*a):
    return subparse(
        *a,
        use_ssl=True,
    )
