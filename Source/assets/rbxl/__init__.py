from . import (
    _logic,
    downdate_font,
    script_disabled,
    roblox_links,
)


def parse(data: bytes):
    parser = _logic.rbxl_parser(data)
    return parser.parse_file([
        downdate_font.replace,
        # script_disabled.replace, # Not useful yet; `rbxl` files still store scripts' `Disabled` property internally.
        roblox_links.replace,
    ])
