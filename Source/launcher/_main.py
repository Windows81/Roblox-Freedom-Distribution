from .subparsers.player import _
from .subparsers.server import _
from .subparsers.studio import _

from .subparsers.aux_tasks.clear_appdata import _
from .subparsers.aux_tasks.download import _

import launcher.routines._logic as routine_logic
import launcher.subparsers._logic as sub_logic
import argparse


def parse_args(args: list[str] | None) -> routine_logic.routine:
    '''
    Generates a list of routines from `launcher/subparser` scripts, filtering by the `mode` command-line parameter.
    '''
    parser = argparse.ArgumentParser()
    mode_parser = parser.add_subparsers(
        dest='mode',
    )
    sub_parsers = {
        m: mode_parser.add_parser(n, add_help=False)
        for n, m in sub_logic.MODE_ALIASES.items()
        if n != None
    }

    # Begins populating the argument namespace; errors aren't thrown because the subparser arguments aren't added yet.
    args_namespace = parser.parse_known_args(args)[0]
    mode = sub_logic.MODE_ALIASES[args_namespace.mode]
    chosen_sub_parser = sub_parsers[mode]

    # Adds parseable arguments for `chosen_sub_parser` which exist only under the current launch mode.
    sub_logic.ADD_MODE_ARGS.call_subparser(
        mode,
        parser,
        chosen_sub_parser,
    )

    # Adds parseable arguments, which exist under all launch modes, into `chosen_sub_parser`.
    sub_logic.ADD_MODE_ARGS.call_auxs(
        mode,
        parser,
        chosen_sub_parser,
    )

    # Adds '--help' argument manually after the super parser called 'parse_known_args'.
    # Otherwise, the program would stop earlier and the help-text would be incomplete.
    chosen_sub_parser.add_argument(
        '--help', '-h',
        help='show this help message and exit',
        action='help',
    )

    # Completes populating the argument namespace, with errors being thrown if an argument is invalid.
    try:
        args_namespace = parser.parse_args()
    except argparse.ArgumentError as x:
        print(x)
        chosen_sub_parser.print_help()

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


def process(args: list[str] | None = None) -> None:
    routine = parse_args(args)
    try:
        routine.wait()
    except KeyboardInterrupt:
        pass
    finally:
        del routine
