from . import _logic


def replace(parser: _logic.rbxl_parser, chunk_data: _logic.chunk_data_type) -> _logic.chunk_data_type | None:
    '''
    This function removes bytecode from any `rbxm` files.
    '''
    if not isinstance(chunk_data, _logic.chunk_data_type_prop):
        return None

    if chunk_data.prop_name != b'Source':
        return None

    if chunk_data.prop_type != 0x1D:
        return None

    chunk_data.prop_values = _logic.join_prop_strings(
        [b''] * len(chunk_data.prop_values)
    )

    return chunk_data
