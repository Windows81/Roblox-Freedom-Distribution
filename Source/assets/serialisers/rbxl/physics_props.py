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
    data_len = len(prop_values)
    data_index = 0
    while data_index < data_len:
        val = prop_values[data_index]
        prop_values[data_index] &= 0b01
        match val:
            case 0b00:
                data_index += 1
            case 0b01:
                data_index += 21
            case 0b10:
                data_index += 1
            case 0b11:
                data_index += 21
                data_len -= 4
                del prop_values[data_index:data_index+4]
            case _:
                assert False

    chunk_data.prop_values = bytes(prop_values)

    return chunk_data
