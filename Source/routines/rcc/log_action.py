import enum


class LogAction(enum.Enum):
    PROCEED = 0
    RESTART = 1
    TERMINATE = 2
    READY = 3


def check(line: bytes) -> LogAction:
    if b'Info: WatcherThread Detected hang' in line:
        return LogAction.RESTART
    elif line.endswith(b'crashes to Backtrace'):
        return LogAction.RESTART
    elif b'Finished initializing game' in line:
        return LogAction.READY
    return LogAction.PROCEED
