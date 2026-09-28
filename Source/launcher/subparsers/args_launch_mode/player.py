import argparse
import itertools

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
        help='Determines the user code for the player which joins the server.\nUser codes derive a username, user iden number, and other characteristics of any particular player.',
    )


@sub_logic.serialise_args(sub_logic.launch_mode.PLAYER)
def _(
    parser: argparse.ArgumentParser,
    args_ns: argparse.Namespace,
) -> list[logic.base_entry]:

    return [
        player.obj_type(
            rcc_host=rcc_host,
            rcc_port=rcc_port,
            web_host=web_host,
            web_port=web_port,
            user_code=user_code,
        )
        for (
            web_host, rcc_host, web_port, rcc_port, user_code,
        ) in itertools.zip_longest(
            args_ns.web_host, args_ns.rcc_host, args_ns.web_port, args_ns.rcc_port, args_ns.user_code,
        )
    ]
