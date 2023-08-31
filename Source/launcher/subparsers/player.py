import launcher.subparsers._logic as sub_logic
import launcher.routines.player as player
import launcher.routines._logic as logic
import argparse


@sub_logic.add_args(sub_logic.launch_mode.PLAYER)
def _(
    parser: argparse.ArgumentParser,
    subparser: argparse.ArgumentParser,
) -> None:

    subparser.add_argument(
        '--rcc_host', '-rh', type=str,
        default=None, nargs='?',
        help='Hostname or IP address to connect this program to the RCC server.',
    )
    subparser.add_argument(
        '--rcc_port', '-rp', type=int,
        default=2005, nargs='?',
        help='Port number to connect this program to the RCC server.',
    )
    subparser.add_argument(
        '--web_host', '-wh', type=str,
        default=None, nargs='?',
        help='Hostname or IP address to connect this program to the web server.',
    )
    subparser.add_argument(
        '--web_port', '-wp', type=int,
        default=2006, nargs='?',
        help='Port number to connect this program to the web server.',
    )
    subparser.add_argument(
        '--user_code', '-u',
        type=str, nargs='?',
    )


@sub_logic.serialise_args(sub_logic.launch_mode.PLAYER)
def _(
    parser: argparse.ArgumentParser,
    args: argparse.Namespace,
) -> list[logic.arg_type]:

    if not (args.web_host or args.rcc_host):
        parser.error('No hostname requested; add --web_host or --rcc_host.')
    args.web_host, args.rcc_host = \
        args.web_host or args.rcc_host, \
        args.rcc_host or args.web_host

    return [
        player.arg_type(
            rcc_host=args.rcc_host,
            rcc_port_num=args.rcc_port,
            web_host=args.web_host,
            web_port=logic.port(
                port_num=args.web_port,
                is_ssl=True,
            ),
            user_code=args.user_code,
        ),
    ]
