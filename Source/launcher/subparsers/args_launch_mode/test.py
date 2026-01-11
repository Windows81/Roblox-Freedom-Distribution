# Standard library imports
import argparse

# Local application imports
import tester

from routines import test
from routines import _logic as logic

import launcher.subparsers._logic as sub_logic


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


@sub_logic.serialise_args(sub_logic.launch_mode.TEST)
def _(
    parser: argparse.ArgumentParser,
    args_ns: argparse.Namespace,
) -> list[logic.base_entry]:
    return [
        test.obj_type(
            tests=set(args_ns.tests_to_run),
        )
    ]
