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
        script_disabled.replace,
        roblox_links.replace,
    ])
