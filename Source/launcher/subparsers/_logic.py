import enum


class launch_mode(enum.Enum):
    STUDIO = 0
    SERVER = 1
    PLAYER = 2


LAUNCH_ROUTINES = {}


def launch_command(launch_mode: launch_mode):
    def inner(f):
        LAUNCH_ROUTINES[launch_mode] = f
        return f
    return inner
