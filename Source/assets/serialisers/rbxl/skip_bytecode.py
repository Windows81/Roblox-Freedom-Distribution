from . import _logic

PRINT_SCRIPT = bytes([
    0x02, 0x01, 0x05, 0x70, 0x72, 0x69, 0x6E, 0x74, 0x01, 0x02, 0x00, 0x00, 0x01, 0x06, 0x41, 0x00,
    0x00, 0x00, 0x0C, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x40, 0x04, 0x01, 0x37, 0x13, 0x15, 0x00,
    0x02, 0x01, 0x16, 0x00, 0x01, 0x00, 0x02, 0x03, 0x01, 0x04, 0x00, 0x00, 0x00, 0x40, 0x00, 0x01,
    0x00, 0x01, 0x18, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00,
])


def replace(parser: _logic.rbxl_parser, info: _logic.chunk_info) -> bytes | None:
    '''
    TODO: this function serves the dual purpose of removing any dangerous instances of bytecode in RBXL files whilst also patching `DataModelPatch.rbxm` with a simple routine.
    '''
    old_prop_name = b'\x06\x00\x00\x00Source\x1D'
    if not info.chunk_data.startswith(old_prop_name, _logic.INT_SIZE):
        return None

    base = _logic.INT_SIZE + len(old_prop_name)
    chunk_prefix = info.chunk_data[:base]
    head = b''
    sources = []
    while True:
        head = info.chunk_data[base:base+4]
        l = int.from_bytes(head, 'little')
        if head == b'PROP' or l == 0:
            break
        e1 = base
        e2 = base + 4 + l
        val = info.chunk_data[e1:e2]
        if True:
            sources.append(
                len(PRINT_SCRIPT).to_bytes(4, 'little') +
                PRINT_SCRIPT
            )
        else:
            sources.append(val)
        base += l + 4

    chunk_suffix = info.chunk_data[base:]
    return b''.join([
        chunk_prefix,
        *sources,
        chunk_suffix,
    ])
