# Standard library imports
import argparse
import dataclasses
import socket

# Local application imports
import game_config as config
import logger.flog_table
import logger.bcolors
import util.resource
import util.const
import logger

from routines import player, rcc, web
from routines import _logic as logic

import launcher.subparsers._logic as sub_logic


def resolve_port_pairs(
    web_ports: list[int | None],
    rcc_ports: list[int | None],
    count: int,
) -> list[tuple[int, int]]:
    result: list[tuple[int, int]] = []
    used_web_ports: set[int] = set()
    used_rcc_ports: set[int] = set()
    next_web_port = util.const.RFD_DEFAULT_PORT

    for index in range(count):
        web_port = web_ports[index] if index < len(web_ports) else None
        rcc_port = rcc_ports[index] if index < len(rcc_ports) else None

        if web_port is None:
            web_port = next_web_port
            while web_port in used_web_ports:
                web_port += 1

        if rcc_port is None:
            rcc_port = web_port
            while (
                rcc_port in used_rcc_ports or
                not is_udp_port_available(rcc_port)
            ):
                rcc_port += 1

        used_web_ports.add(web_port)
        used_rcc_ports.add(rcc_port)
        next_web_port = max(next_web_port, web_port) + 1
        result.append((web_port, rcc_port))

    return result


def is_udp_port_available(port: int) -> bool:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.bind(('', port))
    except OSError:
        return False
    return True


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
        nargs='*',
        default=[util.resource.DEFAULT_CONFIG_PATH],
        help='Game-specific options; defaults to ./GameConfig.toml.  Please review each option before starting a new server up.',
    )
    place_thing.add_argument(
        '--place_path',
        '--place',
        '-pl',
        type=str,
        nargs='*',
        default=[],
        help='Path to the place file to be loaded.  Argument `config_path` can\'t be passed in when using this option.',
    )
    ip_version = subparser.add_mutually_exclusive_group()

    ip_version.add_argument(
        '--ipv4-only',
        action='store_true',
        help='Run server using IPv4 only.',
    )
    ip_version.add_argument(
        '--ipv6-only',
        action='store_true',
        help='Run server using IPv6 only.',
    )
    subparser.add_argument(
        '--rcc_port', '--port', '-rp',
        type=int,
        nargs='*',
        default=[],
        help='Port number for the RCC server to run from.',
    )
    subparser.add_argument(
        '--web_port', '--webserver_port', '-wp', '-p',
        type=int,
        nargs='*',
        default=[],
        help='Port number for the web server to run from.',
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
        help='If --run_client is passed in, determines the user code for the player which joins the server.\nUser codes derive a user name, user iden number, and other characteristics of any particular player',
    )
    subparser.add_argument(
        '--frontend_proxy',
        type=str,
        default=None,
        help='Forward unmatched web paths to a frontend server such as http://127.0.0.1:3000.',
    )

    log_group = subparser.add_mutually_exclusive_group()
    log_group.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Suppresses console output.',
    )
    log_group.add_argument(
        '--loud',
        action='store_true',
        help='Makes RCC console output very verbose.',
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
        "--skip_web",
        action="store_true",
        help="Only runs the Studio binary, skipping hosting the webserver.",
    )


def gen_log_filter(
    parser: argparse.ArgumentParser,
    args_ns: argparse.Namespace,
) -> logger.obj_type:
    if args_ns.quiet:
        result = logger.PRINT_QUIET
    elif args_ns.loud:
        result = logger.PRINT_LOUD
    else:
        result = logger.PRINT_REASONABLE

    if args_ns.rcc_log_options is not None:
        result = dataclasses.replace(
            result,
            rcc_logs=logger.filter.filter_type_bin.parse(*args_ns.rcc_log),
        )

    if args_ns.no_colour:
        result = dataclasses.replace(
            result,
            bcolors=logger.bcolors.BCOLORS_INVISIBLE,
        )

    return result


@sub_logic.serialise_args(sub_logic.launch_mode.SERVER)
def _(
    parser: argparse.ArgumentParser,
    args_ns: argparse.Namespace,
) -> list[logic.base_entry]:
    if len(args_ns.place_path) > 0:
        game_configs = [
            config.generate_config(v)
            for v in args_ns.place_path
        ]
    else:
        game_configs = [
            config.get_cached_config(v)
            for v in args_ns.config_path
        ]

    has_ipv6: bool = not args_ns.ipv4_only
    has_ipv4: bool = not args_ns.ipv6_only

    web_routine_args = set[logic.base_entry]()
    rcc_routine_args = set[logic.base_entry]()
    log_filter = gen_log_filter(
        parser, args_ns,
    )

    port_pairs = resolve_port_pairs(
        list(args_ns.web_port),
        list(args_ns.rcc_port),
        len(game_configs),
    )

    for (
        (web_port, rcc_port), game_config,
    ) in zip(
        port_pairs,
        game_configs,
    ):
        if not args_ns.skip_web:
            if has_ipv6:
                # IPv6 goes first since `localhost` also resolves first to [::1] on the client.
                web_routine_args.add(web.obj_type(
                    web_port=web_port,
                    is_ssl=True,
                    is_ipv6=True,
                    frontend_proxy=args_ns.frontend_proxy,
                    server_mode=web.SERVER_MODE_TYPE.RCC,
                    logger=log_filter,
                    game_config=game_config,
                ))
            if has_ipv4:
                web_routine_args.add(web.obj_type(
                    web_port=web_port,
                    is_ssl=True,
                    is_ipv6=False,
                    frontend_proxy=args_ns.frontend_proxy,
                    server_mode=web.SERVER_MODE_TYPE.RCC,
                    logger=log_filter,
                    game_config=game_config,
                ))

        if not args_ns.skip_rcc:
            rcc_routine_args.add(
                rcc.obj_type(
                    # TODO: add support for RCC to connect to hosts other than `localhost`.
                    web_host='localhost',
                    web_port=web_port,
                    rcc_port=rcc_port,
                    logger=log_filter,
                    game_config=game_config,
                ),
            )

        if args_ns.run_client:
            rcc_routine_args.add(
                player.obj_type(
                    rcc_host='127.0.0.1',
                    web_host='127.0.0.1',
                    rcc_port=rcc_port,
                    web_port=web_port,
                    user_code=args_ns.user_code,
                    logger=log_filter,
                    # Some CoreGUI elements don't render properly if we join too early.
                    launch_delay=3,
                ),
            )

    return [*web_routine_args, *rcc_routine_args]
