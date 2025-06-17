from . import _logic


def pad_enums(enums: list[int], uri_list: list[bytes]) -> list[bytes]:
    return uri_list+[b'']*max(0, len(enums)-len(uri_list))
    # TODO: test which way actually works.
    # placeholder = b''
    # return [
    #     (
    #         placeholder := next(uri_iter)
    #         if e == 0 else
    #         placeholder
    #     )
    #     for e in enums
    # ]


def replace(parser: _logic.rbxl_parser, info: _logic.chunk_info) -> bytes | None:
    '''
    https://github.com/rojo-rbx/rbx-dom/blob/5ee4d9062b2d31d61c07bd81e39b0260c6f91a0e/docs/binary.md#content
    '''
    old_prop_head = _logic.wrap_string(b'ImageContent') + b'\x22'
    new_prop_head = _logic.wrap_string(b'Image') + b'\x01'
    if not info.chunk_data.startswith(old_prop_head, _logic.INT_SIZE):
        return None

    class_id = _logic.get_class_iden(info)
    if class_id is None:
        return None

    prop_data = _logic.get_prop_values_bytes(info)
    if prop_data is None:
        return
    enum_count = parser.class_dict[class_id].instance_count

    # `SourceTypes` objects (just like all enums) are stored as an INTERLEAVED array of big-endian `uint32`s.
    # Why take just a partial segment?  We're taking advantage of the fact that `SourceTypes` never goes above 256.
    # Because integers here are big-endian, we put the least significant bytes at the end.
    enums = list(prop_data[
        enum_count * (_logic.INT_SIZE-1):
        enum_count * (_logic.INT_SIZE)
    ])
    uri_count_pos = enum_count * _logic.INT_SIZE
    uri_count = int.from_bytes(
        prop_data[uri_count_pos:uri_count_pos+_logic.INT_SIZE],
        byteorder='little',
    )

    uri_list = _logic.split_prop_strings(
        prop_data[uri_count_pos+_logic.INT_SIZE:],
        limit=uri_count,
    )
    padded_uri_list = pad_enums(enums, uri_list)

    return b''.join([
        class_id,
        new_prop_head,
        _logic.join_prop_strings(padded_uri_list),
    ])
