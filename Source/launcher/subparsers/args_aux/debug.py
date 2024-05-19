import launcher.subparsers._logic as sub_logic
import launcher.routines._logic as logic
import argparse


@sub_logic.add_args(sub_logic.launch_mode.ALWAYS)
def _(
    mode: sub_logic.launch_mode,
    parser: argparse.ArgumentParser,
    subparser: argparse.ArgumentParser,
) -> None:

    if mode == sub_logic.launch_mode.DOWNLOAD:
        return
    subparser.add_argument(
        '--skip_download',
        action='store_true',
        help='Disables auto-download of RFD binaries from the internet. '
    )


@sub_logic.serialise_args(sub_logic.launch_mode.ALWAYS, set())
def _(
    mode: sub_logic.launch_mode,
    args_ns: argparse.Namespace,
    args_list: list[logic.arg_type],
) -> list[logic.arg_type]:

    # Enables the `auto_download` flag for every routine, but adds no new routines of its own.
    auto_download = not args_ns.skip_download
    for a in args_list:
        if not isinstance(a, logic.bin_arg_type):
            continue
        a.auto_download = auto_download
    return []
