import launcher.routines.webserver as webserver
import launcher.routines.player as player
import launcher.subparsers.logic as logic
import argparse


def subparse(
    parser: argparse.ArgumentParser,
    sub_parser: argparse.ArgumentParser,
    use_ssl: bool = False,
):
    sub_parser.add_argument(
        '--rcc_host', '-rh', type=str,
        default=None, required=True,
    )
    sub_parser.add_argument(
        '--rcc_port', '-rp', type=int,
        default=2005, nargs='?',
    )
    sub_parser.add_argument(
        '--web_host', '-wh', type=str,
        default=None, nargs='?',
    )
    sub_parser.add_argument(
        '--web_port', '-wp', type=int,
        default=80, nargs='?',
    )
    sub_parser.add_argument(
        '--username', '-u',
        type=str, nargs='?',
        default='VisualPlugin'
    )
    args = parser.parse_args()
    return [
        player.argtype(
            rcc_host=args.rcc_host,
            rcc_port_num=args.rcc_port,
            web_host=args.web_host,
            web_port=webserver.port(
                port_num=args.web_port,
                is_ssl=use_ssl,
            ),
            username=args.username,
        ),
    ]


@logic.launch_command(logic.launch_mode.PLAYER)
def _(*a):
    return subparse(
        *a,
        use_ssl=False,
    )


@logic.launch_command(logic.launch_mode.PLAYER, min_version=401)
def _(*a):
    return subparse(
        *a,
        use_ssl=True,
    )
