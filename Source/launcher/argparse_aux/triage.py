from fractions import Fraction
import argparse
import json

from routines import _logic as logic
import launcher._logic as sub_logic
from pretasks import triage
import util.versions
import util.resource


AUX_MODES = (
    sub_logic.launch_mode.LAUNCH_PLAYER,
    sub_logic.launch_mode.LAUNCH_SERVER,
    sub_logic.launch_mode.LAUNCH_STUDIO,
)


def guess_bin_data(
    mode: sub_logic.launch_mode,
    args_list: list[logic.base_entry],
) -> tuple[util.versions.rōblox, util.resource.bin_subtype] | None:
    for a in args_list:
        if not isinstance(a, logic.bin_entry):
            continue
        if not sub_logic.is_primary_bin(mode, a.BIN_SUBTYPE):
            continue
        return (a.retr_version(), a.BIN_SUBTYPE)


@sub_logic.add_aux_args(*AUX_MODES)
def _(
    mode: sub_logic.launch_mode,
    parser: argparse.ArgumentParser,
    subparser: argparse.ArgumentParser,
) -> None:
    subparser.add_argument(
        '--triage_fvars_a',
        type=lambda x: float(Fraction(x)),
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
        '--triage_fvars_a1',
        type=lambda x: float(Fraction(x)),
        help='shows between alphas `--triage_fvars_a1` ...',
    )
    subparser.add_argument(
        '--triage_fvars_a2',
        type=lambda x: float(Fraction(x)),
        help='... and `--triage_fvars_a2` the changed FFlags',
    )


@sub_logic.serialise_aux_args(*AUX_MODES)
def _(
    mode: sub_logic.launch_mode,
    args_ns: argparse.Namespace,
    args_list: list[logic.base_entry],
) -> None:

    bin_data = guess_bin_data(mode, args_list)
    if bin_data is None:
        return

    rōblox_version, bin_type = bin_data

    if (
        args_ns.triage_fvars_a1 is not None and
        args_ns.triage_fvars_a2 is not None
    ):
        diff = triage.get_data_between_triages(
            version=rōblox_version,
            bin_type=bin_type,
            p1=args_ns.triage_fvars_p1,
            p2=args_ns.triage_fvars_p2,
            alpha1=args_ns.triage_fvars_a1,
            alpha2=args_ns.triage_fvars_a2,
        )
        for k, v in diff.items():
            print('%s = %s,' % (k, json.dumps(v)))
        exit()

    if args_ns.triage_fvars_a is None:
        return
    if args_ns.triage_fvars_p1 is None:
        return
    if args_ns.triage_fvars_p2 is None:
        return

    replacement = triage.gen_settings_for_triage(
        version=rōblox_version,
        bin_type=bin_type,
        p1=args_ns.triage_fvars_p1,
        p2=args_ns.triage_fvars_p2,
        alpha=args_ns.triage_fvars_a,
    )

    for a in args_list:
        if not isinstance(a, logic.bin_entry):
            continue
        a.replacement_fvars = replacement
