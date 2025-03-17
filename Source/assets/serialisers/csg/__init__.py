OBFUSCATION_NOISE_CYCLE_XOR = bytes([
    86, 46, 110, 88, 49, 32, 48, 4, 52, 105, 12, 119, 12, 1, 94, 0, 26, 96, 55, 105, 29, 82, 43, 7, 79, 36, 89, 101, 83, 4, 122,
])


def xor_encrypt(code: bytes, key=OBFUSCATION_NOISE_CYCLE_XOR) -> bytes:
    l = len(key)
    return bytes(
        c ^ key[i % l]
        for i, c in enumerate(code)
    )


HEADER_CSG2 = xor_encrypt(
    b"CSGMDL" + (2).to_bytes(length=4, byteorder='little')
)
HEADER_CSG4 = xor_encrypt(
    b"CSGMDL" + (4).to_bytes(length=4, byteorder='little')
)


def parse(data: bytes) -> bytes | None:
    if not data.startswith(HEADER_CSG4):
        return
    return (
        HEADER_CSG2 +
        data[len(HEADER_CSG4):]
    )
