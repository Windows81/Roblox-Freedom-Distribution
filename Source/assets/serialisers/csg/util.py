from typing import Any, Never
import collections.abc
import functools
import hashlib
import enum


OBFUSCATION_NOISE_CYCLE_XOR = bytes([
    0x56, 0x2e, 0x6e, 0x58, 0x31, 0x20, 0x30, 0x04,
    0x34, 0x69, 0x0c, 0x77, 0x0c, 0x01, 0x5e, 0x00,
    0x1a, 0x60, 0x37, 0x69, 0x1d, 0x52, 0x2b, 0x07,
    0x4f, 0x24, 0x59, 0x65, 0x53, 0x04, 0x7a,
])

INT_SIZE = 4


def lcm_rand() -> collections.abc.Generator[int, Any, Never]:
    s = 0b0000_0000_0000_0101_0011_1001  # 1337.
    while True:

        # Doing a bitmask cast to u32 speeds things up.
        s &= 0b11111111_11111111_11111111_11111111

        s *= 0b00000000_00000011_01000011_11111101  # 0214013.
        s += 0b00000000_00100110_10011110_11000011  # 2531011.

        yield (s >> 16) & 0b0111_1111_1111_1111


@functools.cache
def xor_encrypt(code: bytes, offset: int = 0, key=OBFUSCATION_NOISE_CYCLE_XOR) -> bytes:
    l = len(key)
    return bytes(
        c ^ key[i % l]
        for i, c in enumerate(code, offset)
    )


@functools.cache
def get_header(prefix: bytes, version: int) -> bytes:
    return prefix + version.to_bytes(length=INT_SIZE, byteorder='little')


def create_hash(vertices: bytes, indices: bytes, salt: bytes = b'\0'*16) -> bytes:
    assert len(salt) == 16

    byte_buffer = bytearray(b''.join([
        vertices,
        indices,
        salt,
    ]))

    # Deterministicly swaps random bytes.
    buffer_size = len(byte_buffer)
    rand_gen = lcm_rand()
    for i in range(buffer_size):
        j = next(rand_gen) % buffer_size
        byte_buffer[i], byte_buffer[j] = byte_buffer[j], byte_buffer[i]

    hasher = hashlib.md5()
    hasher.update(byte_buffer)
    hash_digest = hasher.hexdigest()[:16].encode()

    # Combines half of the hash's *hex* digest with the unencrypted `salt`.
    hash_buffer = b''.join([
        hash_digest,
        salt,
    ])

    return hash_buffer


class CSG_HEADER(enum.Enum):
    MDL2 = xor_encrypt(get_header(b'CSGMDL', 2))
    MDL4 = xor_encrypt(get_header(b'CSGMDL', 4))
    MDL5 = xor_encrypt(get_header(b'CSGMDL', 5))
    PHS5 = get_header(b'CSGPHS', 5)
    PHS6 = get_header(b'CSGPHS', 6)
    PHS7 = get_header(b'CSGPHS', 7)
    PHS8 = get_header(b'CSGPHS', 8)
