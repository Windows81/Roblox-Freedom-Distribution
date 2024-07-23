from . import (
    _logic,
    downdate_font,
    script_disabled,
    skip_bytecode,
    roblox_links,
)


def parse(data: bytes) -> bytes:
    parser = _logic.rbxl_parser(data)
    return parser.parse_file([
        downdate_font.replace,
        # script_disabled.replace, # Not useful yet; `rbxl` files still store scripts' `Disabled` property internally.
        roblox_links.replace,
        skip_bytecode.replace,
    ])


def check(data: bytes) -> bool:
    return data.startswith(_logic.HEADER_SIGNATURE)
