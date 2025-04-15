# Local application imports

from launcher.routines import player

import launcher.subparsers._logic as sub_logic
from launcher.routines import _logic as logic

# Standard library imports
import argparse
import logger


@sub_logic.add_args(sub_logic.launch_mode.PLAYER)
def _(
    parser: argparse.ArgumentParser,
    subparser: argparse.ArgumentParser,
) -> None:

    subparser.add_argument(
        '--rcc_host',
        '--host',
        '-rh',
        '-h',
        type=str,
        nargs='?',
        default=None,
        help='Hostname or IP address to connect this program to the RCC server.',
    )
    subparser.add_argument(
        '--rcc_port', '--port', '-rp', '-p',
        type=int,
        nargs='?',
        default=None,
        help='Port number to connect this program to the RCC server.',
    )
    subparser.add_argument(
        '--web_host',
        '-wh',
        type=str,
        nargs='?',
        default=None,
        help='Hostname or IP address to connect this program to the web server.',
    )
    subparser.add_argument(
        '--web_port', '-wp',
        type=int,
        nargs='?',
        default=None,
        help='Port number to connect this program to the web server.',
    )
    subparser.add_argument(
        '--user_code', '-u',
        type=str,
        nargs='?',
        default=None,
    )
    subparser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Suppresses console output.',
    )
    subparser.add_argument(
        '--loud',
        action='store_true',
        help='Makes the client\'s output file log very verbosely.',
    )


def gen_log_filter(
    parser: argparse.ArgumentParser,
    args_ns: argparse.Namespace,
) -> logger.filter.filter_type:
    if args_ns.quiet:
        result = logger.filter.FILTER_QUIET
    elif args_ns.loud:
        result = logger.filter.FILTER_LOUD
    else:
        result = logger.filter.FILTER_REASONABLE

    return result


@sub_logic.serialise_args(sub_logic.launch_mode.PLAYER, {player.arg_type})
def _(
    parser: argparse.ArgumentParser,
    args_ns: argparse.Namespace,
) -> list[logic.arg_type]:

    web_host: str | None = args_ns.web_host
    rcc_host: str | None = args_ns.rcc_host
    if web_host is None:
        web_host = rcc_host or 'localhost'
    if rcc_host is None:
        rcc_host = web_host or 'localhost'

    web_port: int | None = args_ns.web_port
    rcc_port: int | None = args_ns.rcc_port
    if web_port is None:
        web_port = rcc_port or 2005
    if rcc_port is None:
        rcc_port = web_port or 2005

    log_filter = gen_log_filter(
        parser, args_ns,
    )

    return [
        player.arg_type(
            rcc_host=rcc_host,
            rcc_port=rcc_port,
            web_host=web_host,
            web_port=web_port,
            user_code=args_ns.user_code,
            log_filter=log_filter,
        ),
    ]
