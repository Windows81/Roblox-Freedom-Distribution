from . import _logic
from .. import csg


def replace(parser: _logic.rbxl_parser, chunk_data: _logic.chunk_data_type) -> _logic.chunk_data_type | None:
    if isinstance(chunk_data, _logic.chunk_data_type_prop):
        sstr_data = chunk_data
        prop_values = _logic.split_prop_strings(sstr_data, len_offset=-4)
        return

    if isinstance(chunk_data, _logic.chunk_data_type_prop):
        if not chunk_data.prop_name.startswith(b'MeshData'):
            return

        if chunk_data.prop_type == 0x1C:
            return

        chunk_data.prop_values = _logic.join_prop_strings([
            csg.parse(data) or data
            for data in _logic.split_prop_strings(chunk_data.prop_values)
        ])

        return chunk_data
