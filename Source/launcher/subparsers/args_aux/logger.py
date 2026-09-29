import argparse
import dataclasses


from routines import _logic as logic
import launcher.subparsers._logic as sub_logic
import logger.flog_table
import logger.bcolors
import logger


AUX_MODES = (
    sub_logic.launch_mode.PLAYER,
    sub_logic.launch_mode.SERVER,
    sub_logic.launch_mode.STUDIO,
)


@sub_logic.add_aux_args(*AUX_MODES)
def _(
    mode: sub_logic.launch_mode,
    parser: argparse.ArgumentParser,
    subparser: argparse.ArgumentParser,
) -> None:
    log_group = subparser.add_mutually_exclusive_group()

    log_group.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Suppresses console output.',
    )

    log_group.add_argument(
        '--loud',
        action='store_true',
        help='Makes console output very verbose.',
    )

    if mode == sub_logic.launch_mode.SERVER:
        # TODO: unify options for a future breaking release.
        subparser.add_argument(
            '--rcc_log_options',
            '--rcc_log',
            '-log',
            dest='log_options',
            type=str,
            nargs='*',
            default=None,
            help='Filter list for which FLog types to print in RCC logs.',
            metavar='[FLog]Output, [FLog]Network, et c.',
        )
    else:
        subparser.add_argument(
            '--log_options',
            '--log',
            '-log',
            dest='log_options',
            type=str,
            nargs='*',
            default=None,
            help='Filter list for which FLog types to print in log files.',
            metavar='[FLog]Output, [FLog]LocalStorage, et c.',
        )

    subparser.add_argument(
        '--no_colour', '--no_color',
        action='store_true',
        help='Suppresses ANSI colour codes.',
    )


def gen_log_filter(args_ns: argparse.Namespace) -> logger.obj_type:
    if args_ns.quiet:
        result = logger.PRINT_QUIET
    elif args_ns.loud:
        result = logger.PRINT_LOUD
    else:
        result = logger.PRINT_REASONABLE

    if args_ns.log_options is not None:
        mods = logger.filter.filter_type_bin.parse(*args_ns.log_options)
        result = dataclasses.replace(result, bin_logs=mods)

    if args_ns.no_colour:
        result = dataclasses.replace(
            result,
            bcolors=logger.bcolors.BCOLORS_INVISIBLE,
        )

    return result


@sub_logic.serialise_aux_args(*AUX_MODES)
def _(
    mode: sub_logic.launch_mode,
    args_ns: argparse.Namespace,
    args_list: list[logic.base_entry],
) -> list[logic.base_entry]:

    log_filter = gen_log_filter(args_ns)
    for a in args_list:
        if not isinstance(a, logic.loggable_entry):
            continue
        a.logger = log_filter

    return []
