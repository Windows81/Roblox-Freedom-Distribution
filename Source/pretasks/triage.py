import urllib.request
import functools
import math
import json

from config_type.types.structs import settings_type
import util.versions
import util.resource
import util.fvars


@functools.cache
def get_bare_defaults(
    version: util.versions.rōblox,
    bin_type: util.resource.bin_subtype,
) -> settings_type:
    url = 'https://github.com/Windows81/Roblox-x64dbg-FFlag-Extractor/raw/651332612610c3484a1785f130c8d057efe02fae/test/'

    match version:
        case util.versions.rōblox.v347:
            url += 'v348-'
        case util.versions.rōblox.v463:
            url += 'v463-'

    match bin_type:
        case util.resource.bin_subtype.PLAYER:
            url += 'player.json'
        case util.resource.bin_subtype.STUDIO:
            url += 'studio.json'
        case util.resource.bin_subtype.SERVER:
            url += 'server.json'

    with urllib.request.urlopen(url) as response:
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


def get_filtered(
    version: util.versions.rōblox,
    bin_type: util.resource.bin_subtype,
    t: settings_type,
) -> settings_type:
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
        'DFFlagDebugCurlOption42',  # This one crashes 2021E Studio.
        'DFFlagTheseAreSomeOfMyBestAttributes',  # This one breaks 2021E if set to `false`
        'DFFlagDebugSimulateHangAtExitMainLoop',
        'DFFlagDebugSimulateHangAtFinishLaunchingGameServer',

        # These make 2021E Studio act weird.
        'FFlagDebugStudioCreateGameWindowReturnsNull',
        'FFlagDebugStudioCreateGameWindowThrows',
        'FFlagDebugStudioFlagState',
        'FFlagDebugStudioForceBootstrapperRedundancyCheck',
        'FFlagDebugStudioForceExternalLogin',

        'FFlagGraphicsGL3UseUBO3',
        'FFlagGraphicsGLDisableTimerQueryAdreno',
        'FFlagGraphicsGLDoNotAllowDesktopGL2',
        'FFlagGraphicsGLHD3000DisableGL3',
        'FFlagGraphicsGLHD3000DisableUBO',
        'FFlagGraphicsGLPerFrameQuery2',
        'FFlagGraphicsGLWindowsShutdownFix',
        'FFlagStudioDisableDoubleAuthenticate',  # This one crashes 2021E Studio upon startup
        'FFlagHumanoidParallelOnStep',
        'FFlagHumanoidParallelRemoveNoPhysics',
        'FFlagHumanoidParallelUseManager',
        'FFlagSimLowerConstraintWidgetMinScale',
        'FFlagWindowsExeLaunchUniversalAppByDefault',
    }
    defaults = get_bare_defaults(version, bin_type)
    r = {}
    for dk, dv in defaults.items():
        if 'FLog' in dk:
            continue
        if dk in BLACKLIST:
            continue
        r[dk] = t.get(dk, dv)
    return r


def load_json(
    version: util.versions.rōblox,
    bin_type: util.resource.bin_subtype,
    path: str,
) -> settings_type:
    '''
    This function is smart enough to recognise if the FFlags are nested within a table with an `applicationSettings` key. This is meant for payloads that were generated from a `/v1/settings/application` endpoint.
    '''
    parts = path.rsplit('.', maxsplit=1)
    if len(parts) > 1:
        (remaining, suffix) = parts
        match suffix:
            case 'inv' | 'invert':
                return get_inverted_flags(load_json(version, bin_type, remaining))
            case _:
                pass

    if path == 'bare':
        return get_filtered(version, bin_type, {})

    if path == 'prod':
        return get_filtered(version, bin_type, util.fvars.DEFAULT_SETTINGS[version])

    r = json.load(open(path))
    r = r.get('applicationSettings', r)
    return get_filtered(version, bin_type, r)


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


def gen_settings_for_triage(
    version: util.versions.rōblox,
    bin_type: util.resource.bin_subtype,
    p1: str, p2: str, alpha: float,
) -> settings_type:
    t1 = load_json(version, bin_type, p1)
    t2 = load_json(version, bin_type, p2)
    return interpolate_diff(t1, t2, alpha)


def get_data_between_triages(
    version: util.versions.rōblox,
    bin_type: util.resource.bin_subtype,
    p1: str, p2: str, alpha1: float, alpha2: float,
) -> settings_type:
    t1 = load_json(version, bin_type, p1)
    t2 = load_json(version, bin_type, p2)
    return get_interpolated_changes_between(t1, t2, alpha1, alpha2)
