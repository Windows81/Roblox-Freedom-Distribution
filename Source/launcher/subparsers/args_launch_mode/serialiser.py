from launcher.routines import serialiser

import launcher.subparsers._logic as sub_logic
from launcher.routines import _logic as logic
import assets.serialisers
import argparse


@sub_logic.add_args(sub_logic.launch_mode.SERIALISE_FILE)
def _(
    parser: argparse.ArgumentParser,
    subparser: argparse.ArgumentParser,
) -> None:

    subparser.add_argument(
        '--load',
        '--read',
        '-r',
        type=str,
        nargs='+',
        help='Path to the file(s) to be loaded.',
    )
    subparser.add_argument(
        '--save',
        '--write',
        '-w',
        type=str,
        nargs='+',
        help='Path to the file(s) to be saved.',
    )
    subparser.add_argument(
        '--method',
        type=assets.serialisers.method.__getitem__,
        choices=assets.serialisers.ALL_METHODS,
        help='Serialisers to use on the file(s) provided.',
        nargs='+',
    )


@sub_logic.serialise_args(sub_logic.launch_mode.SERIALISE_FILE, {serialiser.arg_type})
def _(
    parser: argparse.ArgumentParser,
    args_ns: argparse.Namespace,
) -> list[logic.arg_type]:
    return [
        serialiser.arg_type(
            files=list(zip(args_ns.load, args_ns.save)),
            methods=set(args_ns.method),
        ),
    ]
