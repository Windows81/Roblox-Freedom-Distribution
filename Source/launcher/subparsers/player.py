import launcher.routines.web_server as web_server
import launcher.subparsers._logic as sub_logic
import launcher.routines.player as player
import argparse


def subparse(
    parser: argparse.ArgumentParser,
    sub_parser: argparse.ArgumentParser,
    use_ssl: bool = False,
):
    sub_parser.add_argument(
        '--rcc_host', '-rh', type=str,
        default=None, nargs='?',
        help='Hostname or IP address to connect this program to the RCC server.',
    )
    sub_parser.add_argument(
        '--rcc_port', '-rp', type=int,
        default=2005, nargs='?',
        help='Port number to connect this program to the RCC server.',
    )
    sub_parser.add_argument(
        '--web_host', '-wh', type=str,
        default=None, nargs='?',
        help='Hostname or IP address to connect this program to the web server.',
    )
    sub_parser.add_argument(
        '--web_port', '-wp', type=int,
        default=2006, nargs='?',
        help='Port number to connect this program to the web server.',
    )
    sub_parser.add_argument(
        '--user_code', '-u',
        type=str, nargs='?',
    )
    args = parser.parse_args()

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
            web_port=web_server.port(
                port_num=args.web_port,
                is_ssl=use_ssl,
            ),
            user_code=args.user_code,
        ),
    ]


@sub_logic.launch_command(sub_logic.launch_mode.PLAYER)
def _(*a):
    return subparse(
        *a,
        use_ssl=True,
    )
