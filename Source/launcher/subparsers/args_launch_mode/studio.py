from launcher.routines import player, web, rcc, studio

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


@sub_logic.add_args(sub_logic.launch_mode.STUDIO)
def subparse(
    parser: argparse.ArgumentParser,
    subparser: argparse.ArgumentParser,
) -> None:
    subparser.description = (
        "RFD's bundled Studio binaries are very very very ill-prepared.  "
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
        help='Port number for the web server to run from.',
    )

    subparser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Suppresses console output.',
    )
    subparser.add_argument(
        "--skip_web",
        action="store_true",
        help="Only runs the RCC binary, skipping hosting the webserver.",
    )


@sub_logic.serialise_args(sub_logic.launch_mode.STUDIO,
                          {web.arg_type, rcc.arg_type, player.arg_type})
def _(
    parser: argparse.ArgumentParser,
    args: argparse.Namespace,
) -> list[logic.arg_type]:
    if args.place_path is not None:
        game_config = config.generate_config(args.place_path)
    else:
        game_config = config.get_cached_config(args.config_path)

    if args.web_port is None:
        args.web_port = 20059

    web_port = port_typ(
        port_num=args.web_port,
        is_ssl=True,
        is_ipv6=False,
    )

    log_filter = logger.filter.filter_type(
        other_logs=not args.quiet,
    )

    routine_args: list[logic.arg_type] = []
    if not args.skip_web:
        routine_args.extend([
            web.arg_type(
                web_ports=[web_port],
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
