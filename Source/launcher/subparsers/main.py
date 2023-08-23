from .player import _
from .server import _
from .studio import _

import launcher.routines.logic as routine_logic
import launcher.subparsers.logic as logic
import util.versions as versions
import argparse


def parse_args(parser: argparse.ArgumentParser) -> routine_logic.subparser_argtype:
    parser.add_argument(
        '--version', '-v',
        choices=list(versions.Version),
        type=lambda v: versions.VERSION_MAP[v],
    )
    mode_aliases = {
        n: m
        for m in logic.launch_mode
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
    sub_func = logic.VERSION_ROUTINES[mode_val][args.version]
    sub_parser = sub_parsers[mode_val]

    arg_obj = sub_func(parser, sub_parser)
    arg_obj.global_args = routine_logic.global_argtype(
        roblox_version=args.version,
        parser_class=mode_val.value,
    )
    return arg_obj


def process(parser: argparse.ArgumentParser):
    argtype_obj = parse_args(parser)
    mode_class = argtype_obj.global_args.parser_class
    mode_class.run(argtype_obj)
