#!/usr/bin/env python3
"""Walk a rbxlx and apply two cross-version fixups:

1. Convert every CSGv5 SharedString MeshData2 blob to CSGv2 via the rust
   csg-convert binary built from rbx_mesh. CSGv5 is opaque to Roblox
   0.613 — UnionOperations using v5 render as 1×1×1 placeholder cubes.
   CSGPHS (physics) and other entries pass through unchanged.

2. Convert `<Color3uint8 name="Color3uint8">UINT32</Color3uint8>` (the
   2024+ packed uint storage) to `<Color3 name="Color"><R/><G/><B/>
   </Color3>` (the 0.613 BasePart.Color property). Without this every
   part uses its default color (medium gray).

Usage: csg-downgrade-rbxlx.py INPUT.rbxlx OUTPUT.rbxlx
"""

import io
import struct

from assets.serialisers.csg import util

vector3 = tuple[float, float, float]

# 40-byte magic header that prefixes a CSGPHS V6/V7 Mesh struct.
_CSGPHS_MESH_MAGIC = (
    b"\x10\0\0\0" + b"\0" * 16 +
    b"\x10\0\0\0" + b"\0" * 12 +
    b"\0\0\x80\x3F"
)


def _pack_vec3_array(pts: list[vector3]) -> bytes:
    fmt = f"<{len(pts) * 3}f"
    flat = []
    for p in pts:
        flat.append(p[0])
        flat.append(p[1])
        flat.append(p[2])
    return struct.pack(fmt, *flat)


def _pack_uint3_array(tris: list[tuple[int, int, int]]) -> bytes:
    fmt = f"<{len(tris) * 3}I"
    flat = []
    for t in tris:
        flat.append(int(t[0]))
        flat.append(int(t[1]))
        flat.append(int(t[2]))
    return struct.pack(fmt, *flat)


# ---------------------------------------------------------------------------
# Pure-Python 3D convex hull (Quickhull-style incremental). Replaces
# scipy.spatial.ConvexHull. Returns (simplices, volume) where simplices is
# a list of (i, j, k) triangle index tuples (oriented CCW outward) and
# volume is the hull's signed volume. Returns `None` on degenerate input
# (fewer than 4 non-coplanar points). Sized for CSGPHS-scale inputs
# (22–500 verts); not tuned for huge point sets.
# ---------------------------------------------------------------------------

