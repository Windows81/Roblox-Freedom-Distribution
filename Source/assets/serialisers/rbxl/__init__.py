from functools import partial
import enum

from . import (
    _logic,
    fonts,
    script_disabled,
    skip_bytecode,
    roblox_links,
    image_content,
    convert_csg,
    physics_props,
)


class method(enum.Enum):
    '''
    Why `partial`?  https://stackoverflow.com/a/58714331/6879778
    '''
    repack_fonts = enum.member(partial(fonts.replace))
    script_disabled = enum.member(partial(script_disabled.replace))
    roblox_links = enum.member(partial(roblox_links.replace))
    skip_bytecode = enum.member(partial(skip_bytecode.replace))
    convert_csg = enum.member(partial(convert_csg.replace))
    image_content = enum.member(partial(image_content.replace))
    physics_props = enum.member(partial(physics_props.replace))


DEFAULT_METHODS = set(method).difference({
    method.convert_csg,
})


def check(data: bytes) -> bool:
    return data.startswith(_logic.HEADER_SIGNATURE)


def parse(data: bytes, methods: set[method] = DEFAULT_METHODS) -> bytes | None:
    if not check(data):
        return
    parser = _logic.rbxl_parser(data)
    return parser.parse_file([
        m.value
        for m in methods
    ])
