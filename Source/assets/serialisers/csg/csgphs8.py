import enum
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
    num_clusters = total_bits // CLUSTER_SIZE
    for cluster_num in range(num_clusters):
        cluster_base = CLUSTER_SIZE * cluster_num

        # Since clusters are least-significant-bit aligned,
        # The final cluster is smaller than 4 bytes.
        if cluster_num == num_clusters - 1:
            cluster_size = total_bits % CLUSTER_SIZE
        else:
            cluster_size = CLUSTER_SIZE

        # Each cluster has its bytes read from last to first.
        for byte_num in range(cluster_size):
            byte_idx = cluster_base + cluster_size - 1 - byte_num

            # Each byte has its bits read from last to first.
            for bit_shift in range(7, -1, -1):
                yield (clers_bytes[byte_idx] >> bit_shift) & 0b0000_0001
    return


def get_next_edge(c: int) -> int:
    if c % 3 == 2:
        return c - 2
    return c + 1


def get_prev_edge(c: int) -> int:
    if c % 3 == 0:
        return c + 2
    return c - 1


def zip_boundary(cursor_edge: int, adjacency_list: list[int], index_list: list[int]) -> int:
    current_edge = cursor_edge

    # Loops while an edge set to SENTINEL_PROCESSING still needs to be paired.
    # Infinitely loops if bad format.
    while adjacency_list[current_edge] == SENTINEL_PROCESSING:
        candidate_edge = get_next_edge(current_edge)

        # Walks the fan via twin, then next until we reach a boundary edge.
        # Infinitely loops if bad format.
        while adjacency_list[candidate_edge] >= 0:
            opposite_edge = adjacency_list[candidate_edge]
            candidate_edge = get_next_edge(opposite_edge)

        if adjacency_list[candidate_edge] != SENTINEL_BOUNDARY:
            break

        # Links the two boundary edges as twins (zips them shut).
        adjacency_list[current_edge] = candidate_edge
        adjacency_list[candidate_edge] = current_edge

        prev_edge = current_edge = get_prev_edge(current_edge)
        prev_cand_edge = get_prev_edge(candidate_edge)

        # Rewrites the merged corner with the surviving (donor) vertex iden.
        index_list[get_prev_edge(current_edge)] = index_list[prev_cand_edge]

        # Propagates that vertex iden around the rest of the merged fan.
        connected_edge = adjacency_list[current_edge]

        # Infinitely loops if bad format.
        while connected_edge >= 0 and candidate_edge != prev_edge:
            prev_edge = get_prev_edge(connected_edge)
            prev_of_prev = get_prev_edge(prev_edge)
            index_list[prev_of_prev] = index_list[prev_cand_edge]
            connected_edge = adjacency_list[prev_edge]

        # Hops along the connected fan to the next still-unzipped edge.
        # Infinitely loops if bad format.
        while adjacency_list[current_edge] >= 0 and current_edge != candidate_edge:
            next_link = adjacency_list[current_edge]
            current_edge = get_prev_edge(next_link)

    return current_edge


class CLERS(enum.Enum):
    C = 0b0
    L = 0b110
    E = 0b111
    R = 0b101
    S = 0b100


def decode_clers_symbols(bitreader: Iterator[int]) -> Iterator[CLERS]:
    # Infinitely loops if bad format.
    while (b1 := next(bitreader, None)) is not None:

        if b1 == 0:
            yield CLERS.C
            continue

        b2 = next(bitreader, None)
        if b2 is None:
            return

        b3 = next(bitreader, None)
        if b3 is None:
            return

        op = (
            (b1 * 0b100) +
            (b2 * 0b010) +
            (b3 * 0b001)
        )

        if op == 0b110:
            yield CLERS.L
            continue

        if op == 0b111:
            yield CLERS.E
            continue

        if op == 0b101:
            yield CLERS.R
            continue

        if op == 0b100:
            yield CLERS.S
            continue


