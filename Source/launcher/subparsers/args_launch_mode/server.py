import launcher.subparsers._logic as sub_logic
import launcher.routines._logic as logic
import config._main as config
import util.resource
import argparse

import launcher.routines.download as download
import launcher.routines.web_server as web_server
import launcher.routines.rcc_server as rcc_server
import launcher.routines.player as player


@sub_logic.add_args(sub_logic.launch_mode.SERVER)
def subparse(
    parser: argparse.ArgumentParser,
    subparser: argparse.ArgumentParser,
) -> None:

    subparser.add_argument(
        '--config_path', '-cp', type=str, nargs='?',
        default=util.resource.DEFAULT_CONFIG_PATH,
        help='Game-specific options; defaults to ./GameConfig.toml.  Please review each option before starting a new server up.',
    )
    subparser.add_argument(
        '--rcc_port', '-rp', type=int,
        default=2005, nargs='?',
        help='Hostname or IP address to connect this program to the web server.',
    )
    subparser.add_argument(
        '--web_port', '-wp', type=int,
        default=2006, nargs='?',
        help='Port number to connect this program to the web server.',
    )
    subparser.add_argument(
        '--run_client', '-rc',
        action='store_true',
        help='Runs an instance of the player immediately after starting the server.',
    )

    skip_mutex = subparser.add_mutually_exclusive_group()
    skip_mutex.add_argument(
        '--skip_rcc',
        action='store_true',
        help='Only runs the webserver, skipping the RCC binary completely.',
    )
    skip_mutex.add_argument(
        '--skip_rcc_popen',
        action='store_true',
        help='Runs the webserver and initialises RCC configuration, but doesn\'t execute RCCService.exe.',
    )
    skip_mutex.add_argument(
        '--skip_web',
        action='store_true',
        help='Only runs the RCC binary, skipping hosting the webserver.',
    )


@sub_logic.serialise_args(sub_logic.launch_mode.SERVER)
def _(
    parser: argparse.ArgumentParser,
    args: argparse.Namespace,
) -> list[logic.arg_type]:

    server_config = config.get_config(args.config_path)
    routine_args = []

    web_port_ipv4 = logic.port(
        port_num=args.web_port,
        is_ssl=True,
        is_ipv6=False,
    )

    web_port_ipv6 = logic.port(
        port_num=args.web_port,
        is_ssl=True,
        is_ipv6=True,
    )

    if not args.skip_web:
        routine_args.extend([
            web_server.arg_type(
                # IPv6 goes first since `localhost` resolves fist to [::1] on the client.
                web_ports=[web_port_ipv6, web_port_ipv4],
                server_config=server_config,
            ),
        ])

    if not args.skip_rcc:
        routine_args.extend([
            rcc_server.arg_type(
                rcc_port_num=args.rcc_port,
                web_port=web_port_ipv4,
                server_config=server_config,
                skip_popen=args.skip_rcc_popen,
            ),
        ])

    if args.run_client:
        routine_args.extend([
            player.arg_type(
                rcc_host='127.0.0.1',
                web_host='127.0.0.1',
                rcc_port_num=args.rcc_port,
                web_port=web_port_ipv4,
                # Some CoreGUI elements don't render properly if we join too early.
                launch_delay=3,
            ),
        ])
    return routine_args
