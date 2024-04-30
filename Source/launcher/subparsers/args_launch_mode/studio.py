import launcher.subparsers._logic as sub_logic
import launcher.routines.studio as studio
import launcher.routines._logic as logic
import argparse


@sub_logic.add_args(sub_logic.launch_mode.STUDIO)
def subparse(
    parser: argparse.ArgumentParser,
    subparser: argparse.ArgumentParser,
) -> None:

    subparser.add_argument(
        dest='args', nargs='*',
    )


@sub_logic.serialise_args(sub_logic.launch_mode.STUDIO)
def _(
    parser: argparse.ArgumentParser,
    args: argparse.Namespace,
) -> list[logic.arg_type]:

    return [
        studio.arg_type(
            cmd_args=args.args,
        )
    ]