def _decode_triangles(
    clers_iter: Iterator[CLERS],
    adjacency_list: list[int],
    index_list: list[int],
    current_triangle: int,
    vertex_counter: int,
) -> tuple[int, int]:
    cursor_stack = [1]

    # Infinitely loops if bad format.
    while len(cursor_stack) > 0:
        temp_cursor_edge = cursor_stack[-1]

        # Emits a new triangle and glue its edge 0 to cursor_edge as twins;
        # Edges 1 and 2 inherit the corner vertices from the gate edge.
        current_triangle += 1
        tri_base_edge = 3 * current_triangle

        # Expands adjacency and index lists to prevent against index overflow errors.
        if tri_base_edge >= len(adjacency_list):
            extension_len = tri_base_edge - len(adjacency_list)
            adjacency_list.extend([SENTINEL_UNINIT] * extension_len)
            index_list.extend([+0] * extension_len)
        else:
            adjacency_list[tri_base_edge + 0] = SENTINEL_UNINIT
            adjacency_list[tri_base_edge + 1] = SENTINEL_UNINIT
            adjacency_list[tri_base_edge + 2] = SENTINEL_UNINIT

        adjacency_list[temp_cursor_edge] = tri_base_edge
        adjacency_list[tri_base_edge] = temp_cursor_edge

        index_list[tri_base_edge + 1] = (
            index_list[get_prev_edge(temp_cursor_edge)]
        )
        index_list[tri_base_edge + 2] = (
            index_list[get_next_edge(temp_cursor_edge)]
        )
        cursor_stack[-1] = tri_base_edge + 1

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
            adjacency_list[cursor_stack[-1]] = SENTINEL_PROCESSING
            cursor_stack[-1] = get_next_edge(cursor_stack[-1])
            continue

        if op == CLERS.E:  # E: end
            adjacency_list[cursor_stack[-1]] = SENTINEL_PROCESSING
            next_edge = get_next_edge(cursor_stack[-1])
            adjacency_list[next_edge] = SENTINEL_PROCESSING
            zip_boundary(
                cursor_edge=next_edge,
                adjacency_list=adjacency_list,
                index_list=index_list,
            )
            cursor_stack.pop()
            continue

        if op == CLERS.R:  # R: turn right
            next_edge = get_next_edge(cursor_stack[-1])
            adjacency_list[next_edge] = SENTINEL_PROCESSING
            zip_boundary(
                cursor_edge=next_edge,
                adjacency_list=adjacency_list,
                index_list=index_list,
            )
            continue

        if op == CLERS.S:  # S: split
            current = cursor_stack.pop()
            cursor_stack.append(get_next_edge(current))
            cursor_stack.append(current)
            continue

    return (current_triangle, vertex_counter)


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
    enum_counts = {
        e: sum(1 for v in clers_data if v == e)
        for e in CLERS
    }
    print([
        (geom_type, e1, e2)
        for e1, c1 in enum_counts.items()
        for e2, c2 in enum_counts.items()
        if e1 != e2 and (c1 - c2 == hull_count or c1 == c2)
    ])

    vertex_counter = 2
    for _h in range(hull_count):
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

        (current_triangle, vertex_counter) = _decode_triangles(
            clers_iter=clers_iter,
            adjacency_list=adjacency_list,
            index_list=index_list,
            current_triangle=current_triangle,
            vertex_counter=vertex_counter,
        )

        hull_verts = []
        hull_tris = []
        max_local_idx = 0
        for t in range(current_triangle):
            base = 3 * t
            i0 = index_list[base + 0]
            i1 = index_list[base + 1]
            i2 = index_list[base + 2]
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
        hull_verts.extend(all_vertices[
            global_vert_start:
            global_vert_end
        ])

        hulls.append(Hull(vertices=hull_verts, triangles=hull_tris))
        global_vert_start = global_vert_end

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
        import zstandard
        phs_data = zstandard.decompress(phs_data)
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
