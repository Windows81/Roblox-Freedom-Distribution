from . import _logic


def replace(parser: _logic.rbxl_parser, info: _logic.chunk_info) -> bytes | None:
    '''
    This function removes bytecode from any `rbxm` files.
    '''
    prop_head = _logic.wrap_string(b'Source') + b'\x1D'
    if not info.chunk_data.startswith(prop_head, _logic.INT_SIZE):
        return None

    prop_values_bytes = _logic.get_prop_values_bytes(info)
    assert prop_values_bytes is not None
    return b''.join([
        prop_head,
        _logic.join_prop_strings([b''] * len(prop_values_bytes)),
    ])
