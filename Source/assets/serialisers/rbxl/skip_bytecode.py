from . import _logic


def replace(parser: _logic.rbxl_parser, info: _logic.chunk_info) -> bytes | None:
    '''
    This function removes bytecode from any `rbxm` files.
    '''
    prop_head = b'\x06\x00\x00\x00Source\x1D'
    if not info.chunk_data.startswith(prop_head, _logic.INT_SIZE):
        return None

    prop_values_bytes = _logic.get_prop_values_bytes(info)
    assert prop_values_bytes is not None
    return (
        prop_head +
        _logic.join_prop_values([b''] * len(prop_values_bytes))
    )
