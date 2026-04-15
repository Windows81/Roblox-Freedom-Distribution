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
def xor_encrypt(code: bytes, offset: int = 0, key: bytes = OBFUSCATION_NOISE_CYCLE_XOR) -> bytes:
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


def recalculate_hash(data: bytes) -> bytes:
    data_xor = xor_encrypt(data)

    hash_base = 0x0a
    hash_size = 0x20

    hash_salt_base = hash_base+0x10
    hash_salt_size = 0x10
    hash_salt = data_xor[
        hash_salt_base:
        hash_salt_base+hash_salt_size
    ]

    vertex_count_base = hash_base + hash_size
    vertex_count_size = INT_SIZE
    vertex_count = int.from_bytes(
        bytes=data_xor[
            vertex_count_base:
            vertex_count_base + vertex_count_size
        ],
        byteorder='little',
    )

    vertex_stride_size_base = vertex_count_base + vertex_count_size
    vertex_stride_size_size = INT_SIZE
    vertex_stride_size = int.from_bytes(
        bytes=data_xor[
            vertex_stride_size_base:
            vertex_stride_size_base + vertex_stride_size_size
        ],
        byteorder='little',
    )
    assert vertex_stride_size == 84

    vertex_data_base = vertex_stride_size_base + vertex_stride_size_size
    vertex_data_size = vertex_count * vertex_stride_size
    vertex_data = data_xor[
        vertex_data_base:
        vertex_data_base + vertex_data_size
    ]

    index_count_base = vertex_data_base + vertex_data_size
    index_count_size = INT_SIZE
    index_count = int.from_bytes(
        bytes=data_xor[
            index_count_base:
            index_count_base + index_count_size
        ],
        byteorder='little',
    )

    index_data_base = index_count_base + index_count_size
    index_data_size = index_count * INT_SIZE
    index_data = data_xor[
        index_data_base:
        index_data_base + index_data_size
    ]

    new_hash = create_hash(
        vertices=vertex_data,
        indices=index_data,
        salt=hash_salt,
    )

    result = b''.join([
        data[:hash_base],
        xor_encrypt(new_hash, offset=hash_base),
        data[hash_base+hash_size:],
    ])
    return result


class CSG_HEADER(enum.Enum):
    MDL2 = xor_encrypt(get_header(b'CSGMDL', 2))
    MDL4 = xor_encrypt(get_header(b'CSGMDL', 4))
    MDL5 = xor_encrypt(get_header(b'CSGMDL', 5))
    PHS5 = get_header(b'CSGPHS', 5)
    PHS6 = get_header(b'CSGPHS', 6)
    PHS7 = get_header(b'CSGPHS', 7)
    PHS8 = get_header(b'CSGPHS', 8)
