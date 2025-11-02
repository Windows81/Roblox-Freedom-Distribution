import functools
import hashlib
import collections.abc
from typing import Any, Never
OBFUSCATION_NOISE_CYCLE_XOR = bytes([
    86, 46, 110, 88, 49, 32, 48, 4, 52, 105, 12, 119, 12, 1, 94, 0, 26, 96, 55, 105, 29, 82, 43, 7, 79, 36, 89, 101, 83, 4, 122,
])

INT_SIZE = 4

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
    '''
    TODO: decide whether we should `jmp` this function in the EXEs or to actually use `createHash` and have the client validate the hash.
    '''
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


@functools.cache
def xor_encrypt(code: bytes, key=OBFUSCATION_NOISE_CYCLE_XOR, offset: int = 0) -> bytes:
    l = len(key)
    return bytes(
        c ^ key[i % l]
        for i, c in enumerate(code, offset)
    )


@functools.cache
def get_header(prefix: bytes, version: int) -> bytes:
    return prefix + version.to_bytes(length=INT_SIZE, byteorder='little')


def replace_header_version(data: bytes, versioned_header: bytes, from_version: int, to_version: int) -> bytes:
    '''
    The redundant `from_version` argument is used here to account for the possibility of the data being XOR-encrypted.
    '''
    version_loc = len(versioned_header) - INT_SIZE
    old_version = int.from_bytes(
        data[version_loc:version_loc+INT_SIZE],
        byteorder='little',
    )
    new_version = old_version ^ (from_version ^ to_version)

    return b''.join([
        data[:version_loc],
        new_version.to_bytes(length=INT_SIZE, byteorder='little'),
        data[version_loc+INT_SIZE:],
    ])


def splice(data: bytes, fr: int, ln: int) -> bytes:
    return b''.join([
        data[:fr],
        data[fr+ln:],
    ])


HEADER_CSG2 = xor_encrypt(get_header(b'CSGMDL', 2))
HEADER_CSG4 = xor_encrypt(get_header(b'CSGMDL', 4))
HEADER_CSG5 = xor_encrypt(get_header(b'CSGMDL', 5))
HEADER_CSGPHYS5 = get_header(b'CSGPHS', 5)
HEADER_CSGPHYS6 = get_header(b'CSGPHS', 6)
HEADER_CSGPHYS7 = get_header(b'CSGPHS', 7)


def parse(data: bytes) -> bytes | None:
    if data.startswith(HEADER_CSG4):
        return replace_header_version(data, HEADER_CSG4, 4, 2)

    if data.startswith(HEADER_CSGPHYS5):
        return replace_header_version(data, HEADER_CSGPHYS5, 5, 3)

    if data.startswith(HEADER_CSGPHYS6):
        '''
        Why 40 bytes?
        ```rs
        #[binrw::binrw]
        #[brw(little)]
        #[derive(Debug,Clone)]
        pub struct PhysicsInfo{
            pub volume:f32,
            pub center_of_gravity:[f32;3],
            // upper triangular matrix read left to right top to bottom
            pub moment_of_inertia_packed:[f32;6],
        }
        ```
        CSGPHYS6 and CSGPHYS7 both contain `PhysicsInfo` structs, which as above indicate a length of 40 bytes.
        https://github.com/krakow10/rbx_mesh/blob/d10bcdf727dd9c2504560189a5cb106aa9107ec5/src/physics_data.rs#L8-L16
        '''
        return splice(
            replace_header_version(data, HEADER_CSGPHYS6, 6, 3),
            len(HEADER_CSGPHYS6), 40,
        )

    if data.startswith(HEADER_CSGPHYS7):
        '''
        Why 41 bytes?
        +40: `PhysicsInfo`, as per above.
        + 1: the mysterious magic number `03` (one byte) that takes place after the versioned header.
        https://github.com/krakow10/rbx_mesh/blob/d10bcdf727dd9c2504560189a5cb106aa9107ec5/src/physics_data.rs#L54
        '''
        return splice(
            replace_header_version(data, HEADER_CSGPHYS7, 7, 3),
            len(HEADER_CSGPHYS7), 41,
        )

    return data
