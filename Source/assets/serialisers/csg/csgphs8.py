# Works Cited:

# krakow10. (2025). rbx_mesh/src/union_physics/v8/edgebreaker.rs at master · krakow10/rbx_mesh. GitHub.
# https://github.com/krakow10/rbx_mesh/blob/master/src/union_physics/v8/edgebreaker.rs

# Rossignac, J., Safonova, A., & Szymczak, A. (2001). Rossignac, Safonova, Szymczak:3D Compression Made Simple 3D Compression Made Simple: Edgebreaker on a Corner-Table.
# https://faculty.cc.gatech.edu/~jarek/papers/CornerTableSMI.pdf

import enum
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


def test_lists(
    adjacency_list: list[int],
    index_list: list[int],
) -> bool:
    if len(index_list) != len(adjacency_list):
        return False

    for i in range(len(adjacency_list)):
        if adjacency_list[i] == SENTINEL_BOUNDARY:
            continue
        if adjacency_list[i] == SENTINEL_PROCESSING:
            continue
        if adjacency_list[i] == SENTINEL_UNINIT:
            continue
        if not (0 <= index_list[i] < len(adjacency_list)):
            return False
        if i != adjacency_list[adjacency_list[i]]:
            return False
    return True


class CLERS(enum.Enum):
    C = 0b0
    L = 0b1_01
    E = 0b1_11
    R = 0b1_10
    S = 0b1_00


def decode_clers_symbols(bitreader: Iterator[int]) -> Iterator[CLERS]:
    # Infinitely loops if bad format.
    while (b1 := next(bitreader, None)) is not None:

        if b1 == CLERS.C.value:
            yield CLERS.C
            continue

        b2 = next(bitreader)
        b3 = next(bitreader)

        op = (
            (b1 * 0b100) +
            (b2 * 0b010) +
            (b3 * 0b001)
        )

        if op == CLERS.L.value:
            yield CLERS.L
            continue

        if op == CLERS.E.value:
            yield CLERS.E
            continue

        if op == CLERS.R.value:
            yield CLERS.R
            continue

        if op == CLERS.S.value:
            yield CLERS.S
            continue


def zip_boundary(c: int, adjacency_list: list[int], index_list: list[int]):
    while True:
        b = get_next_edge(c)

        while adjacency_list[b] >= 0:
            b = get_next_edge(adjacency_list[b])

        if adjacency_list[b] != SENTINEL_BOUNDARY:
            return

        adjacency_list[c] = b
        adjacency_list[b] = c

        a = get_prev_edge(c)
        index_list[get_prev_edge(a)] = index_list[get_prev_edge(b)]

        while adjacency_list[a] >= 0 and b != a:
            a = get_prev_edge(adjacency_list[a])
            index_list[get_prev_edge(
                a)] = index_list[get_prev_edge(b)]

        c = get_prev_edge(c)
        while adjacency_list[c] >= 0 and c != b:
            c = get_prev_edge(adjacency_list[c])

        if adjacency_list[c] != SENTINEL_PROCESSING:
            return


