from ...routines import _logic as logic, rcc, web
from web_server._logic import port_typ
from .. import _logic as sub_logic
import config as config
import util.resource
import util.versions
import argparse

from launcher.routines import (
    download,
    clear_appdata,
    player,
)


@sub_logic.add_args(sub_logic.launch_mode.SERVER)
def subparse(
    parser: argparse.ArgumentParser,
    subparser: argparse.ArgumentParser,
) -> None:

    subparser.add_argument(
        '--config_path', '--config', '-cp',
        type=str,
        nargs='?',
        default=util.resource.DEFAULT_CONFIG_PATH,
        help='Game-specific options; defaults to ./GameConfig.toml.  Please review each option before starting a new server up.',
    )
    subparser.add_argument(
        '--rcc_port', '-rp', '-p',
        type=int,
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
        '--run_client', '-rc', '--run_player',
        action='store_true',
        help='Runs an instance of the player immediately after starting the server.',
    )
    subparser.add_argument(
        '--user_code', '-u',
        type=str,
        nargs='?',
        default=None,
        help='If -run_client is passed in, .',
    )
    subparser.add_argument(
        '--quiet', '-q',
        action='store_false',
        help='Suppresses console output from RCC.',
    )

    skip_mutex = subparser.add_mutually_exclusive_group()
    skip_mutex.add_argument(
        "--skip_rcc",
        action="store_true",
        help="Only runs the webserver, skipping the RCC binary completely.",
    )
    skip_mutex.add_argument(
        "--skip_rcc_popen",
        action="store_true",
        help="Runs the webserver and initialises RCC configuration, but doesn't execute `RCCService.exe`.",
    )
    skip_mutex.add_argument(
        "--skip_web",
        action="store_true",
        help="Only runs the RCC binary, skipping hosting the webserver.",
    )


@sub_logic.serialise_args(sub_logic.launch_mode.SERVER, {web.arg_type, rcc.arg_type, player.arg_type})
def _(
    parser: argparse.ArgumentParser,
    args: argparse.Namespace,
) -> list[logic.arg_type]:
    game_config = config.get_cached_config(args.config_path)
    routine_args = []

    if args.web_port is None:
        args.web_port = args.rcc_port or 2005
    if args.rcc_port is None:
        args.rcc_port = args.web_port or 2005

    web_port_ipv4 = port_typ(
        port_num=args.web_port,
        is_ssl=True,
        is_ipv6=False,
    )

    web_port_ipv6 = port_typ(
        port_num=args.web_port,
        is_ssl=True,
        is_ipv6=True,
    )

    if game_config.game_setup.roblox_version in {
        util.versions.rōblox.v463,
    }:
        # Only 2021E support IPv6.
        web_port_servers = [
            web_port_ipv4,
            web_port_ipv6,
        ]
    else:
        web_port_servers = [
            web_port_ipv4,
        ]

    if not args.skip_web:
        routine_args.extend([
            web.arg_type(
                # IPv6 goes first since `localhost` also resolves first to [::1] on the client.
                web_ports=web_port_servers,
                quiet=args.quiet,
                game_config=game_config,
            ),
        ])

    if not args.skip_rcc:
        routine_args.extend([
            rcc.arg_type(
                rcc_port_num=args.rcc_port,
                # since RCC only really connects to 127.0.0.1.
                web_port=web_port_ipv4,
                quiet=args.quiet,
                skip_popen=args.skip_rcc_popen,
                game_config=game_config,
            ),
        ])

    if args.run_client:
        routine_args.extend([
            player.arg_type(
                rcc_host='127.0.0.1',
                web_host='127.0.0.1',
                rcc_port_num=args.rcc_port,
                # since RCC only really connects to 127.0.0.1.
                web_port=web_port_ipv4,
                user_code=args.user_code,
                # Some CoreGUI elements don't render properly if we join too early.
                launch_delay=3,
            ),
        ])
    return routine_args
