from . import flog_table
import dataclasses
import re


@dataclasses.dataclass(frozen=True)
class filter_type_rcc:
    flogs: set[int] = dataclasses.field(default_factory=lambda: set(range(
        flog_table.INDEX_OFFSET,
        len(flog_table.LOG_LEVEL_LIST) + flog_table.INDEX_OFFSET
    )))

    @staticmethod
    def serialise_key(flog: str) -> str:
        return re.sub('^(D?FLog)?', 'FLog', flog)

    @staticmethod
    def parse(*flogs: str) -> "filter_type_rcc":
        return filter_type_rcc(flogs=set(
            flog_table.LOG_LEVEL_DICT[filter_type_rcc.serialise_key(flog)]
            for flog in flogs
        ))

    def __contains__(self, item: int) -> bool:
        return item in self.flogs

    def is_empty(self) -> bool:
        return len(self.flogs) == 0


@dataclasses.dataclass(frozen=True)
class filter_type_web:
    urls: bool = False
    errors: bool = False


@dataclasses.dataclass(frozen=True)
class filter_type:
    rcc_logs: filter_type_rcc = filter_type_rcc()
    web_logs: filter_type_web = filter_type_web()
    other_logs: bool = False


FILTER_QUIET = filter_type(
    rcc_logs=filter_type_rcc(),
    web_logs=filter_type_web(
        urls=False,
        errors=False,
    ),
    other_logs=False,
)

FILTER_REASONABLE = filter_type(
    rcc_logs=filter_type_rcc.parse(
        "RCCServiceInit",
        "LocalStorage",
        "RCCServiceJobs",
        "RCCExecuteInfo",
        "Output",
        "NetworkAudit",
        "Error",
    ),
    web_logs=filter_type_web(
        urls=True,
        errors=True,
    ),
    other_logs=True,
)
