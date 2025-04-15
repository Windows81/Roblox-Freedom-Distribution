# Standard library imports
import argparse

# Local application imports
import game_config as config
import logger
import logger.flog_table
import util.const
import util.resource
import util.versions
from launcher.routines import player, rcc, studio, web
from launcher.routines import _logic as logic
import launcher.subparsers._logic as sub_logic
from web_server._logic import server_mode



@sub_logic.add_args(sub_logic.launch_mode.STUDIO)
def subparse(
    parser: argparse.ArgumentParser,
    subparser: argparse.ArgumentParser,
) -> None:
    subparser.description = (
        "RFD's bundled Studio binaries are very very very ill-prepared.  " +
        "Unless you're creating CSG unions which won't work otherwise, " +
        "I recommend using modern versions of Roblox Studio instead."
    )

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


@sub_logic.serialise_args(sub_logic.launch_mode.STUDIO, {web.arg_type, rcc.arg_type, player.arg_type})
def _(
    parser: argparse.ArgumentParser,
    args_ns: argparse.Namespace,
) -> list[logic.arg_type]:
    if args_ns.place_path is not None:
        game_config = config.generate_config(args_ns.place_path)
    else:
        game_config = config.get_cached_config(args_ns.config_path)

    web_port: int = args_ns.web_port or 20059
    log_filter = logger.filter.filter_type(
        other_logs=not args_ns.quiet,
    )

    routine_args: list[logic.arg_type] = []
    if not args_ns.skip_web:
        routine_args.extend([
            web.arg_type(
                web_port=web_port,
                is_ipv6=False,
                is_ssl=True,
                log_filter=log_filter,
                game_config=game_config,
                server_mode=server_mode.STUDIO,
            ),
        ])

    routine_args.extend([
        studio.arg_type(
            game_config=game_config,
            web_host='localhost',
            web_port=web_port,
            log_filter=log_filter,
        ),
    ])

    return routine_args
