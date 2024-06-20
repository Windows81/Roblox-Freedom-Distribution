import launcher.routines.clear_appdata as clear_appdata
import launcher.subparsers._logic as sub_logic
from ...routines import _logic as logic
import argparse

CACHEABLE_ARG_SUPERTYPE = logic.bin_arg_type


@sub_logic.add_args(sub_logic.launch_mode.ALWAYS)
def _(
    mode: sub_logic.launch_mode,
    parser: argparse.ArgumentParser,
    sub_parser: argparse.ArgumentParser,
) -> None:
    if CACHEABLE_ARG_SUPERTYPE not in sub_logic.SERIALISE_TYPE_SETS[mode]:
        return

    sub_parser.add_argument(
        '--keep_cache',
        action='store_true',
        help='Skips deleting host-specific cached content from the %%LocalAppData%%\\Temp\\Roblox\\http directory.',
    )


@sub_logic.serialise_args(sub_logic.launch_mode.ALWAYS, {clear_appdata.arg_type})
def _(
    mode: sub_logic.launch_mode,
    args_ns: argparse.Namespace,
    args_list: list[logic.arg_type],
) -> list[logic.arg_type]:

    if args_ns.keep_cache:
        return []
    base_args = [
        a
        for a in args_list
        if isinstance(a, logic.host_arg_type)
    ]

    if base_args == None:
        return []

    args_list[:0] = [
        clear_appdata.arg_type(
            rcc_host=base.rcc_host,
            rcc_port_num=base.rcc_port_num,
            web_host=base.web_host,
            web_port=base.web_port,
        )
        for base in base_args
    ]

    return []
