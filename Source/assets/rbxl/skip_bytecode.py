from . import _logic


def replace(parser: _logic.rbxl_parser, info: _logic.chunk_info) -> bytes | None:
    '''
    Filters out properties with bytecode as the value type.
    Used as a precaution against arbitrary code-execution exploits.
    '''
    type_id = _logic.get_type_id(info)
    if type_id not in {0x1D}:
        return None

    # TODO: test empty `PROP` tags like the one below.
    return b''.join([
        b'PROP',
        b'\x00'*12,
    ])
