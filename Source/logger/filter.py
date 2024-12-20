from . import flog_table
import dataclasses
import re


@dataclasses.dataclass(frozen=True)
class filter_type_rcc:
    types: set[int] = dataclasses.field(default_factory=lambda: set(range(
        flog_table.INDEX_OFFSET,
        len(flog_table.LOG_LEVEL_LIST) + flog_table.INDEX_OFFSET
    )))

    @staticmethod
    def serialise_key(flog: str) -> str:
        return re.sub('^(D?FLog)?', 'FLog', flog)

    @staticmethod
    def parse(*flogs: str) -> "filter_type_rcc":
        return filter_type_rcc(set(
            flog_table.LOG_LEVEL_DICT[filter_type_rcc.serialise_key(flog)]
            for flog in flogs
        ))

    def __contains__(self, item: int) -> bool:
        return item in self.types

    def is_empty(self) -> bool:
        return len(self.types) == 0


@dataclasses.dataclass(frozen=True)
class filter_type:
    rcc_logs: filter_type_rcc = filter_type_rcc()
    other_logs: bool = False
