import launcher.subparsers._logic as sub_logic
import launcher.routines.studio as studio
import argparse


@sub_logic.launch_command(sub_logic.launch_mode.STUDIO)
def _(parser: argparse.ArgumentParser, sub_parser: argparse.ArgumentParser):
    sub_parser.add_argument(
        dest='args', nargs='*',
    )
    args = parser.parse_args()
    return [
        studio.arg_type(
            cmd_args=args.args,
        )
    ]
