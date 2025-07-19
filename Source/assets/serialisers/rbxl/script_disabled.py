from . import _logic


def replace(parser: _logic.rbxl_parser,  chunk_data: _logic.chunk_data_type) -> bytes | None:
    if not isinstance(chunk_data, _logic.chunk_data_type_prop):
        return None

    if chunk_data.prop_name != b'Enabled':
        return None

    class_iden = chunk_data.class_iden
    if not parser.class_dict[class_iden].class_name.endswith(b'Script'):
        return None

    # Replace the enabled flag with its opposite.
    # XORs booleaned uint8 between 0 and 1.
    chunk_data.prop_values = bytes(
        b ^ 1
        for b in
        chunk_data.prop_values
    )

    return chunk_data.to_bytes()
