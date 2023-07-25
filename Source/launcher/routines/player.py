from .logic import LaunchMode, min_version
import launcher.player
import argparse


@min_version(LaunchMode.PLAYER)
def _(parser: argparse.ArgumentParser, sub_parser: argparse.ArgumentParser):
    sub_parser.add_argument(
        '--rcc_host', '-rh', type=str,
        default=None, required=True,
    )
    sub_parser.add_argument(
        '--rcc_port', '-rp', type=int,
        default=2005, nargs=1,
    )
    sub_parser.add_argument(
        '--web_host', '-wh', type=str,
        default=None, nargs='?',
    )
    sub_parser.add_argument(
        '--web_port', '-wp', type=int,
        default=80, nargs=1,
    )
    sub_parser.add_argument(
        '--username', '-u',
        type=str, nargs='?',
        default='VisualPlugin'
    )
    args = parser.parse_args()
    instance = launcher.player.Player(
        version=args.version,
        rcc_host=args.rcc_host,
        rcc_port=args.rcc_port,
        web_host=args.web_host,
        web_port=args.web_port,
        username=args.username,
    )
    try:
        instance.communicate()
    except KeyboardInterrupt:
        pass
    finally:
        del instance


@min_version(LaunchMode.PLAYER, version_num=400)
def _(parser: argparse.ArgumentParser, sub_parser: argparse.ArgumentParser):
    raise NotImplementedError("This version hasn't been properly configured yet.")
    sub_parser.add_argument(
        '--rcc_host', '-rh', type=str,
        default=None, required=True,
    )
    sub_parser.add_argument(
        '--rcc_port', '-rp',
        type=int, nargs='?',
    )
    sub_parser.add_argument(
        '--web_host', '-wh', type=str,
        default=None, nargs='?',
    )
    sub_parser.add_argument(
        '--web_port', '-wp', type=int,
        default=80, nargs='?',
    )
    sub_parser.add_argument(
        '--username', '-u',
        type=str, nargs='?',
        default='VisualPlugin'
    )
    args = parser.parse_args()
    instance = launcher.player.Player(
        version=args.version,
        rcc_host=args.rcc_host,
        rcc_port=args.rcc_port,
        web_host=args.web_host,
        web_port=args.web_port,
        username=args.username,
    )
    try:
        instance.communicate()
    except KeyboardInterrupt:
        pass
    finally:
        del instance
