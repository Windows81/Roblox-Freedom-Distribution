import argparse
import json

from config_type.types.structs import settings_type
from routines import _logic as logic
import launcher._logic as sub_logic
from pretasks import triage
import util.versions


AUX_MODES = (
    sub_logic.launch_mode.LAUNCH_PLAYER,
    sub_logic.launch_mode.LAUNCH_SERVER,
    sub_logic.launch_mode.LAUNCH_STUDIO,
)


def guess_version(
    mode: sub_logic.launch_mode,
    args_list: list[logic.base_entry],
) -> util.versions.rōblox | None:
    for a in args_list:
        if not isinstance(a, logic.bin_entry):
            continue
        if not sub_logic.is_primary_bin(mode, a.BIN_SUBTYPE):
            continue
        return a.retr_version()


@sub_logic.add_aux_args(*AUX_MODES)
def _(
    mode: sub_logic.launch_mode,
    parser: argparse.ArgumentParser,
    subparser: argparse.ArgumentParser,
) -> None:
    subparser.add_argument(
        '--triage_fvars_set',
        type=float,
        help='alpha value for testing FFlags, et c.; this clears `ClientAppSettings.json` when you quit RFD',
    )
    subparser.add_argument(
        '--triage_fvars_p1',
        help='file identifier for the first table',
    )
    subparser.add_argument(
        '--triage_fvars_p2',
        help='file identifier for the second table',
    )
    subparser.add_argument(
        '--triage_fvars_set1',
        type=float,
        help='shows between alphas `--triage_fvars_set1` ...',
    )
    subparser.add_argument(
        '--triage_fvars_set2',
        type=float,
        help='... and `--triage_fvars_set2` the changed FFlags',
    )


@sub_logic.serialise_aux_args(*AUX_MODES)
def _(
    mode: sub_logic.launch_mode,
    args_ns: argparse.Namespace,
    args_list: list[logic.base_entry],
) -> None:

    rōblox_version = guess_version(mode, args_list)
    if rōblox_version is None:
        return

    if (
        args_ns.triage_fvars_set1 is not None and
        args_ns.triage_fvars_set2 is not None
    ):
        diff = triage.get_data_between_triages(
            ver=rōblox_version,
            p1=args_ns.triage_fvars_p1,
            p2=args_ns.triage_fvars_p2,
            alpha1=args_ns.triage_fvars_set1,
            alpha2=args_ns.triage_fvars_set2,
        )
        for k, v in diff.items():
            print('%s = %s,' % (k, json.dumps(v)))
        exit()

    if args_ns.triage_fvars_set is None:
        return
    if args_ns.triage_fvars_p1 is None:
        return
    if args_ns.triage_fvars_p2 is None:
        return

    replacement = triage.gen_settings_for_triage(
        ver=rōblox_version,
        p1=args_ns.triage_fvars_p1,
        p2=args_ns.triage_fvars_p2,
        alpha=args_ns.triage_fvars_set,
    )

    for a in args_list:
        if not isinstance(a, logic.bin_entry):
            continue
        a.replacement_fvars = replacement
