# Standard library imports
import argparse

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


@sub_logic.serialise_args(sub_logic.launch_mode.SHOW_COOKIE, {cookie.obj_type})
def _(
    parser: argparse.ArgumentParser,
    args_ns: argparse.Namespace,
) -> list[logic.obj_type]:
    return [
        cookie.obj_type(verbose=args_ns.verbose)
    ]
