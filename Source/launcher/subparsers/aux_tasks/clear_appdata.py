import launcher.aux_tasks.clear_appdata as clear_appdata
import launcher.subparsers._logic as sub_logic
import launcher.routines._logic as logic
import argparse


@sub_logic.add_args(sub_logic.launch_mode.ALWAYS)
def _(
    mode: sub_logic.launch_mode,
    parser: argparse.ArgumentParser,
    sub_parser: argparse.ArgumentParser,
) -> None:

    sub_parser.add_argument(
        '--keep_cache',
        action='store_true',
    )


@sub_logic.serialise_args(sub_logic.launch_mode.ALWAYS)
def _(
    mode: sub_logic.launch_mode,
    parser: argparse.ArgumentParser,
    args_ns: argparse.Namespace,
    args_list: list[logic.arg_type],
) -> None:

    if args_ns.keep_cache:
        return
    base_urls = set(
        a.get_base_url()
        for a in args_list
        if isinstance(a, logic.bin_arg_type)
    )
    for base in base_urls:
        obj = clear_appdata.obj_type(base)
        obj.initialise()
