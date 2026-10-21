'''
Works Cited:

krakow10. (2025). rbx_mesh/src/union_physics/v8/edgebreaker.rs at master · krakow10/rbx_mesh. GitHub.
https://github.com/krakow10/rbx_mesh/blob/master/src/union_physics/v8/edgebreaker.rs

Rossignac, J. "3D compression made simple: Edgebreaker with Zipandwrap on a corner-table." Proceedings International Conference on Shape Modeling and Applications, pp. 278-283, https://doi.org/10.1109/sma.2001.923399.

"Hydroxide/Dependencies/Captcha.Lua at 136FB36EB204C9DCD3926D040AB2BB2CE1319BAD · Salenware/Hydroxide." GitHub, https://github.com/Salenware/HYDROXIDE/blob/136fb36eb204c9dcd3926d040ab2bb2ce1319bad/DEPENDENCIES/Captcha.lua. Accessed 18 Oct. 2026.
'''
import math
from . import util

from collections.abc import Iterator
from dataclasses import dataclass
import struct
import io


# 40-byte magic header that prefixes a CSGPHS3, 6, or 7 mesh struct.
_CSGPHS_MESH_MAGIC = (
    # class btVector3 (transformTrans)
    b"\x10\x00\x00\x00" + (b"\x00" * 16) +

    # class btQuaternion (rotationStride)
    b"\x10\x00\x00\x00" + (b"\x00" * 12) + b"\x00\x00\x80\x3F"
)


SENTINEL_UNINIT = -3
SENTINEL_BOUNDARY = -1
SENTINEL_PROCESSING = -2


@dataclass
class Hull:
    vertices: list[bytes]
    triangles: list[tuple[int, int, int]]


CLUSTER_SIZE = 4


def read_bits(clers_bytes: bytes, total_bits: int) -> Iterator[int]:
    '''
    Reading bits goes in a weird order.
    https://github.com/krakow10/rbx_mesh/blob/master/src/union_physics/v8/roblox_bit_reader.rs
    '''
    # Bytes are clustered into groups of 4 (or fewer, if at the end) from first to last.
    num_clusters = math.ceil(total_bits / (8 * CLUSTER_SIZE))
    for cluster_num in range(num_clusters):

        # Clusters are least-significant-bit aligned.
        # The final cluster can be smaller than 4 bytes.
        cluster = clers_bytes[
            CLUSTER_SIZE * (cluster_num + 0):
            CLUSTER_SIZE * (cluster_num + 1)
        ]
        chunk_as_int = int.from_bytes(cluster, 'little')

        # Each chunk has its bits read from most to least significant.
        cluster_bit_count = min(total_bits, 8 * CLUSTER_SIZE)
        total_bits -= cluster_bit_count
        for i in range(cluster_bit_count):
            yield (chunk_as_int >> (cluster_bit_count - 1 - i)) % 2

    return


def get_next_edge(c: int) -> int:
    if c % 3 == 2:
        return c - 2
    return c + 1


def get_prev_edge(c: int) -> int:
    if c % 3 == 0:
        return c + 2
    return c - 1


def zip_boundary(current: int, adjacency_list: list[int], index_list: list[int]):
    while adjacency_list[current] == SENTINEL_PROCESSING:
        candidate = get_next_edge(current)

        while adjacency_list[candidate] >= 0:
            candidate = get_next_edge(adjacency_list[candidate])

        if adjacency_list[candidate] != SENTINEL_BOUNDARY:
            break

        adjacency_list[current] = candidate
        adjacency_list[candidate] = current

        current = get_prev_edge(current)
        previous = current

        candidatePrevious = get_prev_edge(candidate)
        index_list[get_prev_edge(current)] = index_list[candidatePrevious]

        connected = adjacency_list[current]
        while connected >= 0 and candidate != previous:
            previous = get_prev_edge(connected)
            index_list[get_prev_edge(previous)] = index_list[candidatePrevious]
            connected = adjacency_list[previous]

        while adjacency_list[current] >= 0 and current != candidate:
            current = get_prev_edge(adjacency_list[current])


def decode_faces(clers_bytes: bytes, bit_count: int, hull_count: int, face_count: int):
    bitreader = read_bits(clers_bytes, bit_count)
    adjacency_list = [SENTINEL_UNINIT] * (face_count * 3)
    index_list = [0] * (face_count * 3)
    race_ranges, vert_ranges = [0], [0]
    currentFace, vert_offset = 0, 0

    for _ in range(hull_count):
        firstEdge = currentFace * 3
        adjacency_list[firstEdge:firstEdge +
                       3] = (SENTINEL_BOUNDARY, SENTINEL_UNINIT, SENTINEL_BOUNDARY)
        index_list[firstEdge:firstEdge+3] = (0, 1, 2)
        currentFace += 1
        vert_count = 3

        def decode(cursor):
            nonlocal currentFace, vert_count, race_ranges, vert_ranges
            while True:
                edge0 = currentFace * 3
                edge1, edge2 = edge0 + 1, edge0 + 2
                adjacency_list[edge0], adjacency_list[edge1], adjacency_list[edge2] = cursor, SENTINEL_UNINIT, SENTINEL_UNINIT
                currentFace += 1
                adjacency_list[cursor] = edge0
                index_list[edge1] = index_list[get_prev_edge(cursor)]
                index_list[edge2] = index_list[get_next_edge(cursor)]
                cursor = edge1

                if next(bitreader) == 0:
                    index_list[edge0] = vert_count
                    adjacency_list[get_next_edge(cursor)] = SENTINEL_BOUNDARY
                    vert_count += 1
                    continue

                # Split, Left, Right, End
                symbol = 2*next(bitreader) + next(bitreader)

                if symbol == 0b00:
                    decode(cursor)
                    cursor = get_next_edge(cursor)
                elif symbol == 0b01:
                    adjacency_list[cursor] = SENTINEL_BOUNDARY
                    cursor = get_next_edge(cursor)
                elif symbol == 0b10:
                    next_edge = get_next_edge(cursor)
                    adjacency_list[next_edge] = SENTINEL_BOUNDARY
                    zip_boundary(next_edge, adjacency_list, index_list)
                else:
                    adjacency_list[cursor] = SENTINEL_BOUNDARY
                    next_edge = get_next_edge(cursor)
                    adjacency_list[next_edge] = SENTINEL_BOUNDARY
                    zip_boundary(next_edge, adjacency_list, index_list)
                    return

        decode(firstEdge + 1)
        vert_offset += vert_count
        race_ranges.append(currentFace * 3)
        vert_ranges.append(vert_offset * 3)

    return race_ranges, index_list, vert_ranges


