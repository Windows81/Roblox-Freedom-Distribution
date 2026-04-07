from typing import Callable
import dataclasses
import enum

from . import bcolors as bc
from . import filter
from . import (
    rcc,
    web,
)


class log_context(enum.Enum):
    PYTHON_SETUP = 0
    RCC_SERVER = 1
    WEB_SERVER = 2


@dataclasses.dataclass(frozen=True, unsafe_hash=True)
class obj_type:
    rcc_logs: filter.filter_type_bin
    player_logs: filter.filter_type_bin
    web_logs: filter.filter_type_web
    other_logs: bool
    bcolors: bc.bcolors = bc.BCOLORS_VISIBLE
    action: Callable[[str], None] = filter.default_message_print

    def log(
        self,
        text: bytes | str,
        context: log_context,
        *a, **kwa,
    ) -> None:
        message = get_message(text, context, self, *a, **kwa)
        if message is None:
            return
        self.action(message)


def get_message(
    text: bytes | str,
    context: log_context,
    filter: obj_type,
    *a, **kwa,
) -> str | None:
    if isinstance(text, str):
        text = text.encode('utf-8')
    assert isinstance(text, bytes)

    match context:
        case log_context.RCC_SERVER:
            return rcc.get_message(filter.rcc_logs, filter.bcolors, text, *a, **kwa)
        case log_context.WEB_SERVER:
            return web.get_message(filter.web_logs, filter.bcolors, text, *a, **kwa)
        case log_context.PYTHON_SETUP:
            return text.decode('utf-8')


def default_message_print(message: str) -> None:
    print(f'{message}\n', end='')


PRINT_QUIET = obj_type(
    rcc_logs=filter.FILTER_BIN_QUIET,
    player_logs=filter.FILTER_BIN_QUIET,
    web_logs=filter.filter_type_web(
        urls=False,
        errors=False,
    ),
    other_logs=False,
    action=default_message_print,
)

PRINT_REASONABLE = obj_type(
    rcc_logs=filter.filter_type_bin.parse(
        "Output",
        "Error",
        "LocalStorage",
        "RCCServiceInit",
        "RCCServiceJobs",
        "RCCExecuteInfo",
        "NetworkAudit",
    ),
    player_logs=filter.filter_type_bin.parse(
        "Output",
        "Error",
        "LocalStorage",
        "GameJoinLoadTime",
    ),
    web_logs=filter.filter_type_web(
        urls=True,
        errors=True,
    ),
    other_logs=True,
    action=default_message_print,
)


PRINT_LOUD = obj_type(
    rcc_logs=filter.FILTER_BIN_LOUD,
    player_logs=filter.FILTER_BIN_LOUD,
    web_logs=filter.filter_type_web(
        urls=True,
        errors=True,
    ),
    other_logs=True,
    action=default_message_print,
)
