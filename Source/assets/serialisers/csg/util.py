from typing import Any, Never
import collections.abc
import functools


OBFUSCATION_NOISE_CYCLE_XOR = bytes([
    0x56, 0x2e, 0x6e, 0x58, 0x31, 0x20, 0x30, 0x04,
    0x34, 0x69, 0x0c, 0x77, 0x0c, 0x01, 0x5e, 0x00,
    0x1a, 0x60, 0x37, 0x69, 0x1d, 0x52, 0x2b, 0x07,
    0x4f, 0x24, 0x59, 0x65, 0x53, 0x04, 0x7a,
])

LCM_A = 0b0000_0011_0100_0011_1111_1101
LCM_C = 0b0010_0110_1001_1110_1100_0011

INT_SIZE = 4


def lcm_rand() -> collections.abc.Generator[int, Any, Never]:
    s = 0b0000_0000_0000_0101_0011_1001  # 1337
    while True:
        s = s * LCM_A + LCM_C
        yield (s >> 16) & 0x7FFF


@functools.cache
def xor_encrypt(code: bytes, offset: int = 0, key=OBFUSCATION_NOISE_CYCLE_XOR) -> bytes:
    l = len(key)
    return bytes(
        c ^ key[i % l]
        for i, c in enumerate(code, offset)
    )