def filter_ranges_into_hulls(face_ranges: list[int], faces: list[int], vert_ranges: list[int], verts: list[float]) -> list[Hull]:
    result = []
    for hullIndex in range(1, min(len(face_ranges), len(vert_ranges))):
        vertices = []

        for i in range(vert_ranges[hullIndex - 1], vert_ranges[hullIndex], 3):
            x, y, z = verts[i+0], verts[i+1], verts[i+2]
            vertices.append(struct.pack('<3f', x, y, z))

        triangles = []
        for i in range(face_ranges[hullIndex - 1], face_ranges[hullIndex], 3):
            x, y, z = faces[i+0], faces[i+1], faces[i+2]
            triangles.append((x, y, z))

        result.append(Hull(
            vertices=vertices,
            triangles=triangles,
        ))
    return result


def decode_csgphs8_hulls(csgphs_buffer: bytes) -> list[Hull]:

    # Creates a buffer stream for reading the data.
    csgphs_buffer_stream = io.BytesIO(csgphs_buffer)

    # Defines the header and check if it matches the expected value.
    header = csgphs_buffer_stream.read(10)
    assert header == util.CSG_HEADER.PHS8.value, "Buffer is not CSGPHS8"
    geom_type = util.read_u16(csgphs_buffer_stream)

    phs_data = csgphs_buffer_stream.read()
    try:
        import pyzstd
        phs_data = pyzstd.decompress(phs_data)
    except Exception as e:
        pass

    phs_data_stream = io.BytesIO(phs_data)

    hull_count = util.read_u32(phs_data_stream)
    vert_count = util.read_u32(phs_data_stream)
    face_count = util.read_u32(phs_data_stream)
    first_hull_vert_count = util.read_u32(phs_data_stream)
    first_hull_tri_count = util.read_u32(phs_data_stream)
    raw_hulls_len = util.read_u32(phs_data_stream)
    clers_bit_count = util.read_u32(phs_data_stream)
    clers_buffer_len = util.read_u32(phs_data_stream)
    verts_buffer_len = util.read_u32(phs_data_stream)
    bounding_box_min = util.read_vec3_f32(phs_data_stream)
    bounding_box_max = util.read_vec3_f32(phs_data_stream)

    raw_face_ranges = [0]
    raw_faces = []
    raw_vert_ranges = [0]
    raw_verts = []

    output = []
    if raw_hulls_len != 0:
        for _ in range(util.read_u32(phs_data_stream)):
            raw_face_ranges.append(util.read_u32(phs_data_stream))
        for _ in range(raw_face_ranges[-1]):
            raw_faces.append(util.read_u32(phs_data_stream))
        for _ in range(util.read_u32(phs_data_stream)):
            raw_vert_ranges.append(util.read_u32(phs_data_stream))
        for _ in range(raw_vert_ranges[-1]):
            raw_verts.append(util.read_f32(phs_data_stream))
        output.extend(filter_ranges_into_hulls(
            face_ranges=raw_face_ranges,
            faces=raw_faces,
            vert_ranges=raw_vert_ranges,
            verts=raw_verts,
        ))

    clers_bytes = phs_data_stream.read(clers_buffer_len)
    all_vertices = [
        util.read_f32(phs_data_stream)
        for _ in range(vert_count * 3)
    ]

    faceRanges, faces, vert_ranges = decode_faces(
        clers_bytes, clers_bit_count, hull_count, face_count)

    output.extend(filter_ranges_into_hulls(
        face_ranges=faceRanges,
        faces=faces,
        vert_ranges=vert_ranges,
        verts=all_vertices,
    ))

    return output


def convert_to_csgphs3(csgphs_buffer: bytes) -> bytes:

    result = decode_csgphs8_hulls(csgphs_buffer)
    return b''.join([
        util.CSG_HEADER.PHS3.value,
        *(
            b''.join([
                _CSGPHS_MESH_MAGIC,

                # Vertices
                struct.pack("<I", len(h.vertices) * 3),
                struct.pack("<I", 4),
                b''.join(h.vertices),

                # Triangles
                struct.pack("<I", len(h.triangles) * 3),
                b''.join(struct.pack("<3I", *t) for t in h.triangles),
            ])
            for h in result
        ),
    ])
