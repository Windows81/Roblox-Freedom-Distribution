from launcher.routines import player

from launcher.routines import _logic as logic
import launcher.subparsers._logic as sub_logic
from web_server._logic import port_typ
import argparse


@sub_logic.add_args(sub_logic.launch_mode.PLAYER)
def _(
    parser: argparse.ArgumentParser,
    subparser: argparse.ArgumentParser,
) -> None:

    subparser.add_argument(
        '--rcc_host', '-rh', '-h',
        type=str,
        nargs='?',
        default=None,
        help='Hostname or IP address to connect this program to the RCC server.',
    )
    subparser.add_argument(
        '--rcc_port', '-rp', '-p',
        type=int,
        nargs='?',
        default=None,
        help='Port number to connect this program to the RCC server.',
    )
    subparser.add_argument(
        '--web_host', '-wh',
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

    return [
        player.arg_type(
            rcc_host=args.rcc_host,
            rcc_port_num=args.rcc_port,
            web_host=args.web_host,
            web_port=port_typ(
                port_num=args.web_port,
                is_ssl=True,
            ),
            user_code=args.user_code,
        ),
    ]
