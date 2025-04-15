# Standard library imports
import dataclasses
import re

# Local application imports
from . import bcolors as bc
from . import flog_table



@dataclasses.dataclass(frozen=True)
class filter_type_bin:
    flogs: set[int]

    @staticmethod
    def serialise_key(flog: str) -> str:
        return re.sub('^(D?FLog)?', 'FLog', flog)

    @staticmethod
    def parse(*flogs: str) -> "filter_type_bin":
        return filter_type_bin(flogs=set(
            flog_table.LOG_LEVEL_DICT[filter_type_bin.serialise_key(flog)]
            for flog in flogs
        ))

    def __contains__(self, item: int) -> bool:
        return item in self.flogs

    def is_empty(self) -> bool:
        return len(self.flogs) == 0

    def get_level_table(self) -> dict[str, int]:
        return {
            i: (v if v in self.flogs else 0)
            for i, v in flog_table.LOG_LEVEL_DICT.items()
        }


FILTER_BIN_QUIET = filter_type_bin(set())
FILTER_BIN_LOUD = filter_type_bin(
    flogs=set(range(
        flog_table.INDEX_OFFSET,
        len(flog_table.LOG_LEVEL_LIST) + flog_table.INDEX_OFFSET
    ))
)


@dataclasses.dataclass(frozen=True)
class filter_type_web:
    urls: bool = False
    errors: bool = False


@dataclasses.dataclass(frozen=True)
class filter_type:
    rcc_logs: filter_type_bin
    player_logs: filter_type_bin
    web_logs: filter_type_web
    other_logs: bool
    bcolors: bc.bcolors = bc.BCOLORS_VISIBLE


FILTER_QUIET = filter_type(
    rcc_logs=FILTER_BIN_QUIET,
    player_logs=FILTER_BIN_QUIET,
    web_logs=filter_type_web(
        urls=False,
        errors=False,
    ),
    other_logs=False,
)

FILTER_REASONABLE = filter_type(
    rcc_logs=filter_type_bin.parse(
        "Output",
        "Error",
        "LocalStorage",
        "RCCServiceInit",
        "RCCServiceJobs",
        "RCCExecuteInfo",
        "NetworkAudit",
    ),
    player_logs=filter_type_bin.parse(
        "Output",
        "Error",
        "LocalStorage",
        "GameJoinLoadTime",
    ),
    web_logs=filter_type_web(
        urls=True,
        errors=True,
    ),
    other_logs=True,
)


FILTER_LOUD = filter_type(
    rcc_logs=FILTER_BIN_LOUD,
    player_logs=FILTER_BIN_LOUD,
    web_logs=filter_type_web(
        urls=True,
        errors=True,
    ),
    other_logs=True,
)
