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
    b"\x10\0\0\0" + b"\0" * 16 +
    b"\x10\0\0\0" + b"\0" * 12 +
    b"\0\0\x80\x3F"
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

    for i in range(len(index_list)):
        if adjacency_list[i] == SENTINEL_BOUNDARY:
            continue
        if adjacency_list[i] == SENTINEL_PROCESSING:
            continue
        if adjacency_list[i] == SENTINEL_UNINIT:
            continue
        if i != adjacency_list[adjacency_list[i]]:
            return False
    return True


class CLERS(enum.Enum):
    C = 0b0
    L = 0b110
    E = 0b111
    R = 0b101
    S = 0b100


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
) -> tuple[int, list[int], list[int]]:

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

    current_triangle = 1
    vertex_counter = 0
    cursor_stack = [1]

    # Infinitely loops if bad format.
    while len(cursor_stack) > 0:
        temp_cursor_edge = cursor_stack[-1]

        # Emits a new triangle and glue its edge 0 to cursor_edge as twins;
        # Edges 1 and 2 inherit the corner vertices from the gate edge.
        tri_base_edge = 3 * current_triangle
        current_triangle += 1

        adjacency_list[tri_base_edge] = temp_cursor_edge
        adjacency_list[temp_cursor_edge] = tri_base_edge

        (
            index_list[get_next_edge(tri_base_edge)],
            index_list[get_prev_edge(tri_base_edge)],
        ) = (
            index_list[get_prev_edge(temp_cursor_edge)],
            index_list[get_next_edge(temp_cursor_edge)],
        )

        cursor_stack[-1] = get_next_edge(tri_base_edge)

        op = next(clers_iter, None)
        if op is None:
            break

        if op == CLERS.C:  # C: introduce new vertex
            vertex_counter += 1
            index_list[tri_base_edge] = vertex_counter
            next_edge = get_next_edge(cursor_stack[-1])
            adjacency_list[next_edge] = SENTINEL_BOUNDARY
            continue

        if op == CLERS.L:  # L: turn left
            next_edge = get_next_edge(cursor_stack[-1])
            adjacency_list[next_edge] = SENTINEL_PROCESSING
            zip_boundary(
                c=next_edge,
                adjacency_list=adjacency_list,
                index_list=index_list,
            )
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
            cursor_stack[-1] = get_next_edge(cursor_stack[-1])
            adjacency_list[cursor_stack[-1]] = SENTINEL_PROCESSING
            continue

        if op == CLERS.S:  # S: split
            current = cursor_stack.pop()
            cursor_stack.append(get_next_edge(current))
            cursor_stack.append(current)
            continue

    return (current_triangle, adjacency_list, index_list)


def _edgebreaker_decode(
    clers_bytes: bytes,
    total_bits: int,
    hull_count: int,
    all_vertices: list[bytes],
    total_faces: int = 0,
    geom_type: int = 0,
) -> list[Hull]:
    hulls = []
    global_vert_start = 0

    est_capacity = max(total_faces * 3, 1024)
    bitreader = read_bits(clers_bytes, total_bits)
    clers_reader = decode_clers_symbols(bitreader)
    clers_data = list(clers_reader)
    clers_iter = iter(clers_data)
    current_triangle = 0
    vertex_offset = 2

    for _h in range(hull_count):
        (current_triangle, adjacency_list, index_list) = _decode_triangles(
            clers_iter=clers_iter,
            est_capacity=est_capacity,
        )

        assert (test_lists(adjacency_list, index_list))

        hull_tris = []
        max_local_idx = 0
        for t in range(current_triangle):
            base = 3 * t
            i0 = index_list[base + 0] + vertex_offset
            i1 = index_list[base + 1] + vertex_offset
            i2 = index_list[base + 2] + vertex_offset
            if i0 == i1:
                continue
            if i0 == i2:
                continue
            if i1 == i2:
                continue
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

        vertex_offset = max_local_idx

    return hulls


def decode_raw_hulls(data: bytes) -> list[Hull]:
    if len(data) == 0:
        return []

    stream = io.BytesIO(initial_bytes=data)
    hull_range_count = util.read_u32(stream)

    hull_ranges = [
        util.read_u32(stream)
        for _ in range(hull_range_count)
    ]

    # Index-base length is equal to the value of the last hull range (or 0 if none).
    total_index_count = hull_ranges[-1] if hull_ranges else 0

    index_base = [
        util.read_u32(stream)
        for _ in range(total_index_count)
    ]

    # If no component section exists, then there are no hulls to build.
    if stream.tell() == len(data):
        return []

    vertex_range_count = util.read_u32(stream)

    vertex_ranges = [
        util.read_u32(stream)
        for _ in range(vertex_range_count)
    ]

    total_vertex_count = vertex_ranges[-1] if vertex_ranges else 0
    assert total_vertex_count % 3 == 0
    component_data = [
        read_vector3(stream)
        for _ in range(total_vertex_count//3)
    ]

    hulls: list[Hull] = []

    idx_start = 0   # offset into `index_base` (in *elements*, not bytes)
    vert_start = 0  # offset into `component_data`

    for idx_end, vert_end in zip(hull_ranges, vertex_ranges):

        # Slices the raw buffers for this hull.
        idx_slice = index_base[idx_start:idx_end]
        vert_slice = component_data[vert_start:vert_end]

        # Converts the flat slices into groups of three.
        triangles = [
            (idx_slice[j + 0], idx_slice[j + 1], idx_slice[j + 2])
            for j in range(0, len(idx_slice), 3)
        ]

        hulls.append(Hull(vertices=vert_slice, triangles=triangles))

        # Advances the start pointers for the next iteration.
        idx_start = idx_end
        vert_start = vert_end

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
    total_verts = util.read_u32(zipped_stream)
    total_faces = util.read_u32(zipped_stream)
    first_hull_vert_count = util.read_u32(zipped_stream)
    first_hull_face_count = util.read_u32(zipped_stream)
    raw_hulls_size = util.read_u32(zipped_stream)
    clers_bit_count = util.read_u32(zipped_stream)
    clers_buffer_size = util.read_u32(zipped_stream)
    positions_size = util.read_u32(zipped_stream)
    bounding_box_min = read_vector3(zipped_stream)
    bounding_box_max = read_vector3(zipped_stream)
    raw_hulls = zipped_stream.read(raw_hulls_size)
    clers_bytes = zipped_stream.read(clers_buffer_size)
    all_vertices = [
        read_vector3(zipped_stream)
        for _ in range(total_verts)
    ]

    hulls = [
        *decode_raw_hulls(raw_hulls),
        *_edgebreaker_decode(
            clers_bytes,
            clers_bit_count,
            hull_count,
            all_vertices,
            total_faces,
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
