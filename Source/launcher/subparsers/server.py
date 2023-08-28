import launcher.routines.webserver as webserver
import launcher.routines.server as server
import launcher.routines.player as player
import launcher.subparsers.logic as logic
import util.resource
import argparse


def subparse(
    parser: argparse.ArgumentParser,
    sub_parser: argparse.ArgumentParser,
    additional_web_ports: set[webserver.port],
    use_ssl: bool = False,
    **kwargs,
):

    sub_parser.add_argument(
        '--config_path', '-cp', type=str, nargs='?',
        default=util.resource.DEFAULT_CONFIG_PATH,
    )
    sub_parser.add_argument(
        '--rcc_port', '-rp', type=int,
        default=2005, nargs='?',
    )
    sub_parser.add_argument(
        '--web_port', '-wp', type=int,
        default=2006, nargs='?',
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
    server_config = util.resource.get_config_full_path(args.config_path)
    routine_args = []

    if not args.skip_web:
        routine_args.extend([
            webserver.argtype(
                web_ports=set([
                    webserver.port(
                        port_num=args.web_port,
                        is_ssl=use_ssl,
                    ),
                    *additional_web_ports,
                ]),
                server_config=server_config,
                **kwargs,
            ),
        ])

    if not args.skip_rcc:
        routine_args.extend([
            server.argtype(
                rcc_port_num=args.rcc_port,
                web_port=webserver.port(
                    port_num=args.web_port,
                    is_ssl=use_ssl,
                ),
                server_config=server_config,
                **kwargs,
            ),
        ])

    if args.run_client:
        routine_args.extend([
            player.argtype(
                rcc_host='127.0.0.1',
                web_host='127.0.0.1',
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
        use_ssl=True,
        additional_web_ports=set(),
    )
