# Standard library imports
import argparse
import logger

# Local application imports
from routines import cookie
from routines import _logic as logic

import launcher.subparsers._logic as sub_logic


@sub_logic.add_args(sub_logic.launch_mode.SHOW_COOKIE)
def _(
    parser: argparse.ArgumentParser,
    subparser: argparse.ArgumentParser,
) -> None:
    subparser.add_argument(
        '--verbose',
        '--show',
        '-v',
        action='store_true',
        help='Exposes the entire cookie in plaintext.',
    )


@sub_logic.serialise_args(sub_logic.launch_mode.SHOW_COOKIE, {cookie.arg_type})
def _(
    parser: argparse.ArgumentParser,
    args_ns: argparse.Namespace,
) -> list[logic.arg_type]:
    return [
        cookie.arg_type(args_ns.verbose)
    ]
