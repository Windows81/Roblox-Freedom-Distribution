import argparse
from routines import _logic as logic
import launcher.subparsers._logic as sub_logic

DEBUGGABLE_ARG_SUPERTYPE = logic.popen_entry


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
    debug_mutex = subparser.add_mutually_exclusive_group()

    debug_mutex.add_argument(
        '--debug',
        action='store_true',
        help='Opens an instance of x96dbg and attaches it to the running "%s" binary.' %
        mode.value)

    debug_mutex.add_argument(
        '--debug_all',
        action='store_true',
        help='Opens instances of x96dbg and attaches them to all running binaries.')


@sub_logic.serialise_aux_args(*AUX_MODES)
def _(
    mode: sub_logic.launch_mode,
    args_ns: argparse.Namespace,
    args_list: list[logic.base_entry],
) -> list[logic.base_entry]:

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
