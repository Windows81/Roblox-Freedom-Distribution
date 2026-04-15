'''
This module could not have existed without help from the following codebases:
https://github.com/krakow10/rbx_mesh/blob/master/src/mesh_data.rs#L454
https://github.com/Artifaqt/ROBLOX2016/blob/e0cfac59fea3a5b986843e65b0fda286e439f9fc/App/include/v8datamodel/CSGMesh.h#L92
https://github.com/krakow10/rbx_mesh/blob/master/src/mesh_data.rs#L242
'''

from .util import xor_encrypt, create_hash, CSG_HEADER
import itertools
import struct
import io


def wrap_number(x: float, min_val: float, max_val: float) -> float:
    range_val = max_val - min_val
    wrapped = (x - min_val) % range_val
    if wrapped < 0:
        wrapped += range_val
    return wrapped + min_val


def quantize(x: float, max_val=0x7f) -> float:
    return wrap_number(
        x - max_val,
        -max_val - 1,
        +max_val + 1,
    ) / max_val


def read_state_machine(data: list[int], count: int) -> list[int]:
    index = 0
    indices = []

    for _ in range(count):
        value = data.pop(0)
        flag7 = value & 0b1000_0000 > 0
        flag6 = value & 0b0100_0000 > 0

        if flag7:
            add_lo = data.pop(0)
            add_hi = data.pop(0)
            index += add_lo << 0x08
            index += add_hi << 0x10
            index += value & 0b0111_1111

        elif flag6:
            index += (value & 0b0011_1111) - 0x40
        else:
            index += value

        indices.append(index & 0b0111_1111_1111_1111_1111_1111)

    return indices


def trim_indices(indices: list[int], range_markers: list[int]) -> list[int]:
    '''
    Return subrange(s) of indices return based on the range markers.
    '''
    marker0 = range_markers[0]
    if marker0 != 0:
        # Drops indices at the start of the list.
        indices = indices[marker0:]
    marker1 = range_markers[1]
    if len(range_markers) < 3:
        return indices

    # Splits indices according to marker points.
    difference = marker1 - marker0
    indices = indices[:difference]

    '''
    _unknown = []
    remaining_indices = indices[difference:]
    for i in range(2, len(range_markers)):
        difference = range_markers[i] - range_markers[i-1]
        next_remaining_indices = remaining_indices[difference:]
        _unknown.append(remaining_indices[:difference])
        remaining_indices = next_remaining_indices

    # Inserts the final range.
    if difference < len(remaining_indices):
        # Drops indices at the end of the list.
        remaining_indices = remaining_indices[:difference]
    _unknown.append(remaining_indices)
    '''

    return indices


def read_chunks_vector3(stream: io.BytesIO) -> list[bytes]:
    # Reads an unsigned short (2 bytes).
    count = struct.unpack('<H', stream.read(2))[0]

    # Reads an unsigned int (4 bytes).
    data_len = struct.unpack('<I', stream.read(4))[0]

    result = list[bytes]()
    for _ in range(count):
        result.append(struct.pack(
            # Packs three floats into a 12 byte string.
            'fff',

            # Quantises to 4 bits and pack as float.
            quantize(struct.unpack('<h', stream.read(2))[0], max_val=15),
            quantize(struct.unpack('<h', stream.read(2))[0], max_val=15),
            quantize(struct.unpack('<h', stream.read(2))[0], max_val=15),
        ))

    return result


def read_chunks(stream: io.BytesIO, individual_size: int) -> list[bytes]:
    # Reads an unsigned short (2 bytes).
    count = struct.unpack('<H', stream.read(2))[0]

    result = list[bytes]()
    for _ in range(count):
        result.append(stream.read(individual_size))

    return result


def read_positions(stream: io.BytesIO) -> list[bytes]:
    # Reads an unsigned short (2 bytes).
    count = struct.unpack('<H', stream.read(2))[0]

    result = list[bytes]()
    for _ in range(count):
        result.append(
            # Reads three floats (12 bytes).
            stream.read(3*4),
        )

    return result


def read_normal_idens(stream: io.BytesIO) -> list[bytes]:
    # Reads an unsigned short (2 bytes).
    count = struct.unpack('<H', stream.read(2))[0]

    result = list[bytes]()
    for _ in range(count):
        result.append(
            # Converts u8 to u32 to ensure compatibility with CSGv2.
            stream.read(1)+b'\0\0\0',
        )

    return result


