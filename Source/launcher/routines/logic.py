
import argparse
import enum
import launcher.studio
import launcher.server
import launcher.player
import versions


class LaunchMode(enum.Enum):
    STUDIO = launcher.studio.Studio
    SERVER = launcher.server.Server
    PLAYER = launcher.player.Player


VERSION_ROUTINES = {
    i: {} for i in LaunchMode
}


def min_version(launch_mode: LaunchMode, version_num: int = 0):
    def inner(f):
        mode_arr = VERSION_ROUTINES[launch_mode]
        for v in versions.Version:
            n: int = v.get_number()
            if n < version_num:
                continue
            mode_arr[v] = f
        return f
    return inner
