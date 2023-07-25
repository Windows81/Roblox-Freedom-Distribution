from .logic import LaunchMode, min_version
import launcher.server
import argparse


@min_version(LaunchMode.SERVER)
def _(parser: argparse.ArgumentParser, sub_parser: argparse.ArgumentParser):
    sub_parser.add_argument(
        '--place', '-p', dest='data',
        type=lambda n: open(n, 'rb'),
        default=None, nargs='?',
    )
    sub_parser.add_argument(
        '--rcc_port', '-rp',
        dest='rcc_port', type=int,
        default=2005, nargs=1,
    )
    sub_parser.add_argument(
        '--web_port', '-wp',
        dest='web_port', type=int,
        default=80, nargs=1,
    )
    args = parser.parse_args()
    instance = launcher.server.Server(
        **{i: v for i, v in args.__dict__.items() if v}
    )
    try:
        instance.communicate()
    except KeyboardInterrupt:
        pass
    finally:
        del instance
