import argparse
from routines import _logic as logic
import launcher.subparsers._logic as sub_logic
import util.resource


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
        help='open an instance of x96dbg and attaches it to the running "%s" binary' % mode.value,
    )

    debug_mutex.add_argument(
        '--debug_all',
        action='store_true',
        help='open instances of x96dbg and attaches them to all running binaries',
    )


@sub_logic.serialise_aux_args(*AUX_MODES)
def _(
    mode: sub_logic.launch_mode,
    args_ns: argparse.Namespace,
    args_list: list[logic.base_entry],
) -> list[logic.base_entry]:

    for a in args_list:
        if not isinstance(a, logic.bin_entry):
            continue
        if args_ns.debug_all:
            a.debug_x96 = True
        elif args_ns.debug:
            a.debug_x96 = (mode, a.BIN_SUBTYPE) in {
                (sub_logic.launch_mode.PLAYER, util.resource.bin_subtype.PLAYER),
                (sub_logic.launch_mode.SERVER, util.resource.bin_subtype.SERVER),
                (sub_logic.launch_mode.STUDIO, util.resource.bin_subtype.STUDIO),
            }

    return []
