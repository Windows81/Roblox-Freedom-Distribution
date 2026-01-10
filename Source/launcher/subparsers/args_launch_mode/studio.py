# Standard library imports
import argparse
import dataclasses

# Local application imports
import game_config as config
import logger
import util.resource
from routines import player, rcc, studio, web
from routines import _logic as logic
import launcher.subparsers._logic as sub_logic
from web_server._logic import server_mode


@sub_logic.add_args(sub_logic.launch_mode.STUDIO)
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
    subparser.add_argument(
        '--web_port', '-wp', '-p',
        type=int,
        nargs='?',
        default=None,
        help='Port number for the locally-hosted web server to run from.',
    )

    subparser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Suppresses console output.',
    )
    subparser.add_argument(
        "--skip_web",
        action="store_true",
        help="Skips hosting the webserver.",
    )
    subparser.add_argument(
        "--skip_studio",
        action="store_true",
        help="Skips opening Studio.",
    )


@sub_logic.serialise_args(sub_logic.launch_mode.STUDIO, {web.obj_type, rcc.obj_type, player.obj_type})
def _(
    parser: argparse.ArgumentParser,
    args_ns: argparse.Namespace,
) -> list[logic.obj_type]:
    if args_ns.place_path is not None:
        game_config = config.generate_config(args_ns.place_path)
    else:
        game_config = config.get_cached_config(args_ns.config_path)

    web_port: int = args_ns.web_port or 20059
    log_filter = dataclasses.replace(
        logger.filter.FILTER_REASONABLE,
        other_logs=not args_ns.quiet,
    )

    routine_args: list[logic.obj_type] = []
    if not args_ns.skip_studio:
        routine_args.extend([
            studio.obj_type(
                game_config=game_config,
                web_host='localhost',
                web_port=web_port,
                log_filter=log_filter,
            ),
        ])

    if not args_ns.skip_web:
        routine_args.extend([
            web.obj_type(
                web_port=web_port,
                is_ipv6=False,
                is_ssl=True,
                log_filter=log_filter,
                game_config=game_config,
                server_mode=server_mode.STUDIO,
            ),
        ])

    return routine_args
