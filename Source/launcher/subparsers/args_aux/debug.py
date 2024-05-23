import launcher.subparsers._logic as sub_logic
import launcher.routines._logic as logic
import argparse

DEBUGGABLE_ARG_SUPERTYPE = logic.popen_arg_type


@sub_logic.add_args(sub_logic.launch_mode.ALWAYS)
def _(
    mode: sub_logic.launch_mode,
    parser: argparse.ArgumentParser,
    subparser: argparse.ArgumentParser,
) -> None:
    if DEBUGGABLE_ARG_SUPERTYPE not in sub_logic.SERIALISE_TYPE_SETS[mode]:
        return
    debug_mutex = subparser.add_mutually_exclusive_group()

    debug_mutex.add_argument(
        '--debug',
        action='store_true',
        help='Opens an instance of x96dbg and attaches it to the running "%s" binary.' % mode.value
    )

    debug_mutex.add_argument(
        '--debug_all',
        action='store_true',
        help='Opens instances of x96dbg and attaches them to all running binaries.'
    )


@sub_logic.serialise_args(sub_logic.launch_mode.ALWAYS, set())
def _(
    mode: sub_logic.launch_mode,
    args_ns: argparse.Namespace,
    args_list: list[logic.arg_type],
) -> list[logic.arg_type]:

    for i, a in enumerate(
        a
        for a in args_list
        if isinstance(a, DEBUGGABLE_ARG_SUPERTYPE)
    ):

        a.debug_x96 = (
            True
            if args_ns.debug_all
            else i == 0
            if args_ns.debug
            else False
        )

    return []
