# Standard library imports
import argparse
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
        '--rcc_host', '--host', '-rh', '-h',
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
        '--web_host', '--webserver_host', '-wh',
        type=str,
        nargs='?',
        default=None,
        help='Hostname or IP address to connect this program to the web server.',
    )
    subparser.add_argument(
        '--web_port', '--webserver_port', '-wp',
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
        help='Makes the client\'s output file log very verbosely.',
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
        player.obj_type(
            rcc_host=rcc_host,
            rcc_port=rcc_port,
            web_host=web_host,
            web_port=web_port,
            user_code=args_ns.user_code,
            logger=log_filter,
        ),
    ]