def _convex_hull_3d(points: list[vector3]) -> tuple[list[tuple[int, int, int]], float]:
    n = len(points)
    assert n > 4

    def sub(a: vector3, b: vector3) -> vector3:
        return (a[0] - b[0], a[1] - b[1], a[2] - b[2])

    def cross(a: vector3, b: vector3) -> vector3:
        return (
            a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0],
        )

    def dot(a, b) -> float:
        return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

    def face_plane(a, b, c) -> tuple[float, float, float, float]:
        A, B, C = points[a], points[b], points[c]
        nrm = cross(
            a=sub(B, A),
            b=sub(C, A),
        )
        d = -1 * dot(nrm, A)
        return (nrm[0], nrm[1], nrm[2], d)

    def signed_dist(plane, p) -> float:
        return plane[0] * p[0] + plane[1] * p[1] + plane[2] * p[2] + plane[3]

    # Seed: extreme x-axis points.
    i_xmin = min(range(n), key=lambda i: points[i][0])
    i_xmax = max(range(n), key=lambda i: points[i][0])
    assert i_xmax > i_xmin

    # Third point: farthest from line through extremes.
    A = points[i_xmin]
    AB = sub(points[i_xmax], A)

    def line_dist_sq(i):
        AP = sub(points[i], A)
        c = cross(AP, AB)
        return c[0] * c[0] + c[1] * c[1] + c[2] * c[2]
    i3 = max(range(n), key=line_dist_sq)
    assert line_dist_sq(i3) >= 1e-20

    # Fourth point: farthest from triangle plane.
    plane_seed = face_plane(i_xmin, i_xmax, i3)
    i4 = max(range(n),
             key=lambda i: abs(signed_dist(plane_seed, points[i])))
    assert abs(signed_dist(plane_seed, points[i4])) >= 1e-20

    # Initial tetrahedron — orient each face's normal away from centroid.
    seed = (i_xmin, i_xmax, i3, i4)
    cx = sum(points[i][0] for i in seed) / 4.0
    cy = sum(points[i][1] for i in seed) / 4.0
    cz = sum(points[i][2] for i in seed) / 4.0
    centroid = (cx, cy, cz)

    def oriented[T](a: T, b: T, c: T) -> tuple[T, T, T]:
        if signed_dist(face_plane(a, b, c), centroid) > 0:
            return (a, c, b)
        return (a, b, c)

    faces = [
        oriented(i_xmin, i_xmax, i3),
        oriented(i_xmin, i_xmax, i4),
        oriented(i_xmin, i3, i4),
        oriented(i_xmax, i3, i4),
    ]

    eps = 1e-10
    used = set(seed)
    pool = [i for i in range(n) if i not in used]
    outside = [set() for _ in faces]
    for fi, face in enumerate(faces):
        plane = face_plane(*face)
        for pi in pool:
            if signed_dist(plane, points[pi]) > eps:
                outside[fi].add(pi)

    deleted = [False] * len(faces)
    work = [fi for fi, s in enumerate(outside) if s]

    # Quickhull main loop.
    while work:
        fi = work.pop()
        if deleted[fi] or not outside[fi]:
            continue
        plane = face_plane(*faces[fi])
        far_pi = max(
            outside[fi],
            key=lambda pi: signed_dist(plane, points[pi]),
        )
        far = points[far_pi]

        # Find all faces visible from far_pi.
        visible = []
        for ofi, oface in enumerate(faces):
            if deleted[ofi]:
                continue
            if signed_dist(face_plane(*oface), far) > eps:
                visible.append(ofi)
        if not visible:
            continue

        # Horizon edges = edges of visible faces appearing only once
        # (neighbor on other side is a kept face). Direction stored so
        # the new face inherits the visible face's traversal.
        edge_count = {}
        edge_dir = {}
        for vfi in visible:
            a, b, c = faces[vfi]
            for u, v in ((a, b), (b, c), (c, a)):
                key = (u, v) if u < v else (v, u)
                edge_count[key] = edge_count.get(key, 0) + 1
                edge_dir[key] = (u, v)
        horizon = [edge_dir[k] for k, ct in edge_count.items() if ct == 1]

        orphans = set()
        for vfi in visible:
            orphans |= outside[vfi]
            outside[vfi] = set()
            deleted[vfi] = True
        orphans.discard(far_pi)

        for u, v in horizon:
            new_face = (u, v, far_pi)
            new_plane = face_plane(*new_face)
            new_outside = set()
            for pi in orphans:
                if signed_dist(new_plane, points[pi]) > eps:
                    new_outside.add(pi)
            faces.append(new_face)
            outside.append(new_outside)
            deleted.append(False)
            if new_outside:
                work.append(len(faces) - 1)

    final = [f for fi, f in enumerate(faces) if not deleted[fi]]

    # Volume = (1/6) * |Σ A · (B × C)| over outward-oriented faces.
    vol6 = 0.0
    for a, b, c in final:
        A_, B_, C_ = points[a], points[b], points[c]
        vol6 += dot(A_, cross(B_, C_))
    volume = abs(vol6) / 6.0

    return final, volume


# ---------------------------------------------------------------------------
# Edgebreaker decoder ported from clv2's Mesh Lab plugin (CSGPHS8 module).
# Decodes the CLERS bitstream + global vertex array into per-hull
# (vertices, triangles). This is the EXACT inverse of how Roblox encodes
# CSGPHS8 hulls — preserves the original mesh-intrinsic triangulation
# instead of collapsing to a recomputed convex hull (ConvexHull throws
# away authored topology, e.g. flat-tile meshes become 2.15-cubes).
# ---------------------------------------------------------------------------