def _decode_triangles(
    clers_iter: Iterator[CLERS],
    est_capacity: int,
) -> tuple[int, int, list[int], list[int]]:

    # Middle edge (1) left as SENTINEL_UNINIT so the decoder starts walking from it.
    adjacency_list = [
        SENTINEL_BOUNDARY,  # [0]
        SENTINEL_UNINIT,  # [1]
        SENTINEL_BOUNDARY,  # [2]
        *[SENTINEL_UNINIT] * (est_capacity - 3),  # [3:]
    ]
    # Implicit first triangle: indices [0,1,2].
    # Outer edges marked boundary.
    index_list = [
        +0,  # [0]
        +1,  # [1]
        +2,  # [2]
        *[+0] * (est_capacity - 3),  # [3:]
    ]

    vertex_counter = 3
    cursor_stack = [1]
    triangle_count = 1

    # Infinitely loops if bad format.
    while len(cursor_stack) > 0:

        # Emits a new triangle and glue its edge 0 to cursor_edge as twins;
        # Edges 1 and 2 inherit the corner vertices from the gate edge.
        tri_base_edge = 3 * triangle_count
        triangle_count += 1

        adjacency_list[tri_base_edge] = cursor_stack[-1]
        adjacency_list[cursor_stack[-1]] = tri_base_edge

        (
            index_list[get_next_edge(tri_base_edge)],
            index_list[get_prev_edge(tri_base_edge)],
        ) = (
            index_list[get_prev_edge(cursor_stack[-1])],
            index_list[get_next_edge(cursor_stack[-1])],
        )

        cursor_stack[-1] = get_next_edge(tri_base_edge)

        op = next(clers_iter, None)
        if op is None:
            break

        if op == CLERS.C:  # C: introduce new vertex
            index_list[tri_base_edge] = vertex_counter
            next_edge = get_next_edge(cursor_stack[-1])
            adjacency_list[next_edge] = SENTINEL_BOUNDARY
            vertex_counter += 1
            continue

        if op == CLERS.L:  # L: turn left
            adjacency_list[cursor_stack[-1]] = SENTINEL_PROCESSING
            cursor_stack[-1] = get_next_edge(cursor_stack[-1])
            continue

        if op == CLERS.E:  # E: end
            adjacency_list[cursor_stack[-1]] = SENTINEL_PROCESSING
            next_edge = get_next_edge(cursor_stack[-1])
            adjacency_list[next_edge] = SENTINEL_PROCESSING
            zip_boundary(
                c=next_edge,
                adjacency_list=adjacency_list,
                index_list=index_list,
            )
            cursor_stack.pop()
            continue

        if op == CLERS.R:  # R: turn right
            next_edge = get_next_edge(cursor_stack[-1])
            adjacency_list[next_edge] = SENTINEL_PROCESSING
            zip_boundary(
                c=next_edge,
                adjacency_list=adjacency_list,
                index_list=index_list,
            )
            continue

        if op == CLERS.S:  # S: split
            current = cursor_stack.pop()
            cursor_stack.append(get_next_edge(current))
            cursor_stack.append(current)
            continue

    return (vertex_counter, triangle_count, adjacency_list, index_list)


def _edgebreaker_decode(
    clers_bytes: bytes,
    total_bits: int,
    hull_count: int,
    all_vertices: list[bytes],
    total_triangles: int = 0,
    geom_type: int = 0,
) -> list[Hull]:
    hulls = []
    global_vert_start = 0

    est_capacity = total_triangles * 3
    bitreader = read_bits(clers_bytes, total_bits)
    clers_reader = decode_clers_symbols(bitreader)
    clers_data = list(clers_reader)
    clers_iter = iter(clers_data)
    vertex_offset = 0

    for _ in range(hull_count):
        (vertex_count, triangle_count, adjacency_list, index_list) = _decode_triangles(
            clers_iter=clers_iter,
            est_capacity=est_capacity,
        )

        assert test_lists(adjacency_list, index_list)

        hull_tris = []
        max_local_idx = 0
        for base in range(0, vertex_count, 3):
            i0 = index_list[base + 0]
            i1 = index_list[base + 1]
            i2 = index_list[base + 2]
            assert i0 != i1
            assert i0 != i2
            assert i1 != i2
            vals = (i0, i1, i2)
            hull_tris.append(vals)
            max_local_idx = max(max_local_idx, *vals)

        global_vert_end = global_vert_start + max_local_idx + 1
        hull_verts = all_vertices[
            global_vert_start:
            global_vert_end
        ]
        global_vert_start = global_vert_end

        hulls.append(Hull(
            vertices=hull_verts,
            triangles=hull_tris,
        ))

        assert max_local_idx - vertex_offset < vertex_count
        vertex_offset += vertex_count

    return hulls


