import launcher.routines.web_server as web_server
import launcher.routines.rcc_server as rcc_server
import launcher.subparsers._logic as sub_logic
import launcher.routines.player as player
import launcher.routines._logic as logic
import util.resource
import argparse


@sub_logic.add_args(sub_logic.launch_mode.SERVER)
def subparse(
    parser: argparse.ArgumentParser,
    subparser: argparse.ArgumentParser,
) -> None:

    subparser.add_argument(
        '--config_path', '-cp', type=str, nargs='?',
        default=util.resource.DEFAULT_CONFIG_PATH,
    )
    subparser.add_argument(
        '--rcc_port', '-rp', type=int,
        default=2005, nargs='?',
    )
    subparser.add_argument(
        '--web_port', '-wp', type=int,
        default=2006, nargs='?',
    )
    subparser.add_argument(
        '--run_client', '-rc',
        action='store_true',
    )

    skip_mutex = subparser.add_mutually_exclusive_group()
    skip_mutex.add_argument(
        '--skip_rcc',
        action='store_true',
    )
    skip_mutex.add_argument(
        '--skip_web',
        action='store_true',
    )


@sub_logic.serialise_args(sub_logic.launch_mode.SERVER)
def _(
    parser: argparse.ArgumentParser,
    args: argparse.Namespace,
) -> list[logic.arg_type]:
    server_config = util.resource.get_config_full_path(args.config_path)
    routine_args = []

    if not args.skip_web:
        routine_args.extend([
            web_server.arg_type(
                web_ports=set([
                    logic.port(
                        port_num=args.web_port,
                        is_ssl=True,
                    ),
                ]),
                server_config=server_config,
            ),
        ])

    if not args.skip_rcc:
        routine_args.extend([
            rcc_server.arg_type(
                rcc_port_num=args.rcc_port,
                web_port=logic.port(
                    port_num=args.web_port,
                    is_ssl=True,
                ),
                server_config=server_config,
            ),
        ])

    if args.run_client:
        routine_args.extend([
            player.arg_type(
                rcc_host='127.0.0.1',
                web_host='127.0.0.1',
                rcc_port_num=args.rcc_port,
                web_port=logic.port(
                    port_num=args.web_port,
                    is_ssl=True,
                ),
            ),
        ])
    return routine_args
