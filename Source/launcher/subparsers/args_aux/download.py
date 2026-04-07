# Standard library imports
import argparse
import functools

# Local application imports
import launcher.subparsers._logic as sub_logic
from routines import _logic as logic

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
    subparser.add_argument(
        '--skip_download',
        action='store_true',
        help='Disables auto-download of RFD binaries from the internet.'
    )


@sub_logic.serialise_aux_args(*AUX_MODES)
def _(
    mode: sub_logic.launch_mode,
    args_ns: argparse.Namespace,
    args_list: list[logic.base_entry],
) -> list[logic.base_entry]:

    # Enables the `auto_download` flag for every routine, but adds no new routines of its own.
    auto_download = not args_ns.skip_download

    for a in args_list:
        if not isinstance(a, logic.bin_entry):
            continue
        a.auto_download = auto_download
    return []
