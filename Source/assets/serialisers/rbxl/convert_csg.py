from . import _logic
from .. import csg


def replace(parser: _logic.rbxl_parser, info: _logic.chunk_info) -> bytes | None:
    prop_name = _logic.get_first_chunk_str(info)
    if prop_name is None or not prop_name.startswith(b'MeshData'):
        return None

    prop_data = _logic.get_prop_values_bytes(info)
    if prop_data is None:
        return

    prop_values = _logic.split_prop_values(prop_data)
    results = [
        csg.parse(data) or data
        for data in prop_values
    ]

    return (
        _logic.get_pre_prop_values_bytes(info) +
        _logic.join_prop_values(results)
    )
