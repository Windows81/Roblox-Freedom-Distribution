import launcher.aux_tasks.download as download
import launcher.subparsers._logic as sub_logic
import launcher.routines._logic as logic
import argparse


@sub_logic.add_args(sub_logic.launch_mode.ALWAYS)
def _(
    mode: sub_logic.launch_mode,
    parser: argparse.ArgumentParser,
    subparser: argparse.ArgumentParser,
) -> None:

    subparser.add_argument(
        '--skip_download',
        action='store_true',
    )


@sub_logic.serialise_args(sub_logic.launch_mode.ALWAYS)
def _(
    mode: sub_logic.launch_mode,
    args_ns: argparse.Namespace,
    args_list: list[logic.arg_type],
) -> None:

    auto_download = not args_ns.skip_download
    for a in args_list:
        if not isinstance(a, logic.bin_arg_type):
            continue
        a.auto_download = auto_download
