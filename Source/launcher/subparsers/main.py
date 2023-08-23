from .player import _
from .server import _
from .studio import _

import launcher.routines.logic as routine_logic
import launcher.subparsers.logic as logic
import util.versions as versions
import argparse


def parse_args(parser: argparse.ArgumentParser):
    mode_aliases = {
        n: m
        for m in logic.launch_mode
        for n in [
            m.name.lower(),
        ]
    }
    mode_parser = parser.add_subparsers(
        dest='mode',
    )
    sub_parsers = {
        m: mode_parser.add_parser(n)
        for n, m in mode_aliases.items()
    }

    parser.add_argument(
        '--version', '-v',
        choices=list(versions.Version),
        type=lambda v: versions.VERSION_MAP[v],
    )

    args = parser.parse_known_args()[0]
    mode_val = mode_aliases[args.mode]
    sub_func = logic.VERSION_ROUTINES[mode_val][args.version]
    sub_parser = sub_parsers[mode_val]
    args_list = sub_func(parser, sub_parser)

    return routine_logic.routine(
        routine_logic.global_argtype(
            roblox_version=args.version,
        ),
        *args_list,
    )


def process(parser: argparse.ArgumentParser):
    routine = parse_args(parser)
    try:
        routine.wait()
    except KeyboardInterrupt:
        pass
    finally:
        del routine
