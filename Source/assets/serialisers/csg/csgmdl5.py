from .util import OBFUSCATION_NOISE_CYCLE_XOR, xor_encrypt
from dataclasses import dataclass
from typing import Any
import struct
import io


@dataclass
class Faces5:
    indices: list[int]
    unknown: Any


def read_u32(data):
    return struct.unpack('<I', data[:4])[0]


def read_faces5(reader) -> Faces5:
    faces_inner_data = reader.read(16)
    vertex_count, vertex_data_len, range_marker_count = struct.unpack(
        '<III', faces_inner_data)

    if vertex_data_len % 4 != 0:
        raise ValueError("Invalid vertex data length")

    vertex_data = reader.read(vertex_data_len)
    range_markers = [
        read_u32(reader.read(4))
        for _ in range(range_marker_count)
    ]

    indices = read_state_machine(vertex_data, vertex_count)

    if indices[-1] > len(indices):
        raise ValueError(
            f"Marker {len(range_markers)} (value {indices[-1]}) out of range")

    for i, marker in enumerate(range_markers[1:], start=1):
        if marker < range_markers[i - 1]:
            raise ValueError(
                f"Marker {i} (value {marker}) is less than marker {i-1} (value {range_markers[i-1]})")
        if indices[-1] > marker:
            raise ValueError(f"Marker {i} (value {marker}) out of range")

    unknown = []

    for marker in [read_u32(reader.read(4)) for _ in range(len(range_markers) - 1)]:
        if marker != 0:
            indices = indices[marker:]
        if len(indices) > 0:
            unknown.append(indices)
        if reader.tell() < len(faces_inner_data):
            raise ValueError("Not enough range markers")

    return Faces5(indices, unknown)


class BufferStream:
    def __init__(self, buffer: bytes):
        super().__init__()
        self.buffer = buffer
        self.pos = 0

    def read_string(self, length: int) -> str:
        data = self.buffer[self.pos:self.pos + length]
        self.pos += length
        return data.decode('utf-8')

    def read_u16(self) -> int:
        value, = struct.unpack('<H', self.buffer[self.pos:self.pos + 2])
        self.pos += 2
        return value

    def read_u32(self) -> int:
        value, = struct.unpack('<I', self.buffer[self.pos:self.pos + 4])
        self.pos += 4
        return value

    def read_f32(self) -> float:
        value, = struct.unpack('<f', self.buffer[self.pos:self.pos + 4])
        self.pos += 4
        return value

    def read_i16(self) -> int:
        value, = struct.unpack('<h', self.buffer[self.pos:self.pos + 2])
        self.pos += 2
        return value

    def read_u8(self) -> int:
        value, = struct.unpack('B', self.buffer[self.pos:self.pos + 1])
        self.pos += 1
        return value


@dataclass
class Vector3:
    x: float
    y: float
    z: float


@dataclass
class Vector2:
    u: float
    v: float


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


@dataclass
class ParsedCSGMDLV5:
    positions: bytearray
    normals: bytearray
    colors: bytearray
    normal_ids: list[int]
    uvs: list[Vector2]
    tangents: list[Vector3]
    faces: list[int]


