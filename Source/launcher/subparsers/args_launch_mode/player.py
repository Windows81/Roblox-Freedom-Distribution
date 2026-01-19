# Standard library imports
import argparse
import itertools
import logger

# Local application imports
from routines import player
from routines import _logic as logic

import launcher.subparsers._logic as sub_logic


@sub_logic.add_args(sub_logic.launch_mode.PLAYER)
def _(
    parser: argparse.ArgumentParser,
    subparser: argparse.ArgumentParser,
) -> None:

    subparser.add_argument(
        '--rcc_host', '--host', '-rh',
        type=str,
        nargs='*',
        default=[],
        help='Hostname or IP address to connect this program to the RCC server.',
    )
    subparser.add_argument(
        '--rcc_port', '--port', '-rp',
        type=int,
        nargs='*',
        default=[],
        help='Port number to connect this program to the RCC server.',
    )
    subparser.add_argument(
        '--web_host', '--webserver_host', '-wh', '-h',
        type=str,
        nargs='*',
        default=[],
        help='Hostname or IP address to connect this program to the web server.',
    )
    subparser.add_argument(
        '--web_port', '--webserver_port', '-wp', '-p',
        type=int,
        nargs='*',
        default=[],
        help='Port number to connect this program to the web server.',
    )
    subparser.add_argument(
        '--user_code', '-u',
        type=str,
        nargs='*',
        default=[],
        help='Determines the user code for the player which joins the server.\nUser codes derive a user name, user iden number, and other characteristics of any particular player.',
    )
    subparser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Suppresses console output.',
    )
    subparser.add_argument(
        '--loud',
        action='store_true',
        help='Makes the client\'s output log file very verbose.',
    )


def gen_log_filter(
    parser: argparse.ArgumentParser,
    args_ns: argparse.Namespace,
) -> logger.obj_type:
    if args_ns.quiet:
        result = logger.PRINT_QUIET
    elif args_ns.loud:
        result = logger.PRINT_LOUD
    else:
        result = logger.PRINT_REASONABLE

    return result


@sub_logic.serialise_args(sub_logic.launch_mode.PLAYER)
def _(
    parser: argparse.ArgumentParser,
    args_ns: argparse.Namespace,
) -> list[logic.base_entry]:

    log_filter = gen_log_filter(
        parser, args_ns,
    )

    return [
        player.obj_type(
            rcc_host=rcc_host,
            rcc_port=rcc_port,
            web_host=web_host,
            web_port=web_port,
            user_code=user_code,
            logger=log_filter,
        )
        for (
            web_host, rcc_host, web_port, rcc_port, user_code,
        ) in itertools.zip_longest(
            args_ns.web_host, args_ns.rcc_host, args_ns.web_port, args_ns.rcc_port, args_ns.user_code,
        )
    ]
