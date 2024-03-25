from .subparsers.player import _
from .subparsers.server import _
from .subparsers.studio import _

from .subparsers.aux_tasks.clear_appdata import _
from .subparsers.aux_tasks.download import _

import launcher.routines._logic as routine_logic
import launcher.subparsers._logic as sub_logic
import argparse

MODE_ALIASES = {
    n: m
    for m in sub_logic.launch_mode
    if m != sub_logic.launch_mode.ALWAYS
    for n in [
        m.name.lower(),
    ]
}


def parse_args(parser: argparse.ArgumentParser) -> routine_logic.routine:
    '''
    Generates a list of routines from `launcher/subparser` scripts, filtering by the `mode` command-line parameter.
    '''
    mode_parser = parser.add_subparsers(
        dest='mode',
    )
    sub_parsers = {
        m: mode_parser.add_parser(n)
        for n, m in MODE_ALIASES.items()
    }

    # Begins populating the argument namespace; errors aren't thrown because the subparser arguments aren't added yet.
    args_namespace = parser.parse_known_args()[0]
    mode = MODE_ALIASES[args_namespace.mode]
    chosen_sub_parser = sub_parsers[mode]

    # Develops arguments for `chosen_sub_parser` which exist only under the current launch mode.
    sub_logic.ADD_MODE_ARGS.call_subparser(
        mode,
        parser,
        chosen_sub_parser,
    )

    # Develops arguments for `chosen_sub_parser` which exist under all launch modes.
    sub_logic.ADD_MODE_ARGS.call_auxs(
        mode,
        parser,
        chosen_sub_parser,
    )

    # Completes populating the argument namespace, with errors being thrown if an argument is invalid.
    args_namespace = parser.parse_args()

    routine_args_list = sub_logic.SERIALISE_ARGS.call_subparser(
        mode,
        parser,
        args_namespace,
    )

    sub_logic.SERIALISE_ARGS.call_auxs(
        mode,
        args_namespace,
        routine_args_list,
    )

    routine = routine_logic.routine(*routine_args_list)
    return routine


def process(parser: argparse.ArgumentParser):
    routine = parse_args(parser)
    try:
        routine.wait()
    except KeyboardInterrupt:
        pass
    finally:
        del routine
