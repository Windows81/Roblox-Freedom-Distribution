from dataclasses import dataclass
import dataclasses
from launcher.routines import player, web, rcc

from web_server._logic import port_typ, server_mode
import launcher.subparsers._logic as sub_logic
from launcher.routines import _logic as logic
import game_config as config
import logger.flog_table
import util.resource
import util.versions
import util.const
import argparse
import logger


@sub_logic.add_args(sub_logic.launch_mode.SERVER)
def subparse(
    parser: argparse.ArgumentParser,
    subparser: argparse.ArgumentParser,
) -> None:

    place_thing = subparser.add_mutually_exclusive_group(required=False)
    place_thing.add_argument(
        '--config_path',
        '--config',
        '-cp',
        type=str,
        nargs='?',
        default=util.resource.DEFAULT_CONFIG_PATH,
        help='Game-specific options; defaults to ./GameConfig.toml.  Please review each option before starting a new server up.',
    )
    place_thing.add_argument(
        '--place_path',
        '--place',
        '-pl',
        type=str,
        nargs='?',
        default=None,
        help='Path to the place file to be loaded.  Argument `config_path` can\'t be passed in when using this option.',
    )
    ip_version = subparser.add_mutually_exclusive_group()

    ip_version.add_argument(
        '--ipv4-only',
        action='store_true',
        help='Run server using IPv4 only.')
    ip_version.add_argument(
        '--ipv6-only',
        action='store_true',
        help='Run server using IPv6 only.')
    subparser.add_argument(
        '--rcc_port', '--port', '-rp', '-p',
        type=int,
        nargs='?',
        default=None,
        help='Port number for the RCC server to run from.',
    )
    subparser.add_argument(
        '--web_port', '-wp',
        type=int,
        nargs='?',
        default=None,
        help='Port number for the web server to run from.',
    )
    subparser.add_argument(
        '--run_client',
        '-rc',
        '--run_player',
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
        action='store_true',
        help='Suppresses console output.',
    )
    subparser.add_argument(
        '--rcc_log_options',
        '--rcc_log',
        '-log',
        type=str,
        nargs='*',
        default=None,
        choices=logger.flog_table.LOG_LEVEL_LIST,
        help='Filter list for which FLog types to print in RCC.',
        metavar='FLog',
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
        help="Only runs the Studio binary, skipping hosting the webserver.",
    )


def gen_log_filter(
    parser: argparse.ArgumentParser,
    args: argparse.Namespace,
) -> logger.filter.filter_type:
    if args.quiet:
        result = logger.filter.FILTER_QUIET
    else:
        result = logger.filter.FILTER_REASONABLE

    if args.rcc_log_options is not None:
        result = dataclasses.replace(
            result,
            rcc_logs=logger.filter.filter_type_rcc.parse(*args.rcc_log),
        )

    return result


@sub_logic.serialise_args(sub_logic.launch_mode.SERVER, {web.arg_type, rcc.arg_type, player.arg_type})
def _(
    parser: argparse.ArgumentParser,
    args: argparse.Namespace,
) -> list[logic.arg_type]:
    if args.place_path is not None:
        game_config = config.generate_config(args.place_path)
    else:
        game_config = config.get_cached_config(args.config_path)

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

    if args.ipv6_only:
        web_port_servers = [web_port_ipv6]
    elif args.ipv4_only:
        web_port_servers = [web_port_ipv4]
    elif game_config.game_setup.roblox_version in {util.versions.rōblox.v463}:
        web_port_servers = [web_port_ipv4, web_port_ipv6]
    else:
        web_port_servers = [web_port_ipv4]

    log_filter = gen_log_filter(parser, args)

    routine_args = []
    if not args.skip_web:
        routine_args.extend([
            web.arg_type(
                # IPv6 goes first since `localhost` also resolves first to
                # [::1] on the client.
                web_ports=web_port_servers,
                server_mode=server_mode.RCC,
                log_filter=log_filter,
                game_config=game_config,
            ),
        ])

    if not args.skip_rcc:
        routine_args.extend([
            rcc.arg_type(
                rcc_port_num=args.rcc_port,
                # since RCC only really connects to 127.0.0.1.
                web_port=web_port_ipv4,
                log_filter=log_filter,
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
                log_filter=log_filter,
                # Some CoreGUI elements don't render properly if we join too
                # early.
                launch_delay=3,
            ),
        ])
    return routine_args
