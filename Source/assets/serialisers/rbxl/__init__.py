from functools import partial
import enum

from . import (
    _logic,
    fonts,
    script_disabled,
    skip_bytecode,
    strip_unsupported,
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
    strip_unsupported = enum.member(partial(strip_unsupported.replace))
    convert_csg = enum.member(partial(convert_csg.replace))
    image_content = enum.member(partial(image_content.replace))
    physics_props = enum.member(partial(physics_props.replace))


DEFAULT_METHODS = set(method).difference({
    # method.convert_csg,
})


def is_valid(data: bytes) -> bool:
    return data.startswith(_logic.HEADER_SIGNATURE)


def parse(data: bytes, methods: set[method] = DEFAULT_METHODS) -> bytes | None:
    if not is_valid(data):
        return
    parser = _logic.rbxl_parser(data)
    return parser.parse_file([
        m.value
        for m in methods
    ])


def should_parse(data: bytes) -> bool:
    '''
    Since Rōblox v553, all instances saved within a `rbxl` file will contain a `PROP` field `"UniqueId"`.

    This procedure attempts a linear search for the region in the file in which `PROP` fields live, then does another linear search for the `"UniqueId"` field.

    If there ends up being a `"UniqueId"` field, then the `rbxl` file is too new for RFD, and full serialisiation becomes necessary.
    '''
    if not is_valid(data):
        return False

    unique_str = _logic.wrap_string(b'UniqueId')+b'\x1F'
    halfway_point_idx = int(len(data) * 0.40)

    start_search_idx = data.find(b'PROP', halfway_point_idx)
    uniqueid_idx = data.find(unique_str, start_search_idx)
    if uniqueid_idx == -1:
        return False

    if data[uniqueid_idx-0x16:uniqueid_idx-0x12] != b'PROP':
        return False

    return True