def parse(csgmdl_buffer: bytes) -> ParsedCSGMDLV5:
    # Create a buffer stream for reading the data
    stream = io.BytesIO(xor_encrypt(csgmdl_buffer, 0))

    # Define the header and check if it matches the expected value
    HEADER = b'\x15\x7d\x29\x15\x75\x6c\x35\x04\x34\x69'
    assert stream.read(10) == HEADER, "Buffer is not CSGMDLV5"

    # Read the positions data and store it in a bytearray
    positions = bytearray()
    n_positions = struct.unpack('<H', stream.read(2))[
        0]  # Read an unsigned short (2 bytes)
    for _ in range(n_positions):
        positions.extend(stream.read(3*4))  # Read three floats (12 bytes)

    # Read the normals data and store it in a bytearray
    normals = bytearray()
    # Read an unsigned short (2 bytes)
    n_normals = struct.unpack('<H', stream.read(2))[0]
    for _ in range(n_normals):
        normals.extend(struct.pack(
            '<f<f<f',  # Pack three floats into a 12 byte string
            # Quantize to 4 bits and pack as float
            quantize(struct.unpack('<h', stream.read(2))[0], max_val=15),
            quantize(struct.unpack('<h', stream.read(2))[0], max_val=15),
            quantize(struct.unpack('<h', stream.read(2))[0], max_val=15),
        ))

    # Read the colors data and store it in a bytearray
    colors = bytearray()
    # Read an unsigned short (2 bytes)
    n_colors = struct.unpack('<H', stream.read(2))[0]
    for _ in range(n_colors):
        r = struct.unpack('<B', stream.read(1))[
            0]  # Read a single byte (1 byte)
        g = struct.unpack('<B', stream.read(1))[0]
        b = struct.unpack('<B', stream.read(1))[0]
        a = struct.unpack('<B', stream.read(1))[0]
        colors.append((r, g, b, a))

    # Read the normal IDs data and store it in a list
    normal_ids: list[int] = []
    n_normal_ids = struct.unpack('<H', stream.read(2))[
        0]  # Read an unsigned short (2 bytes)
    for _ in range(n_normal_ids):
        normal_ids.append(struct.unpack('<B', stream.read(1))
                          [0])  # Read a single byte (1 byte)

    # Read the UVs data and store it in a list of Vector2 objects
    uvs: list[Vector2] = []
    # Read an unsigned short (2 bytes)
    n_uvs = struct.unpack('<H', stream.read(2))[0]
    for _ in range(n_uvs):
        # Read two floats (4 bytes each)
        u = struct.unpack('<f', stream.read(4))[0]
        v = struct.unpack('<f', stream.read(4))[0]
        uvs.append(Vector2(u, v))

    # Read the tangents data and store it in a list of Vector3 objects
    tangents: list[Vector3] = []
    n_tangents = struct.unpack('<H', stream.read(2))[
        0]  # Read an unsigned short (2 bytes)
    stream.read(4)  # Number of bytes containing the components
    for _ in range(n_tangents):
        # Quantize to 4 bits and pack as float
        x = quantize(struct.unpack('<h', stream.read(2))[0], max_val=15)
        y = quantize(struct.unpack('<h', stream.read(2))[0], max_val=15)
        z = quantize(struct.unpack('<h', stream.read(2))[0], max_val=15)
        tangents.append(Vector3(x, y, z))

    # Read the number of vertices and store it in a variable
    n_vertices = struct.unpack('<I', stream.read(4))[
        0]  # Read an unsigned int (4 bytes)

    # Read the vertex data and store it in a list
    vertex_data: list[int] = []
    for _ in range(n_vertices):
        vertex_data.append(struct.unpack('<B', stream.read(1))[
                           0])  # Read a single byte (1 byte)

    # Read the number of range markers and store it in a variable
    n_range_markers = struct.unpack('<B', stream.read(1))[
        0]  # Read an unsigned char (1 byte)

    # Read the range markers data and store it in a list
    range_markers: list[int] = []
    for _ in range(n_range_markers):
        range_markers.append(struct.unpack('<I', stream.read(4))[
                             0])  # Read an unsigned int (4 bytes)

    # Read the state machine indices and store them in a list
    indices = read_state_machine(vertex_data, n_vertices)

    # Adjust the indices based on the range markers
    marker0 = range_markers[0]
    marker1 = range_markers[1]
    if marker0 != 0:
        indices = indices[marker0:]

    if len(range_markers) < 3:
        indices = indices[:marker1 - marker0]

    # Return a ParsedCSGMDLV5 object containing all the data
    return ParsedCSGMDLV5(
        positions=positions,
        normals=normals,
        colors=colors,
        normal_ids=normal_ids,
        uvs=uvs,
        tangents=tangents,
        faces=indices
    )