def _decode_raw_hulls(data: bytes) -> list[Hull]:
    if len(data) == 0:
        return []

    stream = io.BytesIO(initial_bytes=data)
    tri_range_count = util.read_u32(stream)

    tri_ranges = [
        util.read_u32(stream)
        for _ in range(tri_range_count)
    ] or [0]

    # Count length is equal to the value of the last range's value (or 0 if none).
    total_triangle_count = tri_ranges[-1]
    triangle_array = [
        util.read_u32(stream)
        for _ in range(total_triangle_count)
    ]

    # If no component section exists, then there are no hulls to build.
    if stream.tell() == len(data):
        return []

    vertex_range_count = util.read_u32(stream)

    vertex_ranges = [
        util.read_u32(stream)
        for _ in range(vertex_range_count)
    ] or [0]

    # Count is equal to the value of the last range's value (or 0 if none).
    total_vertex_count = vertex_ranges[-1]
    assert total_vertex_count % 3 == 0
    vertex_array = [
        read_vector3(stream)
        for _ in range(total_vertex_count//3)
    ]

    hulls: list[Hull] = []

    tri_start = 0   # offset into `index_base` (in *elements*, not bytes)
    vert_start = 0  # offset into `component_data`

    for i in range(1, len(tri_ranges)):

        tri_start = tri_ranges[i-1]
        tri_end = tri_ranges[i-0]

        vert_start = vertex_ranges[i-1]
        vert_end = vertex_ranges[i-0]

        # Slices the raw buffers for this hull.
        idx_slice = triangle_array[tri_start:tri_end]
        vert_slice = vertex_array[vert_start:vert_end]

        # Converts the flat slices into groups of three.
        triangles = [
            (idx_slice[j + 0], idx_slice[j + 1], idx_slice[j + 2])
            for j in range(0, len(idx_slice), 3)
        ]

        hulls.append(Hull(vertices=vert_slice, triangles=triangles))

    return hulls


def read_vector3(stream: io.BytesIO) -> bytes:
    # Reads three floats (12 bytes).
    return stream.read(3*4)


def convert_to_csgphs3(csgphs_buffer: bytes) -> bytes:
    # Creates a buffer stream for reading the data.
    stream = io.BytesIO(csgphs_buffer)

    # Defines the header and check if it matches the expected value.
    header = stream.read(10)
    assert header == util.CSG_HEADER.PHS8.value, "Buffer is not CSGPHS8"
    geom_type = util.read_u16(stream)

    phs_data = stream.read()
    try:
        import pyzstd
        phs_data = pyzstd.decompress(phs_data)
    except Exception as e:
        pass

    zipped_stream = io.BytesIO(phs_data)

    hull_count = util.read_u32(zipped_stream)
    vert_count = util.read_u32(zipped_stream)
    tri_count = util.read_u32(zipped_stream)
    first_hull_vert_count = util.read_u32(zipped_stream)
    first_hull_tri_count = util.read_u32(zipped_stream)
    raw_hulls_len = util.read_u32(zipped_stream)
    clers_bit_count = util.read_u32(zipped_stream)
    clers_buffer_len = util.read_u32(zipped_stream)
    verts_len = util.read_u32(zipped_stream)
    bounding_box_min = read_vector3(zipped_stream)
    bounding_box_max = read_vector3(zipped_stream)
    raw_hulls = zipped_stream.read(raw_hulls_len)
    clers_bytes = zipped_stream.read(clers_buffer_len)
    all_vertices = [
        read_vector3(zipped_stream)
        for _ in range(vert_count)
    ]

    hulls = [
        *_decode_raw_hulls(raw_hulls),
        *_edgebreaker_decode(
            clers_bytes,
            clers_bit_count,
            hull_count,
            all_vertices,
            tri_count,
            geom_type,
        ),
    ]

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
            for h in hulls
        ),
    ])
