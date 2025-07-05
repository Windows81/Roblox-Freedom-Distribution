import enum


class LogAction(enum.Enum):
    PROCEED = 0
    RESTART = 1
    TERMINATE = 2


def check(line: bytes) -> LogAction:
    if b'Info: WatcherThread Detected hang' in line:
        return LogAction.RESTART
    return LogAction.PROCEED
