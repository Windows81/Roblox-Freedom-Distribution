import hashlib
import collections.abc
from typing import Any, Never
OBFUSCATION_NOISE_CYCLE_XOR = bytes([
    86, 46, 110, 88, 49, 32, 48, 4, 52, 105, 12, 119, 12, 1, 94, 0, 26, 96, 55, 105, 29, 82, 43, 7, 79, 36, 89, 101, 83, 4, 122,
])

LCM_A = 0b0000_0011_0100_0011_1111_1101
LCM_C = 0b0010_0110_1001_1110_1100_0011


def lcm_rand() -> collections.abc.Generator[int, Any, Never]:
    s = 0b0000_0000_0000_0101_0011_1001  # 1337
    while True:
        s = s * LCM_A + LCM_C
        yield (s >> 16) & 0x7FFF


saltSize: int = 0x10
hashSize: int = 0x10


def createHash(data: bytes, saltIn: bytes = b'rfd') -> str:
    verticesSize: int = 0  # vertices.size() * sizeof(CSGVertex);
    indicesSize: int = 0  # indices.size() * sizeof(unsigned int);
    buffSize: int = verticesSize + indicesSize + saltSize

    salt = saltIn.rjust(16)
    byteBuffer = list(data+salt)

    # size_t copyOffset = 0;
    # memcpy(&byteBuffer[copyOffset], &vertices[0], verticesSize);

    # copyOffset += verticesSize;
    # memcpy(&byteBuffer[copyOffset], &indices[0], indicesSize);

    # copyOffset += indicesSize;
    # memcpy(&byteBuffer[copyOffset], salt.c_str(), salt.size());

    randGen = lcm_rand()
    for i in range(buffSize):
        j = next(randGen) % buffSize
        byteBuffer[i], byteBuffer[j] = byteBuffer[j], byteBuffer[i]

    hashlib.md5(bytes(byteBuffer))
    # boost::scoped_ptr<RBX::MD5Hasher> hasher(RBX::MD5Hasher::create());
    # hasher->addData((const char*)&byteBuffer[0], byteBuffer.size());

    # memcpy(&hash[0], hasher->toString().c_str(), hashSize);
    # memcpy(&hash[hashSize], salt.c_str(), saltSize);

    # std::string hashStr(&hash[0], hashSize + saltSize);

    return hashStr


def xor_encrypt(code: bytes, key=OBFUSCATION_NOISE_CYCLE_XOR) -> bytes:
    l = len(key)
    return bytes(
        c ^ key[i % l]
        for i, c in enumerate(code)
    )


def get_header(prefix: bytes, version: int) -> bytes:
    return xor_encrypt(
        prefix + version.to_bytes(length=4, byteorder='little')
    )


HEADER_CSG2 = get_header(b"CSGMDL", 2)
HEADER_CSG4 = get_header(b"CSGMDL", 4)
HEADER_CSG5 = get_header(b"CSGMDL", 5)


def parse(data: bytes) -> bytes | None:
    if not data.startswith(HEADER_CSG4):
        return
    return (
        HEADER_CSG2 +
        data[len(HEADER_CSG4):]
    )
