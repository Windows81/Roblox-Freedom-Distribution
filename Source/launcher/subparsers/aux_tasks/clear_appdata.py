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
    args: argparse.Namespace,
    routine: logic.routine,
) -> None:

    if args.keep_cache:
        return
    base_urls = set(
        e.get_base_url()
        for e in routine.entries
        if isinstance(e, logic.bin_entry)
    )
    for base in base_urls:
        obj = clear_appdata.obj_type(base)
        obj.perform()