def read_vertices(stream: io.BytesIO) -> tuple[list[int], int]:
    # Reads an unsigned int (4 bytes).
    vertex_count = struct.unpack('<I', stream.read(4))[0]

    # Reads an unsigned int (4 bytes).
    vertex_data_len = struct.unpack('<I', stream.read(4))[0]

    vertex_data = list[int]()
    for _ in range(vertex_data_len):
        vertex_data.append(
            # Reads a single byte (1 byte).
            struct.unpack('<B', stream.read(1))[0],
        )

    return (vertex_data, vertex_count)


def read_range_markers(stream: io.BytesIO) -> list[int]:
    # Reads an unsigned char (1 byte).
    n_range_markers = struct.unpack('<B', stream.read(1))[0]

    range_markers = list[int]()
    for _ in range(n_range_markers):
        range_markers.append(
            # Reads an unsigned int (4 bytes).
            struct.unpack('<I', stream.read(4))[0],
        )

    return range_markers


def convert_to_csgmdl2(csgmdl_buffer: bytes) -> bytes:
    # Create a buffer stream for reading the data
    stream = io.BytesIO(csgmdl_buffer)

    # Define the header and check if it matches the expected value
    HEADER = b'\x15\x7d\x29\x15\x75\x6c\x35\x04\x34\x69'
    assert stream.read(10) == HEADER, "Buffer is not CSGMDLV5"

    # Reads three floats (12 bytes).
    positions = read_chunks(stream, 3*4)

    normals = read_chunks_vector3(stream)

    # Reads a `G3D::Color4uint8`.
    colours = read_chunks(stream, 4)

    normal_idens = read_normal_idens(stream)

    # Reads a `G3D::Vector2`, which contains two floats.
    uvs = read_chunks(stream, 2*4)

    tangents = read_chunks_vector3(stream)

    assert (
        len(positions) ==
        len(normals) ==
        len(colours) ==
        len(normal_idens) ==
        len(uvs)
    )

    (vertex_data, vertex_count) = read_vertices(stream)
    range_markers = read_range_markers(stream)

    # Read the state machine indices and store them in a list
    indices = read_state_machine(vertex_data, vertex_count)
    indices = trim_indices(indices, range_markers)

    '''
    Packs chunks in the following manner:

    pub struct Vertex{
        pub pos:[f32;3],
        pub norm:[f32;3],
        pub color:[u8;4],
        pub normal_id:NormalId2,
        pub tex:[f32;2],
        #[brw(magic=0u128)]
        pub tangent:[f32;3],
        #[brw(magic=0u128)]
        // This field does not exist in the final struct and
        // exists purely to de/serialize the magic number.
        #[br(temp)]
        #[bw(ignore)]
        #[brw(magic=0u128)]
        _magic:(),
    }
    '''
    vertices_packed = b''.join(
        b''.join(v) for v in zip(
            positions,
            normals,
            colours,
            normal_idens,
            uvs,
            itertools.repeat(b'\0'*16),
            tangents,
            itertools.repeat(b'\0'*16),
        )
    )

    assert len(vertices_packed) / len(positions) == 84

    # Packs unsigned ints (4 bytes).
    indices_packed = struct.pack('<%dI' % len(indices), *indices)

    '''
    #[brw(little)]
    pub struct Mesh2{
        pub vertex_count:u32,
        // vertex data length
        #[brw(magic=84u32)]
        #[br(count=vertex_count)]
        pub vertices:Vec<Vertex>,
        pub face_count:u32,
        #[br(count=face_count/3)]
        pub faces:Vec<[VertexId;3]>,
    }

    #[brw(little)]
    #[brw(magic=b"CSGMDL")]
    pub struct CSGMDL2{
        #[brw(magic=2u32)]
        pub hash:Hash,
        pub mesh:Mesh2,
    }
    '''
    return b''.join([

        # Skip re-encrypting header since the header is already encrypted.
        CSG_HEADER.MDL2.value,

        xor_encrypt(b''.join([
            # Hash
            create_hash(
                vertices=vertices_packed,
                indices=indices_packed,
                salt=b'67'*8,
            ),

            # Vertex count
            len(positions).to_bytes(4, byteorder='little'),

            # Size (in bytes) of each individual vertex datum
            (84).to_bytes(4, byteorder='little'),

            # Vertex data
            vertices_packed,

            # Index count
            len(indices).to_bytes(4, byteorder='little'),

            # Index data
            indices_packed,

        ]), offset=len(CSG_HEADER.MDL2.value))
    ])
