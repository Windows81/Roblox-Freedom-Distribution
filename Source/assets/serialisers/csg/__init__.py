from .util import lcm_rand, xor_encrypt, INT_SIZE
from . import csgmdl5

from io import BytesIO
import functools
import hashlib
import struct


def create_hash(vertices: bytes, indices: bytes, salt_in: bytes = b'') -> bytearray:
    salt = salt_in.rjust(16)

    byte_buffer = bytearray()
    byte_buffer.extend(vertices)
    byte_buffer.extend(indices)
    byte_buffer.extend(salt)

    rand_gen = lcm_rand()
    for i in range(len(byte_buffer)):
        j = next(rand_gen) % len(byte_buffer)
        byte_buffer[i], byte_buffer[j] = byte_buffer[j], byte_buffer[i]

    hasher = hashlib.md5()
    hasher.update(byte_buffer)
    hash_digest = hasher.digest()

    hash_buffer = bytearray()
    hash_buffer.extend(hash_digest)
    hash_buffer.extend(salt)

    return hash_buffer


def recalculate_hash(data: bytes) -> bytes:
    header_tag = b'CSGMDL'
    version_size = INT_SIZE
    hash_size = 16
    salt_size = 16
    num_vertices_size = INT_SIZE
    vertex_stride = (
        + 12
        + 12
        + 8
        + 4
    )
    num_indices_size = 4

    # Create a BytesIO buffer from the binary string
    buffer = BytesIO(xor_encrypt(data))

    # Check header tag
    if buffer.read(len(header_tag)) != header_tag:
        raise ValueError("Invalid header tag")

    # Read version number
    version = struct.unpack('<I', buffer.read(version_size))[0]

    # Read hash
    hash_pos = buffer.tell()
    old_hash = buffer.read(hash_size)

    # Read salt
    salt_in = buffer.read(salt_size)

    # Read number of vertices
    num_vertices = struct.unpack('<I', buffer.read(num_vertices_size))[0]

    # Read vertices
    vertices = buffer.read(vertex_stride * num_vertices)

    # Read number of indices
    num_indices = struct.unpack('<I', buffer.read(num_indices_size))[0]

    # Read indices
    indices = buffer.read(INT_SIZE * num_indices)

    # Overwrite hash
    buffer.seek(hash_pos)
    buffer.write(create_hash(vertices, indices, salt_in))

    return xor_encrypt(buffer.getvalue())


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


def splice_without_middle_elements(data: bytes, fr: int, ln: int) -> bytes:
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

    if data.startswith(HEADER_CSG5):
        model = csgmdl5.parse(data)

    if data.startswith(HEADER_CSGPHYS5):
        '''
        CSGPHYS5 is identical in data format to CSGPHYS3.
        https://github.com/krakow10/rbx_mesh/blob/d10bcdf727dd9c2504560189a5cb106aa9107ec5/src/physics_data.rs#L71
        '''
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
        return splice_without_middle_elements(
            replace_header_version(data, HEADER_CSGPHYS6, 6, 3),
            len(HEADER_CSGPHYS6), 40,
        )

    if data.startswith(HEADER_CSGPHYS7):
        '''
        Why 41 bytes in CSGPHYS7?
        +40: `PhysicsInfo`, as per above.
        + 1: the mysterious magic number `03` (one byte) that takes place after the versioned header.
        https://github.com/krakow10/rbx_mesh/blob/d10bcdf727dd9c2504560189a5cb106aa9107ec5/src/physics_data.rs#L54
        '''
        return splice_without_middle_elements(
            replace_header_version(data, HEADER_CSGPHYS7, 7, 3),
            len(HEADER_CSGPHYS7), 41,
        )
