from . import util

import dataclasses
import struct
import io


# 40-byte magic header that prefixes a CSGPHS V6/V7 Mesh struct.
_CSGPHS_MESH_MAGIC = (
    b"\x10\0\0\0" + b"\0" * 16 +
    b"\x10\0\0\0" + b"\0" * 12 +
    b"\0\0\x80\x3F"
)


class State:
    adjacency: list[int] = []
    index: list[int] = []
    current_tri_idx: int = 0
    vertex_counter: int = 0


@dataclasses.dataclass
class Edgebreaker:
    vertices: list[bytes]
    triangles: list[tuple[int, int, int]]

# ---------------------------------------------------------------------------
# Edgebreaker decoder ported from clv2's Mesh Lab plugin (CSGPHS8 module).
# Decodes the CLERS bitstream + global vertex array into per-hull
# (vertices, triangles). This is the EXACT inverse of how Rōblox encodes
# CSGPHS8 hulls — preserves the original mesh-intrinsic triangulation
# instead of collapsing to a recomputed convex hull (ConvexHull throws
# away authored topology, e.g. flat-tile meshes become 2.15-cubes).
# ---------------------------------------------------------------------------


def _edgebreaker_decode(
    clers_bytes: bytes,
    total_bits: int,
    hull_count: int,
    all_vertices: list[bytes],
    total_faces: int = 0,
) -> list[Edgebreaker]:
    '''
    Returns list of {Vertices: [(x,y,z), ...], Triangles: [(a,b,c), ...]}
    1-based indices into Vertices, matching MeshLab convention. Uses 0-based
    here for python; convert at emit time.
    '''
    hulls = []
    bit_pos = 0
    total_words = (total_bits + 31) // 32

    def read_bit() -> int:
        nonlocal bit_pos
        if bit_pos >= total_bits:
            raise ValueError("Edgebreaker: read past end")
        word_idx = bit_pos // 0x20
        bit_in_word = bit_pos % 0x20

        bits_in_word = 32
        if word_idx == total_words - 1:
            bits_in_word = total_bits % 0x20
            if bits_in_word == 0:
                bits_in_word = 0x20

        shift = bits_in_word - bit_in_word - 1
        word = struct.unpack_from("<I", clers_bytes, word_idx * 4)[0]
        bit_pos += 1
        return (word >> shift) & 1

    global_vert_offset = 0

    def get_next_edge(c):
        if c % 3 == 2:
            return c - 2
        return c + 1

    def get_prev_edge(c):
        if c % 3 == 0:
            return c + 2
        return c - 1

    state = State()

    def zip_boundary(cursor_edge: int) -> int:
        adj = state.adjacency
        idx = state.index
        current_edge = cursor_edge
        safety_outer = 0
        while True:
            if adj[current_edge] != -2:
                break

            safety_outer += 1
            if safety_outer > 1000:
                raise RuntimeError("zip outer overflow")

            candidate_edge = get_next_edge(current_edge)
            safety_inner = 0
            while adj[candidate_edge] >= 0:
                safety_inner += 1
                if safety_inner > 1000:
                    raise RuntimeError("zip inner overflow")
                opposite = adj[candidate_edge]
                candidate_edge = get_next_edge(opposite)

            if adj[candidate_edge] != -1:
                break

            adj[current_edge] = candidate_edge
            adj[candidate_edge] = current_edge
            current_edge = get_prev_edge(current_edge)

            previous_edge = current_edge
            previous_candidate = get_prev_edge(candidate_edge)
            idx[get_prev_edge(current_edge)] = idx[previous_candidate]

            safety_inner = 0
            connected = adj[current_edge]
            while connected >= 0:
                safety_inner += 1
                if safety_inner > 1000:
                    raise RuntimeError("zip inner2 overflow")
                if candidate_edge == previous_edge:
                    break
                previous_edge = get_prev_edge(connected)
                prev_of_prev = get_prev_edge(previous_edge)
                idx[prev_of_prev] = idx[previous_candidate]
                connected = adj[previous_edge]

            safety_inner = 0
            while adj[current_edge] >= 0:
                safety_inner += 1
                if safety_inner > 1000:
                    raise RuntimeError("zip inner3 overflow")
                if current_edge == candidate_edge:
                    break
                next_link = adj[current_edge]
                current_edge = get_prev_edge(next_link)

        return current_edge

    def decode_recursive(cursor_edge, depth) -> bool:
        if depth > 500:
            raise RuntimeError("decode depth exceeded")
        adj = state.adjacency
        idx = state.index
        iter_count = 0
        while True:
            iter_count += 1
            if iter_count > 100000:
                raise RuntimeError("decode iter exceeded")

            state.current_tri_idx += 1
            triIdx = state.current_tri_idx
            tri_base_edge = 3 * triIdx

            if tri_base_edge >= len(adj):
                extension_len = tri_base_edge - len(adj)
                adj.extend([-3] * extension_len)
                idx.extend([+0] * extension_len)
            else:
                adj[tri_base_edge + 0] = -3
                adj[tri_base_edge + 1] = -3
                adj[tri_base_edge + 2] = -3

            adj[cursor_edge] = tri_base_edge
            adj[tri_base_edge] = cursor_edge

            idx[tri_base_edge + 1] = idx[get_prev_edge(cursor_edge)]
            idx[tri_base_edge + 2] = idx[get_next_edge(cursor_edge)]
            cursor_edge = tri_base_edge + 1

            b1 = read_bit()
            if b1 == 0:  # C
                state.vertex_counter += 1
                idx[tri_base_edge] = state.vertex_counter
                next_edge = get_next_edge(cursor_edge)
                adj[next_edge] = -1
                continue

            b2 = read_bit()
            b3 = read_bit()
            op = (
                (b1 * 4) +
                (b2 * 2) +
                (b3 * 1)
            )

            if op == 0b101:  # L
                adj[cursor_edge] = -2
                cursor_edge = get_next_edge(cursor_edge)
                continue

            if op == 0b111:  # E
                next_edge = get_next_edge(cursor_edge)
                adj[next_edge] = adj[cursor_edge] = -2
                zip_boundary(cursor_edge=next_edge)
                return True

            if op == 0b110:  # R
                next_edge = get_next_edge(cursor_edge)
                adj[next_edge] = -2
                zip_boundary(cursor_edge=next_edge)
                continue

            if op == 0b100:  # S
                if not decode_recursive(cursor_edge, depth=depth + 1):
                    return False
                cursor_edge = get_next_edge(cursor_edge)
                continue

    est_capacity = max(total_faces * 3, 1024)
    for _h in range(hull_count):
        state.current_tri_idx = 0
        state.vertex_counter = 2
        state.adjacency = [
            -1, -3, -1,
            *[-3] * (est_capacity - 3),
        ]
        state.index = [
            +2, +0, +1,
            *[+0] * (est_capacity - 3),
        ]

        try:
            ok = decode_recursive(cursor_edge=1, depth=0)
        except Exception as e:
            break
        if not ok:
            break

        hull_verts = []
        hull_tris = []
        max_local_idx = 0
        for t in range(state.current_tri_idx + 1):
            base = 3 * t
            i0 = state.index[base + 1]
            i1 = state.index[base + 2]
            i2 = state.index[base + 3]
            if i0 == i1:
                continue
            if i0 == i2:
                continue
            if i1 == i2:
                continue
            hull_tris.append((i0, i1, i2))
            max_local_idx = max(max_local_idx, i0, i1, i2)

        verts_consumed = max_local_idx + 1
        for v in range(verts_consumed):
            gv = global_vert_offset + v
            if gv < len(all_vertices):
                hull_verts.append(all_vertices[gv])
            else:
                hull_verts.append((0.0, 0.0, 0.0))

        hulls.append(Edgebreaker(vertices=hull_verts, triangles=hull_tris))
        global_vert_offset += verts_consumed

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
    GeomType = util.read_u16(stream)

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
    first_hull_face_coun = util.read_u32(zipped_stream)
    raw_hulls_size = util.read_u32(zipped_stream)
    total_bits = util.read_u32(zipped_stream)
    clers_buffer_size = util.read_u32(zipped_stream)
    vertices_size = util.read_u32(zipped_stream)
    bounding_box_min = read_vector3(zipped_stream)
    bounding_box_max = read_vector3(zipped_stream)
    raw_hulls = zipped_stream.read(raw_hulls_size)
    clers_bytes = zipped_stream.read(clers_buffer_size)
    all_vertices = [read_vector3(zipped_stream) for _ in range(total_verts)]

    hulls = _edgebreaker_decode(
        clers_bytes,
        total_bits,
        hull_count,
        all_vertices,
        total_faces,
    )

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
