import launcher.routines.player as player
import launcher.routines.server as server
import launcher.routines.studio as studio

import launcher.routines.logic as logic
import util.versions as versions
import typing
import enum


class launch_mode(enum.Enum):
    STUDIO = 0
    SERVER = 1
    PLAYER = 2


VERSION_ROUTINES = {
    i: versions.version_holder[typing.Callable]() for i in launch_mode
}


def launch_command(launch_mode: launch_mode, min_version: int = 0):
    def inner(f):
        VERSION_ROUTINES[launch_mode].add_min(f, min_version)
        return f
    return inner
