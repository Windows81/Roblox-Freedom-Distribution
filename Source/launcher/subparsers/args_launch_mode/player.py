from launcher.routines import player

import launcher.subparsers._logic as sub_logic
from launcher.routines import _logic as logic
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


@sub_logic.serialise_args(sub_logic.launch_mode.PLAYER, {player.arg_type})
def _(
    parser: argparse.ArgumentParser,
    args: argparse.Namespace,
) -> list[logic.arg_type]:

    if args.web_host is None:
        args.web_host = args.rcc_host or 'localhost'
    if args.rcc_host is None:
        args.rcc_host = args.web_host or 'localhost'

    if args.web_port is None:
        args.web_port = args.rcc_port or 2005
    if args.rcc_port is None:
        args.rcc_port = args.web_port or 2005

    log_filter = logger.filter.filter_type(
        other_logs=not args.quiet,
    )

    return [
        player.arg_type(
            rcc_host=args.rcc_host,
            rcc_port=args.rcc_port,
            web_host=args.web_host,
            web_port=args.web_port,
            user_code=args.user_code,
            log_filter=log_filter,
        ),
    ]