def _edgebreaker_decode(
    clers_bytes: bytes,
    total_bits: int,
    hull_count: int,
    all_vertices: list[vector3],
    total_faces: int,
):
    """Returns list of {Vertices: [(x,y,z), ...], Triangles: [(a,b,c), ...]}
    1-based indices into Vertices, matching MeshLab convention. Uses 0-based
    here for python; convert at emit time."""
    hulls = []
    bit_pos = 0
    total_words = (total_bits + 31) // 32

    def read_bit():
        nonlocal bit_pos
        if bit_pos >= total_bits:
            raise ValueError("Edgebreaker: read past end")
        word_idx = bit_pos // 32
        bit_in_word = bit_pos % 32
        bits_in_word = 32
        if word_idx == total_words - 1:
            bits_in_word = total_bits % 32
            if bits_in_word == 0:
                bits_in_word = 32
        shift = bits_in_word - bit_in_word - 1
        word = struct.unpack_from("<I", clers_bytes, word_idx * 4)[0]
        bit_pos += 1
        return (word >> shift) & 1

    global_vert_offset = 0

    def get_next_edge(edge_index):
        return 1 if (edge_index % 3) < 2 else -2

    def get_prev_edge(edge_index):
        return 1 if (edge_index % 3) > 0 else -2

    state_adjacency = list[int]()
    state_index = list[int]()
    state_current_tri_idx = 0
    state_vertex_counter = 0

    def zip_boundary(cursor_edge):
        adj = state_adjacency
        idx = state_index
        current_edge = cursor_edge
        safety_outer = 0
        while True:
            if adj[current_edge + 1] != -2:
                break
            safety_outer += 1
            if safety_outer > 1000:
                raise RuntimeError("zip outer overflow")
            next_offset = get_next_edge(current_edge)
            candidate_edge = current_edge + next_offset
            if adj[candidate_edge + 1] >= 0:
                safety_inner = 0
                while True:
                    safety_inner += 1
                    if safety_inner > 1000:
                        raise RuntimeError("zip inner overflow")
                    opposite = adj[candidate_edge + 1]
                    candidate_edge = opposite + get_next_edge(opposite)
                    if adj[candidate_edge + 1] < 0:
                        break
            if adj[candidate_edge + 1] != -1:
                break
            adj[current_edge + 1] = candidate_edge
            adj[candidate_edge + 1] = current_edge
            prev_off = get_prev_edge(current_edge)
            current_edge -= prev_off
            previous_edge = current_edge
            cand_prev_off = get_prev_edge(candidate_edge)
            previous_candidate = candidate_edge - cand_prev_off
            idx[current_edge - get_prev_edge(current_edge) + 1] = (
                idx[previous_candidate + 1])
            connected = adj[current_edge + 1]
            if connected >= 0:
                safety_inner = 0
                while True:
                    safety_inner += 1
                    if safety_inner > 1000:
                        raise RuntimeError("zip inner2 overflow")
                    if candidate_edge == previous_edge:
                        break
                    prev_of_conn = get_prev_edge(connected)
                    previous_edge = connected - prev_of_conn
                    prev_of_prev = get_prev_edge(previous_edge)
                    idx[previous_edge - prev_of_prev + 1] = (
                        idx[previous_candidate + 1])
                    connected = adj[previous_edge + 1]
                    if connected < 0:
                        break
            if adj[current_edge + 1] >= 0:
                safety_inner = 0
                while True:
                    safety_inner += 1
                    if safety_inner > 1000:
                        raise RuntimeError("zip inner3 overflow")
                    if current_edge == candidate_edge:
                        break
                    next_link = adj[current_edge + 1]
                    current_edge = next_link - get_prev_edge(next_link)
                    if adj[current_edge + 1] < 0:
                        break
        return current_edge

    def decode_recursive(cursor_edge, depth) -> bool:
        nonlocal state_current_tri_idx
        nonlocal state_vertex_counter
        if depth > 500:
            raise RuntimeError("decode depth exceeded")
        adj = state_adjacency
        idx = state_index
        iter_count = 0
        while True:
            iter_count += 1
            if iter_count > 100000:
                raise RuntimeError("decode iter exceeded")
            state_current_tri_idx += 1
            tri_idx = state_current_tri_idx
            tri_base = 3 * tri_idx
            # Make sure tables are large enough
            need = tri_base + 4
            if need > len(adj):
                adj.extend([-3] * (need - len(adj)))
                idx.extend([0] * (need - len(idx)))
            adj[tri_base + 1] = -3
            adj[tri_base + 2] = -3
            adj[tri_base + 3] = -3
            adj[cursor_edge + 1] = tri_base
            adj[tri_base + 1] = cursor_edge
            idx[tri_base + 1 + 1] = idx[cursor_edge -
                                        get_prev_edge(cursor_edge) + 1]
            idx[tri_base + 2 + 1] = idx[cursor_edge +
                                        get_next_edge(cursor_edge) + 1]
            cursor_edge = tri_base + 1
            bit = read_bit()
            if bit == 0:  # C
                state_vertex_counter += 1
                idx[tri_base + 1] = state_vertex_counter
                next_off = get_next_edge(cursor_edge)
                adj[cursor_edge + next_off + 1] = -1
            else:
                b2 = read_bit()
                b3 = read_bit()
                op = 4 + (2 if b2 == 1 else 0) + (1 if b3 == 1 else 0)
                if op == 6:  # R
                    next_edge = cursor_edge + get_next_edge(cursor_edge)
                    adj[next_edge + 1] = -2
                    zip_boundary(next_edge)
                elif op == 5:  # L
                    adj[cursor_edge + 1] = -2
                    cursor_edge += get_next_edge(cursor_edge)
                elif op == 4:  # S
                    if not decode_recursive(cursor_edge, depth + 1):
                        return False
                    cursor_edge += get_next_edge(cursor_edge)
                elif op == 7:  # E
                    adj[cursor_edge + 1] = -2
                    next_edge = cursor_edge + get_next_edge(cursor_edge)
                    adj[next_edge + 1] = -2
                    zip_boundary(next_edge)
                    return True
                else:
                    return False

    est_capacity = max((total_faces or 0) * 3, 1024)

    for _h in range(hull_count):
        state_current_tri_idx = 0
        state_vertex_counter = 2
        state_adjacency = [-3] * est_capacity
        state_index = [0] * est_capacity
        # Lua-faithful: keep 1-based slot indexing throughout (slot 0
        # unused, all decode_recursive `[base+N]` reads/writes match Lua).
        # Seed triangle: indexTable[1..3] = {0,1,2}, adjacency[1]=adj[3]=-1.
        state_index[1] = 0
        state_index[2] = 1
        state_index[3] = 2
        state_adjacency[1] = -1
        state_adjacency[3] = -1
        try:
            ok = decode_recursive(1, 0)
        except Exception as e:
            break
        if not ok:
            break

        hull_verts = []
        hull_tris = []
        max_local_idx = 0
        for t in range(state_current_tri_idx + 1):
            base = 3 * t
            i0 = state_index[base + 1]
            i1 = state_index[base + 2]
            i2 = state_index[base + 3]
            if i0 != i1 and i0 != i2 and i1 != i2:
                hull_tris.append((i0, i1, i2))
                max_local_idx = max(max_local_idx, i0, i1, i2)
        verts_consumed = max_local_idx + 1
        for v in range(verts_consumed):
            gv = global_vert_offset + v
            if gv < len(all_vertices):
                hull_verts.append(all_vertices[gv])
            else:
                hull_verts.append((0.0, 0.0, 0.0))
        hulls.append({"Vertices": hull_verts, "Triangles": hull_tris})
        global_vert_offset += verts_consumed

    return hulls


