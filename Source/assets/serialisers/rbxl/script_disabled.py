from . import _logic


def replace(parser: _logic.rbxl_parser, info: _logic.chunk_info) -> bytes | None:
    if _logic.get_first_chunk_str(info) != b'Enabled':
        return None

    class_id = _logic.get_class_iden(info)
    if class_id is None:
        return None

    if not parser.class_dict[class_id].class_name.endswith(b'Script'):
        return None

    class_id = info.chunk_data[0:_logic.INT_SIZE]
    old_prop_name = b'\x07\x00\x00\x00Enabled\x02'
    new_prop_name = b'\x08\x00\x00\x00Disabled\x02'
    chunk_values = info.chunk_data[len(class_id + old_prop_name):]

    new_values = bytes(
        b ^ 1  # XORs booleaned uint8 between 0 and 1.
        for b in
        chunk_values
    )

    return b''.join([
        class_id,
        new_prop_name,
        new_values,
    ])
