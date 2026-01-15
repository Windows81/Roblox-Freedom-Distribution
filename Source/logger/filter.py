# Standard library imports
import dataclasses
import re

# Local application imports
from . import flog_table


@dataclasses.dataclass(frozen=True)
class filter_type_bin:
    flogs: frozenset[int]

    @staticmethod
    def serialise_key(flog: str) -> str:
        return re.sub('^(D?FLog)?', 'FLog', flog)

    @staticmethod
    def parse(*flogs: str) -> "filter_type_bin":
        return filter_type_bin(flogs=frozenset(
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


@dataclasses.dataclass(frozen=True, unsafe_hash=True)
class filter_type_web:
    urls: bool
    errors: bool


def default_message_print(message: str) -> None:
    print(f'{message}\n', end='')


FILTER_WEB_QUIET = filter_type_web(False, False)
FILTER_WEB_LOUD = filter_type_web(True, True)

FILTER_BIN_QUIET = filter_type_bin(frozenset())
FILTER_BIN_LOUD = filter_type_bin(
    flogs=frozenset(range(
        flog_table.INDEX_OFFSET,
        len(flog_table.LOG_LEVEL_LIST) + flog_table.INDEX_OFFSET
    ))
)
