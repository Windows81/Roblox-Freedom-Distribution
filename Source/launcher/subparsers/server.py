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

    skip_mutex = sub_parser.add_mutually_exclusive_group()
    skip_mutex.add_argument(
        '--skip_rcc',
        action='store_true',
    )
    skip_mutex.add_argument(
        '--skip_web',
        action='store_true',
    )

    args = parser.parse_args()
    routine_args = []

    if not args.skip_rcc:
        routine_args.extend([
            webserver.argtype(
                port=webserver.port(
                    port_num=args.web_port,
                    is_ssl=use_ssl,
                ),
            ),
        ])

    if not args.skip_web:
        routine_args.extend([
            server.argtype(
                place_path=args.place,
                rcc_port_num=args.rcc_port,
                web_port=webserver.port(
                    port_num=args.web_port,
                    is_ssl=use_ssl,
                ),
                **kwargs,
            ),
        ])

    if args.run_client:
        routine_args.extend([
            player.argtype(
                rcc_host='localhost',
                rcc_port_num=args.rcc_port,
                web_port=webserver.port(
                    port_num=args.web_port,
                    is_ssl=use_ssl,
                ),
            ),
        ])
    return routine_args


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


@logic.launch_command(logic.launch_mode.SERVER, min_version=401)
def _(*a):
    return subparse(
        *a,
        use_ssl=True,
        additional_web_ports=set(),
    )
