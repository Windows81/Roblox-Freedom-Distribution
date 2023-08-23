import launcher.routines.webserver as webserver
import launcher.routines.server as server
import launcher.routines.player as player
import launcher.subparsers.logic as logic
import argparse


def subparse(
    parser: argparse.ArgumentParser,
    sub_parser: argparse.ArgumentParser,
    use_ssl: bool = False,
    **kwargs,
):

    sub_parser.add_argument(
        '--place', '-p',
        dest='place', type=str,
        required=True,
    )
    sub_parser.add_argument(
        '--rcc_port', '-rp',
        dest='rcc_port', type=int,
        default=2005, nargs='?',
    )
    sub_parser.add_argument(
        '--web_port', '-wp',
        dest='web_port', type=int,
        default=80, nargs='?',
    )
    sub_parser.add_argument(
        '--run_client', '-rc',
        action='store_true',
    )

    args = parser.parse_args()
    return [
        webserver.argtype(
            port=webserver.port(
                port_num=args.web_port,
                is_ssl=use_ssl,
            ),
        ),
        server.argtype(
            place_path=args.place,
            rcc_port_num=args.rcc_port,
            web_port=webserver.port(
                port_num=args.web_port,
                is_ssl=use_ssl,
            ),
            **kwargs,
        ),
    ] + [
        player.argtype(
            rcc_host='localhost',
            rcc_port_num=args.rcc_port,
            web_port=webserver.port(
                port_num=args.web_port,
                is_ssl=use_ssl,
            ),
        ),
    ] if args.run_client else []


@logic.launch_command(logic.launch_mode.SERVER)
def _(*a):
    return subparse(
        *a,
        use_ssl=False,
        additional_web_ports=set([
            webserver.port(
                port_num=443,
                is_ssl=True,
            ),
        ]),
    )


@logic.launch_command(logic.launch_mode.SERVER, min_version=400)
def _(*a):
    return subparse(
        *a,
        use_ssl=True,
        additional_web_ports=set(),
    )
