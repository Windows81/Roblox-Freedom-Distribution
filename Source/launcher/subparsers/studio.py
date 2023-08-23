import launcher.routines.studio as studio
import launcher.subparsers.logic as logic
import argparse


@logic.launch_command(logic.launch_mode.STUDIO)
def _(parser: argparse.ArgumentParser, sub_parser: argparse.ArgumentParser):
    sub_parser.add_argument(
        dest='args', nargs='*',
    )
    args = parser.parse_args()
    return [
        studio.argtype(
            cmd_args=args.args,
        )
    ]
