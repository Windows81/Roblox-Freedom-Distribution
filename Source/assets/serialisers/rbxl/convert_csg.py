from . import _logic
from .. import csg


def replace(parser: _logic.rbxl_parser, info: _logic.chunk_info) -> bytes | None:
    old_prop_head = b'\x08\x00\x00\x00MeshData\x01'
    if not info.chunk_data.startswith(old_prop_head, _logic.INT_SIZE):
        return None

    prop_data = _logic.get_prop_values_bytes(info)
    if prop_data is None:
        return

    prop_values = _logic.split_prop_values(prop_data)
    results = [
        csg.parse(data) or data
        for data in prop_values
    ]

    return _logic.join_prop_values(results)
