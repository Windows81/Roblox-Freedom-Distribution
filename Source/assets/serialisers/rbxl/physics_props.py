from . import _logic


def replace(parser: _logic.rbxl_parser, chunk_data: _logic.chunk_data_type) -> _logic.chunk_data_type | None:
    '''
    Removes support for the `AcousticAbsorption` field in `PhysicalProperties` data types.
    https://github.com/rojo-rbx/rbx-dom/commit/668bf8b36e3560655b8fa425e75571d8e5d838b7
    '''
    if not isinstance(chunk_data, _logic.chunk_data_type_prop):
        return None

    if chunk_data.prop_type != 0x19:
        return None

    prop_values = list(chunk_data.prop_values)
    l = len(prop_values)
    i = 0
    while i < l:
        val = prop_values[i]
        prop_values[i] &= 0x01
        match val & 0x04:
            case 0x00 | 0x02:
                i += 1
            case 0x01:
                i += 21
            case 0x03:
                i += 21
                prop_values[i:i+_logic.INT_SIZE] = []
            case _:
                assert False

    chunk_data.prop_values = bytes(prop_values)

    return chunk_data
