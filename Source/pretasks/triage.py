import functools
import math
import urllib.request
import json

from config_type.types.structs import settings_type
import util.versions
import util.fvars


@functools.cache
def get_bare_defaults(version: util.versions.rōblox) -> settings_type:
    URLS = {
        util.versions.rōblox.v347: 'https://github.com/Windows81/Roblox-x64dbg-FFlag-Extractor/raw/651332612610c3484a1785f130c8d057efe02fae/test/v348-player.json',
        util.versions.rōblox.v463: 'https://github.com/Windows81/Roblox-x64dbg-FFlag-Extractor/raw/651332612610c3484a1785f130c8d057efe02fae/test/v463-player.json',
    }
    with urllib.request.urlopen(URLS[version]) as response:
        return {k: v[1] for k, v in json.loads(response.read()).items()}


def get_inverted_flags(t: settings_type) -> settings_type:
    '''
    You may want to invert all boolean FFlag values.
    '''
    r = t.copy()
    for k, v in list(t.items()):
        if isinstance(v, bool):
            r[k] = not v
    return r


def get_filtered(ver: util.versions.rōblox, t: settings_type) -> settings_type:
    BLACKLIST = {
        'FFlagDebugLocalRccServerConnection',
        'DFFlagAnimateScriptWalkRunBlendFix',
        'DFFlagDebugSimulateExceptionAtStartup',
        'DFFlagDebugSimulateExceptionAtShutdown',
        'DFFlagDebugSimulateHangAtStartup',
        'DFFlagDebugSimulateHangAtShutdown',
        'DFFlagDebugStudioAssetProxy',
        'DFFlagReflectionLoggingUsingEphemeral',
        'FFlagCreateAndUpdateDataReplicationCache5',
        'DFFlagCLI120342',
        'FFlagDebugAdornsDisabled',  # This one disables CoreGuis in 2021E.
        'FFlagDebugGraphicsDisableOpenGL',
        'FFlagDebugLocalRccTicketTesting',
    }
    defaults = get_bare_defaults(ver)
    r = {}
    for dk, dv in defaults.items():
        if 'FLog' in dk:
            continue
        if dk in BLACKLIST:
            continue
        r[dk] = t.get(dk, dv)
    return r


def load_json(ver: util.versions.rōblox, path: str) -> settings_type:
    '''
    This function is smart enough to recognise if the FFlags are nested within a table with an `applicationSettings` key. This is meant for payloads that were generated from a `/v1/settings/application` endpoint.
    '''
    parts = path.rsplit('.', maxsplit=1)
    if len(parts) > 1:
        (remaining, suffix) = parts
        match suffix:
            case 'invert':
                return get_inverted_flags(load_json(ver, remaining))
            case _:
                pass

    if path == 'bare':
        return get_filtered(ver, get_bare_defaults(ver))

    if path == 'prod':
        return get_filtered(ver, util.fvars.DEFAULT_SETTINGS[ver])

    r = json.load(open(path))
    r = r.get('applicationSettings', r)
    return get_filtered(ver, r)


def build_diff_map(t1: settings_type, t2: settings_type):
    s1 = set(t1.items())
    s2 = set(t2.items())
    return sorted(list(s2 - s1))


def interpolate_diff(t1: settings_type, t2: settings_type, alpha: float) -> settings_type:
    '''
    Interpolation is carried out via an _alpha_ value.

    - Lower _alpha_ gets you closer to first param.
    - Higher _alpha_ gets you closer to second param.
    '''
    assert 0 <= alpha <= 1
    diffs = build_diff_map(t1, t2)
    index = math.floor(len(diffs) * alpha)
    return t1 | dict(diffs[:index])


def get_interpolated_changes_between(t1: settings_type, t2: settings_type, alpha1: float, alpha2: float) -> settings_type:
    '''
    Note that the result shows the changes that you'd make to go from `t1` to `t2`.

    - **If `t1` is buggy and `t2` is fine**, you can use the change(s) returned by `get_interpolated_changes_between` _as-is_.

    - **If `t1` is fine and `t2` is buggy**, you need to _reverse_ the change(s) returned by `get_interpolated_changes_between`.
    '''
    assert 0 <= alpha1 <= 1
    assert 0 <= alpha2 <= 1
    diffs = build_diff_map(t1, t2)
    index1 = math.floor(len(diffs) * alpha1)
    index2 = math.floor(len(diffs) * alpha2)
    return dict(diffs[index1:index2])


def gen_settings_for_triage(ver: util.versions.rōblox, p1: str, p2: str, alpha: float) -> settings_type:
    t1 = load_json(ver, p1)
    t2 = load_json(ver, p2)
    return interpolate_diff(t1, t2, alpha)


def get_data_between_triages(ver: util.versions.rōblox, p1: str, p2: str, alpha1: float, alpha2: float) -> settings_type:
    t1 = load_json(ver, p1)
    t2 = load_json(ver, p2)
    return get_interpolated_changes_between(t1, t2, alpha1, alpha2)