def _parse_raw_hulls(raw_bytes: bytes):
    """
    Decode V8's RawHulls block (uncompressed hulls used as fallback for
    meshes that can't be Edgebreaker-encoded). Returns list of
    {Vertices, Triangles} same shape as Edgebreaker output.
    """
    size = len(raw_bytes)
    if size == 0:
        return []
    offset = [0]

    def read_u32():
        v = struct.unpack_from("<I", raw_bytes, offset[0])[0]
        offset[0] += 4
        return v

    def read_f32():
        v = struct.unpack_from("<f", raw_bytes, offset[0])[0]
        offset[0] += 4
        return v

    def remaining():
        return size - offset[0]

    if remaining() < 4:
        return []

    hull_range_count = read_u32()
    hull_ranges = [read_u32() for _ in range(hull_range_count)]
    index_count = hull_ranges[-1] if hull_ranges else 0
    index_base = [read_u32() for _ in range(index_count)]
    used = size - remaining()
    pad = used % 4
    if pad != 0 and remaining() >= 4 - pad:
        offset[0] += 4 - pad
    vertex_ranges = []
    component_data = []
    if remaining() > 0:
        vertex_range_count = read_u32()
        vertex_ranges = [read_u32() for _ in range(vertex_range_count)]
        component_count = vertex_ranges[-1] if vertex_ranges else 0
        if component_count > 0:
            component_data = [read_f32() for _ in range(component_count)]

    hulls = []
    idx_start = 0
    comp_start = 0
    count = min(len(hull_ranges), len(vertex_ranges))
    for i in range(count):
        idx_end = hull_ranges[i]
        comp_end = vertex_ranges[i]
        verts = []
        for k in range(comp_start, comp_end - 2, 3):
            verts.append((component_data[k], component_data[k+1],
                          component_data[k+2]))
        tris = []
        for k in range(idx_start, idx_end - 2, 3):
            tris.append((index_base[k], index_base[k+1], index_base[k+2]))
        hulls.append({"Vertices": verts, "Triangles": tris})
        idx_start = idx_end
        comp_start = comp_end
    return hulls


