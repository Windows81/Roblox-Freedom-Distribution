import argparse
import os
import sys

import util.resource
import util.versions
import util.const
import logger

from routines import player, rcc, studio
from routines import _logic as logic
from pretasks import download

import launcher.subparsers._logic as sub_logic


def prompt_overwrite(rōblox_version: util.versions.rōblox, bin_type: util.resource.bin_subtype) -> bool:
    full_dir = download.get_full_dir(rōblox_version, bin_type)

    rfd_ver_path = os.path.join(full_dir, 'rfd_version')
    if os.path.isfile(rfd_ver_path):
        with open(rfd_ver_path, 'r') as f:
            version_str = f.read()
    else:
        version_str = ''

    if not sys.stdin or not sys.stdin.isatty():
        return False

    if version_str.startswith(util.const.ZIPPED_RELEASE_VERSION):
        return False

    return input('Should RFD overwrite `%s`? (y/N) ' % full_dir).lower().startswith('y')


@sub_logic.add_args(sub_logic.launch_mode.DOWNLOAD)
def _(
    parser: argparse.ArgumentParser,
    subparser: argparse.ArgumentParser,
) -> None:
    subparser.add_argument(
        '--rbx_version', '-v',
        type=util.versions.rōblox.from_name,
        choices=[
            name
            for v in util.versions.rōblox.get_all_versions()
            for name in v.value
        ],
        help='version to download',
        nargs='+', required=True,
    )
    subparser.add_argument(
        '--bin_subtype', '-b',
        type=util.resource.bin_subtype,
        choices=[v.value for v in util.resource.bin_subtype],
        help='directories to download',
        nargs='+', required=True,
    )
    subparser.add_argument(
        '--force_update_bins',
        action='store_true',
        help='forcibly overwrite RFD binaries\' directories if any already exist'
    )
    subparser.add_argument(
        '--skip_existing_bins',
        action='store_true',
        help='skip downloading RFD binaries\' directories if any already exist'
    )


@sub_logic.serialise_args(sub_logic.launch_mode.DOWNLOAD)
def _(
    parser: argparse.ArgumentParser,
    args_ns: argparse.Namespace,
) -> list[logic.base_entry]:

    for bin_type in args_ns.bin_subtype:
        force_overwrite = prompt_overwrite(
            rōblox_version=args_ns.rbx_version,
            bin_type=bin_type,
        )
        download.bootstrap_binary(
            rōblox_version=args_ns.rbx_version,
            bin_type=bin_type,
            force_overwrite=force_overwrite,
            log_filter=logger.PRINT_REASONABLE,
        )
    return []
