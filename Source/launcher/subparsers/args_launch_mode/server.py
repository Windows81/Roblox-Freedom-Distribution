from launcher.routines import player, web, rcc

import launcher.subparsers._logic as sub_logic
from launcher.routines import _logic as logic
from web_server._logic import server_mode
import game_config as config
import logger.flog_table
import logger.bcolors
import util.resource
import util.versions
import dataclasses
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
        '--no_colour', '--no_color',
        action='store_true',
        help='Suppresses ANSI colour codes.',
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
    args_ns: argparse.Namespace,
) -> logger.filter.filter_type:
    if args_ns.quiet:
        result = logger.filter.FILTER_QUIET
    else:
        result = logger.filter.FILTER_REASONABLE

    if args_ns.rcc_log_options is not None:
        result = dataclasses.replace(
            result,
            rcc_logs=logger.filter.filter_type_rcc.parse(*args_ns.rcc_log),
        )

    if args_ns.no_colour:
        result = dataclasses.replace(
            result,
            bcolors=logger.bcolors.BCOLORS_INVISIBLE,
        )

    return result


@sub_logic.serialise_args(sub_logic.launch_mode.SERVER, {web.arg_type, rcc.arg_type, player.arg_type})
def _(
    parser: argparse.ArgumentParser,
    args_ns: argparse.Namespace,
) -> list[logic.arg_type]:
    if args_ns.place_path is not None:
        game_config = config.generate_config(args_ns.place_path)
    else:
        game_config = config.get_cached_config(args_ns.config_path)

    web_port: int = args_ns.web_port or 2005
    rcc_port: int = args_ns.rcc_port or 2005
    has_ipv6: bool = not args_ns.ipv4_only
    has_ipv4: bool = not args_ns.ipv6_only

    log_filter = gen_log_filter(
        parser, args_ns,
    )

    web_routine_args = []
    if has_ipv6:
        # IPv6 goes first since `localhost` also resolves first to
        # [::1] on the client.
        web_routine_args.append(web.arg_type(
            web_port=web_port,
            is_ssl=True,
            is_ipv6=True,
            server_mode=server_mode.RCC,
            log_filter=log_filter,
            game_config=game_config,
        ))
    if has_ipv4:
        web_routine_args.append(web.arg_type(
            web_port=web_port,
            is_ssl=True,
            is_ipv6=False,
            server_mode=server_mode.RCC,
            log_filter=log_filter,
            game_config=game_config,
        ))

    routine_args = []
    if not args_ns.skip_web:
        routine_args.extend(web_routine_args)

    if not args_ns.skip_rcc:
        routine_args.append(
            rcc.arg_type(
                # TODO: add support for RCC to connect to hosts other than `localhost`.
                web_host='localhost',
                web_port=web_port,
                rcc_port=rcc_port,
                log_filter=log_filter,
                skip_popen=args_ns.skip_rcc_popen,
                game_config=game_config,
            ),
        )

    if args_ns.run_client:
        routine_args.extend([
            player.arg_type(
                rcc_host='127.0.0.1',
                web_host='127.0.0.1',
                rcc_port=rcc_port,
                web_port=web_port,
                user_code=args_ns.user_code,
                log_filter=log_filter,
                # Some CoreGUI elements don't render properly if we join too
                # early.
                launch_delay=3,
            ),
        ])
    return routine_args
