from .logic import LaunchMode, VERSION_ROUTINES
from .player import _
from .server import _
from .studio import _
import argparse
import versions


def parse_args(parser: argparse.ArgumentParser):
    parser.add_argument(
        '--version', '-v',
        choices=list(versions.Version),
        type=lambda v: versions.VERSION_MAP[v],
    )
    mode_aliases = {
        n: m
        for m in LaunchMode
        for n in [
            m.name.lower(),
        ]
    }

    mode_parser: argparse._SubParsersAction = parser.add_subparsers(dest='mode')
    sub_parsers = {
        m: mode_parser.add_parser(n)
        for n, m in mode_aliases.items()
    }
    (args, _) = parser.parse_known_args()
    mode_val = mode_aliases[args.mode]
    sub_func = VERSION_ROUTINES[mode_val][args.version]
    sub_parser = sub_parsers[mode_val]
    return sub_func(parser, sub_parser)
