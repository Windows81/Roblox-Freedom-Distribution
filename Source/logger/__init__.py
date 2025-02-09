from . import filter
import enum

from . import (
    rcc,
    web,
)


class log_context(enum.Enum):
    PYTHON_SETUP = 0
    RCC_SERVER = 1
    WEB_SERVER = 2


# All messages are allowed by default.
DEFAULT_FILTER = filter.filter_type()


def get_message(
    text: bytes | str,
    context: log_context,
    filter: filter.filter_type = DEFAULT_FILTER
) -> str | None:
    if isinstance(text, str):
        text = text.encode('utf-8')
    assert isinstance(text, bytes)

    match context:
        case log_context.RCC_SERVER:
            return rcc.get_message(text, filter)
        case log_context.WEB_SERVER:
            return web.get_message(text, filter)
        case log_context.PYTHON_SETUP:
            return text.decode('utf-8')


def log(
    text: bytes | str,
    context: log_context,
        filter: filter.filter_type
) -> None:
    message = get_message(text, context, filter)
    if message is not None:
        print(f'{message}\n', end='')
