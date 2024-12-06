from launcher.routines import test

from launcher.routines import _logic as logic
import launcher.subparsers._logic as sub_logic
import tester

import argparse


@sub_logic.add_args(sub_logic.launch_mode.TEST)
def _(
    parser: argparse.ArgumentParser,
    subparser: argparse.ArgumentParser,
) -> None:
    subparser.add_argument(
        'tests_to_run',
        type=str,
        help='Unit tests which are run by RFD.',
        default=tester.DEFAULT_TEST_NAMES,
        nargs='*',
    )


@sub_logic.serialise_args(sub_logic.launch_mode.TEST, {test.arg_type})
def _(
    parser: argparse.ArgumentParser,
    args: argparse.Namespace,
) -> list[logic.arg_type]:
    return [
        test.arg_type(
            tests=set(args.tests_to_run),
        )
    ]