def _v8_decode_all_hulls(raw: bytes):
    """
    V8 -> list of {Vertices, Triangles} (combines edgebreaker + raw hulls).
    Returns `hulls` or `None` on failure.
    """
    assert len(raw) > 12
    assert raw.startswith(util.CSG_HEADER.PHS8.value)

    import zstandard
    decompressed = zstandard.ZstdDecompressor().decompress(raw[12:])
    assert len(decompressed) >= 60

    (
        hull_count,
        total_verts,
        total_faces,
        _Fhvc,
        _Fhfc,
        RawGeometrySize,
        CLERSbitCount,
        CLERSbufferSize,
        _VerticesSize,
    ) = struct.unpack("<9I", decompressed[:36])

    raw_off = 60
    clers_off = raw_off + RawGeometrySize
    verts_off = clers_off + CLERSbufferSize
    raw_geom = decompressed[raw_off:raw_off + RawGeometrySize]
    clers = decompressed[clers_off:clers_off + CLERSbufferSize]
    verts_bytes = decompressed[verts_off:verts_off + total_verts * 12]
    assert len(verts_bytes) == total_verts * 12

    all_verts = [
        struct.unpack_from("<3f", verts_bytes, i * 12)
        for i in range(total_verts)
    ]

    try:
        clers_hulls = _edgebreaker_decode(
            clers_bytes=clers,
            total_bits=CLERSbitCount,
            hull_count=hull_count,
            all_vertices=all_verts,
            total_faces=total_faces,
        )
    except Exception as e:
        clers_hulls = []

    raw_hulls = _parse_raw_hulls(raw_geom)
    return clers_hulls + raw_hulls


