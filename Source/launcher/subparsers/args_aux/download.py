# Standard library imports
import argparse
import functools

# Local application imports
from routines import _logic as logic
import launcher.subparsers._logic as sub_logic


DOWNLOADABLE_ARG_SUPERTYPE = logic.bin_entry


@functools.cache
def check_mode(mode: sub_logic.launch_mode) -> bool:
    return DOWNLOADABLE_ARG_SUPERTYPE in sub_logic.SERIALISE_TYPE_SETS[mode]


@sub_logic.add_args(sub_logic.launch_mode.ALWAYS)
def _(
    mode: sub_logic.launch_mode,
    parser: argparse.ArgumentParser,
    subparser: argparse.ArgumentParser,
) -> None:
    if not check_mode(mode):
        return

    subparser.add_argument(
        '--skip_download',
        action='store_true',
        help='Disables auto-download of RFD binaries from the internet.'
    )


@sub_logic.serialise_args(sub_logic.launch_mode.ALWAYS, set())
def _(
    mode: sub_logic.launch_mode,
    args_ns: argparse.Namespace,
    args_list: list[logic.obj_type],
) -> list[logic.obj_type]:
    if not check_mode(mode):
        return []

    # Enables the `auto_download` flag for every routine, but adds no new routines of its own.
    auto_download = not args_ns.skip_download
    for a in args_list:
        if not isinstance(a, DOWNLOADABLE_ARG_SUPERTYPE):
            continue
        a.auto_download = auto_download
    return []
