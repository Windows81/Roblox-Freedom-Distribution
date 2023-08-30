from .subparsers.player import _
from .subparsers.server import _
from .subparsers.studio import _

import launcher.routines._logic as routine_logic
import launcher.subparsers._logic as sub_logic
import argparse


def parse_args(parser: argparse.ArgumentParser) -> routine_logic.routine:
    mode_aliases = {
        n: m
        for m in sub_logic.launch_mode
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

    args = parser.parse_known_args()[0]
    mode_val = mode_aliases[args.mode]
    sub_func = sub_logic.LAUNCH_ROUTINES[mode_val]
    sub_parser = sub_parsers[mode_val]
    args_list = sub_func(parser, sub_parser)
    return routine_logic.routine(*args_list)


def process(parser: argparse.ArgumentParser):
    routine = parse_args(parser)
    try:
        routine.wait()
    except KeyboardInterrupt:
        pass
    finally:
        del routine