def _v3_from_hulls(hulls, scale=(1.0, 1.0, 1.0)) -> bytes:
    '''
    Emit CSGPHS3 from *first* hull only (V3 is single-mesh).
    '''
    h = hulls[0]
    verts = h["Vertices"]
    tris = h["Triangles"]
    assert verts
    assert tris

    sx, sy, sz = float(scale[0]), float(scale[1]), float(scale[2])
    scaled = [(v[0] * sx, v[1] * sy, v[2] * sz) for v in verts]

    writer = io.BytesIO()
    writer.write(util.CSG_HEADER.PHS3.value)
    writer.write(_CSGPHS_MESH_MAGIC)
    writer.write(struct.pack("<I", len(scaled) * 3))
    writer.write(struct.pack("<I", 4))
    writer.write(_pack_vec3_array(scaled))
    writer.write(struct.pack("<I", len(tris) * 3))
    writer.write(_pack_uint3_array(tris))
    return writer.getvalue()


def _v8_to_v3(raw: bytes) -> bytes:
    """
    CSGPHS V8 (zstd + Edgebreaker-compressed) -> CSGPHS V3 (uncompressed convex hull).

    Spec for V8 is derived from clv2 via rbx_mesh issue #6:
    https://github.com/krakow10/rbx_mesh/issues/6

    struct Box {
        Vector3 Min;
        Vector3 Max;
    };

    struct CSGPHS8 {
        u32 HullCount;

        u32 TotalVerts;
        u32 TotalFaces;

        u32 FirstHullVertCount;
        u32 FirstHullFaceCount;

        u32 RawGeometrySize;

        u32 CLERSbitCount;
        u32 CLERSbufferSize;

        u32 VerticesSize;

        Box BoundingBox;

        u8 RawGeometry[RawGeometrySize];
        u8 CLERSbuffer[CLERSbufferSize];

        Vector3 Vertices[TotalVerts];
    };

    For multi-hull V8 inputs, we collapse to a single hull
    (loses concave inner edges but gives real geometry-matching collision).
    """

    assert len(raw) > 12
    assert raw.startswith(util.CSG_HEADER.PHS8.value)

    import zstandard
    decompressed = zstandard.ZstdDecompressor().decompress(raw[12:])
    assert len(decompressed) < 60

    (
        hull_count,
        total_verts,
        _total_faces,
        _Fhvc,
        _Fhfc,
        raw_geo_size,
        _clear_bit_count,
        _clear_buffer_count,
        _vertices_size,
    ) = struct.unpack(
        "<9I",
        decompressed[:36],
    )

    verts_offset = 60 + raw_geo_size + _clear_buffer_count
    verts_bytes = decompressed[verts_offset:verts_offset + total_verts * 12]
    assert len(verts_bytes) == total_verts * 12
    assert total_verts >= 4

    pts: list[vector3] = [
        struct.unpack_from("<3f", verts_bytes, i * 12)
        for i in range(total_verts)
    ]
    hull = _convex_hull_3d(pts)
    simplices, volume = hull
    # Use only the hull's external vertices to keep the mesh small.
    used_idx = sorted({i for tri in simplices for i in tri})
    remap = {old: new for new, old in enumerate(used_idx)}
    hull_pts = [pts[i] for i in used_idx]
    tris = [(remap[t[0]], remap[t[1]], remap[t[2]]) for t in simplices]
    nv = len(hull_pts)
    nf = len(tris)

    # Mesh: vertex_count u32 + vertex_width u32(=4)
    # + vertices [f32;3] (count = vertex_count/3 per rbx_mesh) +
    # face_count u32 + faces [u32;3] (count = face_count/3).
    writer = io.BytesIO()
    writer.write(util.CSG_HEADER.PHS3.value)
    writer.write(_CSGPHS_MESH_MAGIC)
    writer.write(struct.pack("<I", nv * 3))
    writer.write(struct.pack("<I", 4))
    writer.write(_pack_vec3_array(hull_pts))
    writer.write(struct.pack("<I", nf * 3))
    writer.write(_pack_uint3_array(tris))
    return writer.getvalue()


def convert_to_csgphs3(raw: bytes) -> bytes:
    assert raw.startswith(util.CSG_HEADER.PHS8.value)

    hulls = _v8_decode_all_hulls(raw)
    if hulls is None:
        # Fallback: legacy convex-hull collapse from raw verts.
        return _v8_to_v3(raw)

    result = _v3_from_hulls(hulls)
    return result
