from functools import partial
import enum

from . import (
    _logic,
    fonts,
    script_disabled,
    skip_bytecode,
    roblox_links,
)


class method(enum.Enum):
    # Why `partial`?
    # https://stackoverflow.com/a/58714331/6879778
    fonts = partial(fonts.replace)
    # script_disabled = partial(script_disabled.replace)
    roblox_links = partial(roblox_links.replace)
    skip_bytecode = partial(skip_bytecode.replace)


def check(data: bytes) -> bool:
    return data.startswith(_logic.HEADER_SIGNATURE)


def parse(data: bytes, methods: set[method] = set(method)) -> bytes:
    if not check(data):
        return data
    parser = _logic.rbxl_parser(data)
    return parser.parse_file([
        m.value
        for m in methods
    ])
