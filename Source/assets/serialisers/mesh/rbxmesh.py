"""
    https://github.com/PrintedScript/RBXMesh/blob/main/RBXMesh.py
    Python Library for reading and writing Roblox mesh files.
    Written by something.else on 21/9/2023

    Supported meshes up to version 7.
    Mesh Format documentation by MaximumADHD: https://devforum.roblox.com/t/roblox-mesh-format/326114

    v6/v7 chunked meshes are read and converted to v2.00 format, or v4.00 if bone data exists.
    v4.01 meshes are converted to v4.00.
    Draco-compressed COREMESH chunks (version 2) require the DracoPy package:
        pip install DracoPy
"""

import os
import struct
import tempfile
from collections import OrderedDict
from dataclasses import dataclass
import sys
from typing import override


def debug_print(message: str) -> None:
    if __name__ == "__main__":
        print(message)


"""
struct FileMeshVertexNormalTexture3d
{
    float vx,vy,vz;
    float nx,ny,nz;
    float tu,tv;

    signed char tx, ty, tz, ts;
    unsigned char  r, g, b, a;
};
"""


@dataclass
class FileMeshVertexNormalTexture3d:
    vx: float
    vy: float
    vz: float
    nx: float
    ny: float
    nz: float
    tu: float
    tv: float
    tx: int
    ty: int
    tz: int
    ts: int
    r: int
    g: int
    b: int
    a: int

    def read_data(self, data: bytes):
        if len(data) < 40:
            raise Exception(
                f"FileMeshVertexNormalTexture3d.read_data: data is too short ({len(data)} bytes)")

        self.vx = struct.unpack("<f", data[0:4])[0]
        self.vy = struct.unpack("<f", data[4:8])[0]
        self.vz = struct.unpack("<f", data[8:12])[0]
        self.nx = struct.unpack("<f", data[12:16])[0]
        self.ny = struct.unpack("<f", data[16:20])[0]
        self.nz = struct.unpack("<f", data[20:24])[0]
        self.tu = struct.unpack("<f", data[24:28])[0]
        self.tv = struct.unpack("<f", data[28:32])[0]
        self.tx = int.from_bytes(data[32:33], "little")
        self.ty = int.from_bytes(data[33:34], "little")
        self.tz = int.from_bytes(data[34:35], "little")
        self.ts = int.from_bytes(data[35:36], "little")
        self.r = int.from_bytes(data[36:37], "little")
        self.g = int.from_bytes(data[37:38], "little")
        self.b = int.from_bytes(data[38:39], "little")
        self.a = int.from_bytes(data[39:40], "little")

    def export_data(self) -> bytes:
        return bytes(b''.join([
            struct.pack("<f", self.vx),
            struct.pack("<f", self.vy),
            struct.pack("<f", self.vz),
            struct.pack("<f", self.nx),
            struct.pack("<f", self.ny),
            struct.pack("<f", self.nz),
            struct.pack("<f", self.tu),
            struct.pack("<f", self.tv),
            self.tx.to_bytes(1, "little"),
            self.ty.to_bytes(1, "little"),
            self.tz.to_bytes(1, "little"),
            self.ts.to_bytes(1, "little"),
            self.r.to_bytes(1, "little"),
            self.g.to_bytes(1, "little"),
            self.b.to_bytes(1, "little"),
            self.a.to_bytes(1, "little"),
        ]))


"""
struct FileMeshVertexNormalTexture3dNoRGBA
{
    float vx, vy, vz;
    float nx, ny, nz;
    float tu, tv;

    signed char tx, ty, tz, ts;
};
"""


@dataclass
class FileMeshVertexNormalTexture3dNoRGBA:
    vx: float
    vy: float
    vz: float
    nx: float
    ny: float
    nz: float
    tu: float
    tv: float
    tx: int
    ty: int
    tz: int
    ts: int

    def read_data(self, data: bytes):
        if len(data) < 36:
            raise Exception(
                f"FileMeshVertexNormalTexture3dNoRGBA.read_data: data is too short ({len(data)} bytes)")

        self.vx = struct.unpack("<f", data[0:4])[0]
        self.vy = struct.unpack("<f", data[4:8])[0]
        self.vz = struct.unpack("<f", data[8:12])[0]
        self.nx = struct.unpack("<f", data[12:16])[0]
        self.ny = struct.unpack("<f", data[16:20])[0]
        self.nz = struct.unpack("<f", data[20:24])[0]
        self.tu = struct.unpack("<f", data[24:28])[0]
        self.tv = struct.unpack("<f", data[28:32])[0]
        self.tx = int.from_bytes(data[32:33], "little")
        self.ty = int.from_bytes(data[33:34], "little")
        self.tz = int.from_bytes(data[34:35], "little")
        self.ts = int.from_bytes(data[35:36], "little")

    def export_data(self) -> bytes:
        return bytes(b''.join([
            struct.pack("<f", self.vx),
            struct.pack("<f", self.vy),
            struct.pack("<f", self.vz),
            struct.pack("<f", self.nx),
            struct.pack("<f", self.ny),
            struct.pack("<f", self.nz),
            struct.pack("<f", self.tu),
            struct.pack("<f", self.tv),
            self.tx.to_bytes(1, "little"),
            self.ty.to_bytes(1, "little"),
            self.tz.to_bytes(1, "little"),
            self.ts.to_bytes(1, "little"),
        ]))


"""
struct FileMeshFace
{
    unsigned int a;
    unsigned int b;
    unsigned int c;
};
"""


@dataclass
class FileMeshFace:
    a: int
    b: int
    c: int

    def read_data(self, data: bytes):
        if len(data) < 12:
            raise Exception(
                f"FileMeshFace.read_data: data is too short ({len(data)} bytes)")

        self.a = int.from_bytes(data[0:4], "little")
        self.b = int.from_bytes(data[4:8], "little")
        self.c = int.from_bytes(data[8:12], "little")

    def export_data(self) -> bytes:
        return bytes(b''.join([
            self.a.to_bytes(4, "little"),
            self.b.to_bytes(4, "little"),
            self.c.to_bytes(4, "little"),
        ]))


"""
struct FileMeshHeader
{
    unsigned short cbSize;
    unsigned char cbVerticesStride;
    unsigned char cbFaceStride;

    unsigned int num_vertices;
    unsigned int num_faces;
};
"""


@dataclass
class FileMeshHeader:
    cbSize: int
    cbVerticesStride: int
    cbFaceStride: int
    num_vertices: int
    num_faces: int

    def read_data(self, data: bytes):
        if len(data) < 12:
            raise Exception(
                f"FileMeshHeader.read_data: data is too short ({len(data)} bytes)")

        self.cbSize = int.from_bytes(data[0:2], "little")
        if self.cbSize != 12:
            raise Exception(
                f"FileMeshHeader.read_data: invalid cbSize ({self.cbSize})")
        self.cbVerticesStride = int.from_bytes(data[2:3], "little")
        self.cbFaceStride = int.from_bytes(data[3:4], "little")
        self.num_vertices = int.from_bytes(data[4:8], "little")
        self.num_faces = int.from_bytes(data[8:12], "little")

    def export_data(self) -> bytes:
        return bytes(b''.join([
            self.cbSize.to_bytes(2, "little"),
            self.cbVerticesStride.to_bytes(1, "little"),
            self.cbFaceStride.to_bytes(1, "little"),
            self.num_vertices.to_bytes(4, "little"),
            self.num_faces.to_bytes(4, "little"),
        ]))

    @override
    def __str__(self) -> str:
        return f"FileMeshHeader(cbSize={self.cbSize}, cbVerticesStride={self.cbVerticesStride}, cbFaceStride={self.cbFaceStride}, num_vertices={self.num_vertices}, num_faces={self.num_faces})"

    @override
    def __repr__(self) -> str:
        return str(self)


"""
struct FileMeshHeaderV3
{
    unsigned short cbSize;
    unsigned char cbVerticesStride;
    unsigned char cbFaceStride;
    unsigned short sizeof_LOD;

    unsigned short numLODs;
    unsigned int num_vertices;
    unsigned int num_faces;
};
"""


@dataclass
class FileMeshHeaderV3:
    cbSize: int
    cbVerticesStride: int
    cbFaceStride: int
    sizeof_LOD: int
    numLODs: int
    num_vertices: int
    num_faces: int

    def read_data(self, data: bytes):
        if len(data) < 16:
            raise Exception(
                f"FileMeshHeaderV3.read_data: data is too short ({len(data)} bytes)")

        self.cbSize = int.from_bytes(data[0:2], "little")
        if self.cbSize != 16:
            raise Exception(
                f"FileMeshHeaderV3.read_data: invalid cbSize ({self.cbSize})")
        self.cbVerticesStride = int.from_bytes(data[2:3], "little")
        self.cbFaceStride = int.from_bytes(data[3:4], "little")
        self.sizeof_LOD = int.from_bytes(data[4:6], "little")
        self.numLODs = int.from_bytes(data[6:8], "little")
        self.num_vertices = int.from_bytes(data[8:12], "little")
        self.num_faces = int.from_bytes(data[12:16], "little")

    def export_data(self) -> bytes:
        return bytes(b''.join([
            self.cbSize.to_bytes(2, "little"),
            self.cbVerticesStride.to_bytes(1, "little"),
            self.cbFaceStride.to_bytes(1, "little"),
            self.sizeof_LOD.to_bytes(2, "little"),
            self.numLODs.to_bytes(2, "little"),
            self.num_vertices.to_bytes(4, "little"),
            self.num_faces.to_bytes(4, "little"),
        ]))


"""
struct FileMeshHeaderV4
{
    unsigned short sizeof_MeshHeader;
    unsigned short lodType;

    unsigned int numVerts;
    unsigned int numFaces;

    unsigned short numLODs;
    unsigned short numBones;

    unsigned int sizeof_boneNamesBuffer;
    unsigned short numSubsets;

    unsigned char numHighQualityLODs;
    unsigned char unused;
};
"""


@dataclass
class FileMeshHeaderV4:
    sizeof_MeshHeader: int
    lodType: int
    numVerts: int
    numFaces: int
    numLODs: int
    numBones: int
    sizeof_boneNamesBuffer: int
    numSubsets: int
    numHighQualityLODs: int
    unused: int

    def read_data(self, data: bytes):
        if len(data) < 24:
            raise Exception(
                f"FileMeshHeaderV4.read_data: data is too short ({len(data)} bytes)")

        self.sizeof_MeshHeader = int.from_bytes(data[0:2], "little")
        if self.sizeof_MeshHeader != 24:
            raise Exception(
                "FileMeshHeaderV4.read_data: invalid sizeof_MeshHeader (%d)" %
                (self.sizeof_MeshHeader)
            )
        self.lodType = int.from_bytes(data[2:4], "little")
        self.numVerts = int.from_bytes(data[4:8], "little")
        self.numFaces = int.from_bytes(data[8:12], "little")
        self.numLODs = int.from_bytes(data[12:14], "little")
        self.numBones = int.from_bytes(data[14:16], "little")
        self.sizeof_boneNamesBuffer = int.from_bytes(data[16:20], "little")
        self.numSubsets = int.from_bytes(data[20:22], "little")
        self.numHighQualityLODs = int.from_bytes(data[22:23], "little")
        self.unused = int.from_bytes(data[23:24], "little")

    def export_data(self) -> bytes:
        return bytes(b''.join([
            self.sizeof_MeshHeader.to_bytes(2, "little"),
            self.lodType.to_bytes(2, "little"),
            self.numVerts.to_bytes(4, "little"),
            self.numFaces.to_bytes(4, "little"),
            self.numLODs.to_bytes(2, "little"),
            self.numBones.to_bytes(2, "little"),
            self.sizeof_boneNamesBuffer.to_bytes(4, "little"),
            self.numSubsets.to_bytes(2, "little"),
            self.numHighQualityLODs.to_bytes(1, "little"),
            self.unused.to_bytes(1, "little"),
        ]))


"""
struct Envelope
{
    unsigned char bones[4];
    unsigned char weights[4];
};
"""


@dataclass
class Envelope:
    bones: list[int]
    weights: list[int]

    def read_data(self, data: bytes):
        if len(data) < 8:
            raise Exception(
                f"Envelope.read_data: data is too short ({len(data)} bytes)")

        for i in range(0, 4):
            self.bones.append(int.from_bytes(data[i+0:i+1], "little"))
            self.weights.append(int.from_bytes(data[i+4:i+5], "little"))

    def export_data(self) -> bytes:
        return bytes(b''.join([
            self.bones[0].to_bytes(1, "little") +
            self.bones[1].to_bytes(1, "little") +
            self.bones[2].to_bytes(1, "little") +
            self.bones[3].to_bytes(1, "little") +
            self.weights[0].to_bytes(1, "little") +
            self.weights[1].to_bytes(1, "little") +
            self.weights[2].to_bytes(1, "little") +
            self.weights[3].to_bytes(1, "little")
        ]))


"""
struct Bone
{
    unsigned int boneNameIndex;
    unsigned short parentIndex;
    unsigned short lodParentIndex;
    float culling;

    float r00, r01, r02;
    float r10, r11, r12;
    float r20, r21, r22;

    float x, y, z;
};
"""


@dataclass
class Bone:
    boneNameIndex: int
    parentIndex: int
    lodParentIndex: int
    culling: float
    r00: float
    r01: float
    r02: float
    r10: float
    r11: float
    r12: float
    r20: float
    r21: float
    r22: float
    x: float
    y: float
    z: float

    def read_data(self, data: bytes):
        if len(data) < 60:
            raise Exception(
                f"Bone.read_data: data is too short ({len(data)} bytes)")

        self.boneNameIndex = int.from_bytes(data[0:4], "little")
        self.parentIndex = int.from_bytes(data[4:6], "little")
        self.lodParentIndex = int.from_bytes(data[6:8], "little")
        self.culling = struct.unpack("<f", data[8:12])[0]
        self.r00 = struct.unpack("<f", data[12:16])[0]
        self.r01 = struct.unpack("<f", data[16:20])[0]
        self.r02 = struct.unpack("<f", data[20:24])[0]
        self.r10 = struct.unpack("<f", data[24:28])[0]
        self.r11 = struct.unpack("<f", data[28:32])[0]
        self.r12 = struct.unpack("<f", data[32:36])[0]
        self.r20 = struct.unpack("<f", data[36:40])[0]
        self.r21 = struct.unpack("<f", data[40:44])[0]
        self.r22 = struct.unpack("<f", data[44:48])[0]
        self.x = struct.unpack("<f", data[48:52])[0]
        self.y = struct.unpack("<f", data[52:56])[0]
        self.z = struct.unpack("<f", data[56:60])[0]

    def export_data(self) -> bytes:
        return bytes(b''.join([
            self.boneNameIndex.to_bytes(4, "little"),
            self.parentIndex.to_bytes(2, "little"),
            self.lodParentIndex.to_bytes(2, "little"),
            struct.pack("<f", self.culling),
            struct.pack("<f", self.r00),
            struct.pack("<f", self.r01),
            struct.pack("<f", self.r02),
            struct.pack("<f", self.r10),
            struct.pack("<f", self.r11),
            struct.pack("<f", self.r12),
            struct.pack("<f", self.r20),
            struct.pack("<f", self.r21),
            struct.pack("<f", self.r22),
            struct.pack("<f", self.x),
            struct.pack("<f", self.y),
            struct.pack("<f", self.z),
        ]))


"""
struct MeshSubset
{
    unsigned int facesBegin;
    unsigned int facesLength;

    unsigned int vertsBegin;
    unsigned int vertsLength;

    unsigned int numBoneIndicies;
    unsigned short boneIndicies[26];
};
"""


@dataclass
class MeshSubset:
    facesBegin: int
    facesLength: int
    vertsBegin: int
    vertsLength: int
    numBoneIndicies: int
    boneIndicies: list[int]

    def read_data(self, data: bytes):
        if len(data) < 72:
            raise Exception(
                f"MeshSubset.read_data: data is too short ({len(data)} bytes)")

        self.facesBegin = int.from_bytes(data[0:4], "little")
        self.facesLength = int.from_bytes(data[4:8], "little")
        self.vertsBegin = int.from_bytes(data[8:12], "little")
        self.vertsLength = int.from_bytes(data[12:16], "little")
        self.numBoneIndicies = int.from_bytes(data[16:20], "little")
        for i in range(0, 26):
            self.boneIndicies.append(int.from_bytes(data[20 + i*2 : 22 + i*2], "little"))

    def export_data(self) -> bytes:
        subsetData: bytes = bytes(b''.join([
            self.facesBegin.to_bytes(4, "little"),
            self.facesLength.to_bytes(4, "little"),
            self.vertsBegin.to_bytes(4, "little"),
            self.vertsLength.to_bytes(4, "little"),
            self.numBoneIndicies.to_bytes(4, "little"),
        ]))
        for i in range(0, 26):
            subsetData += self.boneIndicies[i].to_bytes(2, "little")

        return subsetData


"""
struct FileMeshHeaderV5
{
    unsigned short sizeof_MeshHeader;
    unsigned short lodType;

    unsigned int numVerts;
    unsigned int numFaces;

    unsigned short numLODs;
    unsigned short numBones;

    unsigned int sizeof_boneNamesBuffer;
    unsigned short numSubsets;

    unsigned char numHighQualityLODs;
    unsigned char unusedPadding;

    unsigned int facsDataFormat;
    unsigned int facsDataSize;
};
"""


@dataclass
class FileMeshHeaderV5:
    sizeof_MeshHeader: int
    lodType: int
    numVerts: int
    numFaces: int
    numLODs: int
    numBones: int
    sizeof_boneNamesBuffer: int
    numSubsets: int
    numHighQualityLODs: int
    unusedPadding: int
    facsDataFormat: int
    facsDataSize: int

    def read_data(self, data: bytes):
        if len(data) < 32:
            raise Exception(
                f"FileMeshHeaderV5.read_data: data is too short ({len(data)} bytes)")

        self.sizeof_MeshHeader = int.from_bytes(data[0:2], "little")
        if self.sizeof_MeshHeader != 32:
            raise Exception(
                "FileMeshHeaderV5.read_data: invalid sizeof_MeshHeader (%d)" %
                (self.sizeof_MeshHeader)
            )
        self.lodType = int.from_bytes(data[2:4], "little")
        self.numVerts = int.from_bytes(data[4:8], "little")
        self.numFaces = int.from_bytes(data[8:12], "little")
        self.numLODs = int.from_bytes(data[12:14], "little")
        self.numBones = int.from_bytes(data[14:16], "little")
        self.sizeof_boneNamesBuffer = int.from_bytes(data[16:20], "little")
        self.numSubsets = int.from_bytes(data[20:22], "little")
        self.numHighQualityLODs = int.from_bytes(data[22:23], "little")
        self.unusedPadding = int.from_bytes(data[23:24], "little")
        self.facsDataFormat = int.from_bytes(data[24:28], "little")
        self.facsDataSize = int.from_bytes(data[28:32], "little")

    def export_data(self) -> bytes:
        return bytes(b''.join([
            self.sizeof_MeshHeader.to_bytes(2, "little"),
            self.lodType.to_bytes(2, "little"),
            self.numVerts.to_bytes(4, "little"),
            self.numFaces.to_bytes(4, "little"),
            self.numLODs.to_bytes(2, "little"),
            self.numBones.to_bytes(2, "little"),
            self.sizeof_boneNamesBuffer.to_bytes(4, "little"),
            self.numSubsets.to_bytes(2, "little"),
            self.numHighQualityLODs.to_bytes(1, "little"),
            self.unusedPadding.to_bytes(1, "little"),
            self.facsDataFormat.to_bytes(4, "little"),
            self.facsDataSize.to_bytes(4, "little"),
        ]))


@dataclass
class FileMeshData:
    vnts: list[
        FileMeshVertexNormalTexture3d |
        FileMeshVertexNormalTexture3dNoRGBA
    ]
    faces: list[FileMeshFace]
    header: FileMeshHeader | FileMeshHeaderV3 | FileMeshHeaderV4 | FileMeshHeaderV5
    LODs: list[int]
    bones: list[Bone]
    boneNames: str
    meshSubsets: list[MeshSubset]
    full_faces: list[FileMeshFace]
    envelopes: list[Envelope]


def read_data(data: bytes, offset: int, size: int) -> bytes:
    """Reads a string of data from a given offset and size."""

    if len(data) < offset + size:
        raise Exception(
            f"read_data: offset is out of bounds (offset={offset}, size={size})")
    return data[offset:offset+size]


def get_mesh_version(data: bytes) -> str:
    """Gets the version of the mesh file. Throws an exception if the version is not supported."""

    if len(data) < 12:
        raise Exception(
            f"get_mesh_version: data is too short ({len(data)} bytes)")

    if not data[0:8] == b"version ":
        raise Exception(
            f"get_mesh_version: invalid mesh header ({data[0:8]})")

    return data[8:12].decode('ASCII')


def read_mesh_v1(data_bytes: bytes, offset: int, scale: float = 0.5, invertUV: bool = True) -> FileMeshData:
    data_ascii = data_bytes[offset:].decode("ASCII")

    meshData: FileMeshData = FileMeshData(
        [], [], FileMeshHeader(0, 0, 0, 0, 0), [], [], "", [], [], [],
    )
    numFaces: int = int(data_ascii.split("\n", 1)[0])
    debug_print(f"read_mesh_v1: numFaces={numFaces}")

    # [0.551563,-0.0944613,0.0862401] we need to find every vector3 in the file
    # Each vert has 3 vector3 values so we need to find 3 vector3 values for each vert
    startingIndex = data_ascii.find("[")
    allVectorStrs: list[str] = data_ascii[startingIndex:].split("]")
    allVectors: list[list[float]] = []

    for vecStr in allVectorStrs:
        vector: str = vecStr.strip()
        vector = vector.replace("[", "").replace("]", "")
        if vector == "":
            continue

        vector_floats: list[float] = [float(x) for x in vector.split(",")]

        if len(vector_floats) != 3:
            raise Exception(f"read_mesh_v1: invalid vector3 ({vector})")
        allVectors.append(vector_floats)

    if len(allVectors) != numFaces * 9:
        raise Exception(
            "read_mesh_v1: invalid number of verticies (%d), expected %d" %
            (len(allVectors), numFaces * 9)
        )

    for i in range(0, len(allVectors), 3):
        vertPos: list[float] = allVectors[i]
        vertNorm: list[float] = allVectors[i + 1]
        vertUV: list[float] = allVectors[i + 2]

        meshData.vnts.append(FileMeshVertexNormalTexture3d(
            vertPos[0] * scale, vertPos[1] * scale, vertPos[2] * scale,
            vertNorm[0], vertNorm[1], vertNorm[2],
            # Version 1.0 has the UVs inverted, it was only fixed in 1.1
            vertUV[0], float(
                (1 - vertUV[1]) if invertUV else vertUV[1]), int(vertUV[2]),

            0, 0, 0, 0, 0, 0, 0
        ))

        debug_print(f"read_mesh_v1: vnts[{i // 3}]={meshData.vnts[i // 3]}")

    for i in range(0, numFaces):
        meshData.faces.append(FileMeshFace(i * 3, i * 3 + 1, i * 3 + 2))
        debug_print(f"read_mesh_v1: faces[{i}]={meshData.faces[i]}")

    debug_print(
        "read_mesh_v1: read %d vertices and %d faces successfully" %
        (len(meshData.vnts), len(meshData.faces))
    )
    return meshData


def read_mesh_v2(data: bytes, offset: int) -> FileMeshData:
    meshData: FileMeshData = FileMeshData(
        [], [], FileMeshHeader(0, 0, 0, 0, 0), [], [], "", [], [], [])
    meshHeader: FileMeshHeader = FileMeshHeader(0, 0, 0, 0, 0)
    meshHeader.read_data(read_data(data, offset, 12))
    offset += 12

    debug_print(f"read_mesh_v2: meshHeader={meshHeader}")
    if meshHeader.num_vertices == 0 or meshHeader.num_faces == 0:
        raise Exception(f"read_mesh_v2: empty mesh")
    meshData.header = meshHeader
    isRGBAMissing = meshHeader.cbVerticesStride == 36
    if isRGBAMissing:
        for i in range(0, meshHeader.num_vertices):
            meshData.vnts.append(FileMeshVertexNormalTexture3dNoRGBA(
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
            meshData.vnts[i].read_data(read_data(data, offset + i * 36, 36))

            debug_print(f"read_mesh_v2: vnts[{i}]={meshData.vnts[i]}")
    else:
        for i in range(0, meshHeader.num_vertices):
            meshData.vnts.append(FileMeshVertexNormalTexture3d(
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
            meshData.vnts[i].read_data(read_data(data, offset + i * 40, 40))

            debug_print(f"read_mesh_v2: vnts[{i}]={meshData.vnts[i]}")
    offset += meshHeader.num_vertices * meshHeader.cbVerticesStride

    for i in range(0, meshHeader.num_faces):
        meshData.faces.append(FileMeshFace(0, 0, 0))
        meshData.faces[i].read_data(read_data(data, offset + i * 12, 12))

        debug_print(f"read_mesh_v2: faces[{i}]={meshData.faces[i]}")

    offset += meshHeader.num_faces * meshHeader.cbFaceStride

    if offset != len(data):
        raise Exception(
            "read_mesh_v2: unexpected data at end of file (%d bytes)" %
            (len(data) - offset)
        )

    debug_print(
        "read_mesh_v2: read %d vertices and %d faces successfully" %
        (len(meshData.vnts), len(meshData.faces))
    )
    return meshData


def read_mesh_v3(data: bytes, offset: int) -> FileMeshData:
    meshData: FileMeshData = FileMeshData(
        [], [], FileMeshHeader(0, 0, 0, 0, 0), [], [], "", [], [], [])
    meshHeader: FileMeshHeaderV3 = FileMeshHeaderV3(0, 0, 0, 0, 0, 0, 0)
    meshHeader.read_data(read_data(data, offset, 16))
    offset += 16

    debug_print(f"read_mesh_v3: meshHeader={meshHeader}")
    if meshHeader.num_vertices == 0 or meshHeader.num_faces == 0:
        raise Exception(f"read_mesh_v3: empty mesh")
    meshData.header = meshHeader
    for i in range(0, meshHeader.num_vertices):
        meshData.vnts.append(FileMeshVertexNormalTexture3d(
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
        meshData.vnts[i].read_data(read_data(data, offset + i * 40, 40))

        debug_print(f"read_mesh_v3: vnts[{i}]={meshData.vnts[i]}")
    offset += meshHeader.num_vertices * meshHeader.cbVerticesStride

    for i in range(0, meshHeader.num_faces):
        meshData.faces.append(FileMeshFace(0, 0, 0))
        meshData.faces[i].read_data(read_data(data, offset + i * 12, 12))

        debug_print(f"read_mesh_v3: faces[{i}]={meshData.faces[i]}")
    offset += meshHeader.num_faces * meshHeader.cbFaceStride

    # LODs ( sizeof_LOD [ unsigned int ] * numLODs )
    meshLODs: list[int] = []
    for i in range(0, meshHeader.numLODs):
        meshLODs.append(int.from_bytes(
            read_data(data, offset + i * 4, 4), "little"))
        debug_print(f"read_mesh_v3: meshLODs[{i}]={meshLODs[i]}")
    offset += meshHeader.numLODs * 4

    # We only keep the first LOD in the mesh data
    if len(meshLODs) > 1:
        meshData.full_faces = meshData.faces
        meshData.faces = meshData.faces[0:meshLODs[1]]
        debug_print(
            f"read_mesh_v3: only keeping %d/%d faces" %
            (meshLODs[1], meshHeader.num_faces)
        )
    meshData.LODs = meshLODs

    if offset != len(data):
        raise Exception(
            "read_mesh_v3: unexpected data at end of file (%d bytes)"
            % (len(data) - offset)
        )

    debug_print(
        "read_mesh_v3: read %d vertices and %d faces successfully" %
        (len(meshData.vnts), len(meshData.faces))
    )
    return meshData


def read_mesh_v4(data: bytes, offset: int) -> FileMeshData:
    meshData: FileMeshData = FileMeshData(
        [], [], FileMeshHeader(0, 0, 0, 0, 0), [], [], "", [], [], [],
    )
    meshHeader: FileMeshHeaderV4 = FileMeshHeaderV4(
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    )
    meshHeader.read_data(read_data(data, offset, 24))
    offset += 24

    debug_print(f"read_mesh_v4: meshHeader={meshHeader}")
    if meshHeader.numVerts == 0 or meshHeader.numFaces == 0:
        raise Exception(f"read_mesh_v4: empty mesh")
    meshData.header = meshHeader
    for i in range(0, meshHeader.numVerts):
        meshData.vnts.append(FileMeshVertexNormalTexture3d(
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 127, 127, 127, 127, 127))
        meshData.vnts[i].read_data(read_data(data, offset + i * 40, 40))

        debug_print(f"read_mesh_v4: vnts[{i}]={meshData.vnts[i]}")
    offset += meshHeader.numVerts * 40

    if meshHeader.numBones > 0:
        for i in range(0, meshHeader.numVerts):
            meshData.envelopes.append(Envelope([], []))
            meshData.envelopes[i].read_data(read_data(data, offset + i * 8, 8))

            debug_print(
                "read_mesh_v4: envelopes[%d]=%s" %
                (i, meshData.envelopes[i])
            )
        offset += meshHeader.numVerts * 8

    for i in range(0, meshHeader.numFaces):
        meshData.faces.append(FileMeshFace(0, 0, 0))
        meshData.faces[i].read_data(read_data(data, offset + i * 12, 12))

        debug_print(f"read_mesh_v4: faces[{i}]={meshData.faces[i]}")
    offset += meshHeader.numFaces * 12

    # LODs ( sizeof_LOD [ unsigned int ] * numLODs )
    meshLODs: list[int] = []
    for i in range(0, meshHeader.numLODs):
        meshLODs.append(int.from_bytes(
            read_data(data, offset + i * 4, 4), "little"))
        debug_print(f"read_mesh_v4: meshLODs[{i}]={meshLODs[i]}")
    offset += meshHeader.numLODs * 4

    if len(meshLODs) > 1:
        meshData.full_faces = meshData.faces
        meshData.faces = meshData.faces[0:meshLODs[1]]
        debug_print(
            "read_mesh_v4: only keeping %d/%d faces" %
            (meshLODs[1], meshHeader.numFaces)
        )
    meshData.LODs = meshLODs

    if meshHeader.numBones > 0:
        for i in range(0, meshHeader.numBones):
            meshData.bones.append(
                Bone(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -127, -127, -127, 0, 0))
            meshData.bones[i].read_data(read_data(data, offset + i * 60, 60))

            debug_print(f"read_mesh_v4: bones[{i}]={meshData.bones[i]}")
        offset += meshHeader.numBones * 60

    boneNames: str = read_data(
        data, offset, meshHeader.sizeof_boneNamesBuffer).decode("utf-8")
    meshData.boneNames = boneNames
    offset += meshHeader.sizeof_boneNamesBuffer
    debug_print(f"read_mesh_v4: boneNames={boneNames}")

    meshSubsets: list[MeshSubset] = []
    for i in range(0, meshHeader.numSubsets):
        meshSubsets.append(MeshSubset(0, 0, 0, 0, 0, []))
        meshSubsets[i].read_data(read_data(data, offset + i * 72, 72))

        debug_print(f"read_mesh_v4: meshSubsets[{i}]={meshSubsets[i]}")
    meshData.meshSubsets = meshSubsets
    offset += meshHeader.numSubsets * 72
	
	# offset += meshHeader.unused
    # Note: v4 has no trailing padding block — 'unused' is a 1-byte pad in the
    # header struct itself, not a variable-length data region after the subsets.

    if offset != len(data):
        raise Exception(
            "read_mesh_v4: unexpected data at end of file (%d bytes)" %
            (len(data) - offset)
        )

    debug_print(
        "read_mesh_v4: read {len(meshData.vnts)} vertices and %d faces successfully" %
        (len(meshData.faces))
    )
    return meshData


def read_mesh_v5(data: bytes, offset: int) -> FileMeshData:
    meshData: FileMeshData = FileMeshData(
        [], [], FileMeshHeader(0, 0, 0, 0, 0), [], [], "", [], [], [])
    meshHeader: FileMeshHeaderV5 = FileMeshHeaderV5(
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    meshHeader.read_data(read_data(data, offset, 32))
    offset += 32

    debug_print(f"read_mesh_v5: meshHeader={meshHeader}")
    if meshHeader.numVerts == 0 or meshHeader.numFaces == 0:
        raise Exception(f"read_mesh_v5: empty mesh")
    meshData.header = meshHeader
    for i in range(0, meshHeader.numVerts):
        meshData.vnts.append(FileMeshVertexNormalTexture3d(
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 127, 127, 127, 127, 127))
        meshData.vnts[i].read_data(read_data(data, offset + i * 40, 40))

        debug_print(f"read_mesh_v5: vnts[{i}]={meshData.vnts[i]}")
    offset += meshHeader.numVerts * 40

    if meshHeader.numBones > 0:
        for i in range(0, meshHeader.numVerts):
            env = Envelope([], [])
            env.read_data(read_data(data, offset + i * 8, 8))
            meshData.envelopes.append(env)
        offset += meshHeader.numVerts * 8

    for i in range(0, meshHeader.numFaces):
        meshData.faces.append(FileMeshFace(0, 0, 0))
        meshData.faces[i].read_data(read_data(data, offset + i * 12, 12))

        debug_print(f"read_mesh_v5: faces[{i}]={meshData.faces[i]}")
    offset += meshHeader.numFaces * 12

    # LODs ( sizeof_LOD [ unsigned int ] * numLODs )
    meshLODs: list[int] = []
    for i in range(0, meshHeader.numLODs):
        meshLODs.append(int.from_bytes(
            read_data(data, offset + i * 4, 4), "little"))
        debug_print(f"read_mesh_v5: meshLODs[{i}]={meshLODs[i]}")
    offset += meshHeader.numLODs * 4

    if len(meshLODs) > 1:
        meshData.full_faces = meshData.faces
        meshData.faces = meshData.faces[0:meshLODs[1]]
        debug_print(
            "read_mesh_v5: only keeping %d/%d faces" %
            (meshLODs[1], meshHeader.numFaces)
        )
    meshData.LODs = meshLODs

    if meshHeader.numBones > 0:
        for i in range(0, meshHeader.numBones):
            meshData.bones.append(
                Bone(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -127, -127, -127, 0, 0))
            meshData.bones[i].read_data(read_data(data, offset + i * 60, 60))

            debug_print(f"read_mesh_v5: bones[{i}]={meshData.bones[i]}")
        offset += meshHeader.numBones * 60

    boneNames: str = read_data(
        data, offset, meshHeader.sizeof_boneNamesBuffer).decode("utf-8")
    meshData.boneNames = boneNames
    offset += meshHeader.sizeof_boneNamesBuffer
    debug_print(f"read_mesh_v5: boneNames={boneNames}")

    meshSubsets: list[MeshSubset] = []
    for i in range(0, meshHeader.numSubsets):
        meshSubsets.append(MeshSubset(0, 0, 0, 0, 0, []))
        meshSubsets[i].read_data(read_data(data, offset + i * 72, 72))

        debug_print(f"read_mesh_v5: meshSubsets[{i}]={meshSubsets[i]}")
    meshData.meshSubsets = meshSubsets
    offset += meshHeader.numSubsets * 72
    offset += meshHeader.unusedPadding

    offset += meshHeader.facsDataSize  # No way I am doing allat

    if offset != len(data):
        raise Exception(
            "read_mesh_v5: unexpected data at end of file (%d bytes)" %
            (len(data) - offset)
        )

    debug_print(
        "read_mesh_v5: read %d vertices and %d faces successfully" %
        (len(meshData.vnts), len(meshData.faces))
    )
    return meshData


def export_mesh_v2(meshData: FileMeshData | None) -> bytes:
    if meshData is None:
        raise Exception(f"export_mesh_v2: meshData is None")
    if len(meshData.vnts) == 0 or len(meshData.faces) == 0:
        raise Exception(f"export_mesh_v2: meshData is empty")

    finalmesh: bytes = b""
    finalmesh += b"version 2.00\n"
    finalmesh += FileMeshHeader(
        12,
        36 if len(meshData.vnts) > 0 and isinstance(
            meshData.vnts[0], FileMeshVertexNormalTexture3dNoRGBA) else 40,
        12,
        len(meshData.vnts),
        len(meshData.faces)
    ).export_data()

    for i in range(0, len(meshData.vnts)):
        finalmesh += meshData.vnts[i].export_data()

    for i in range(0, len(meshData.faces)):
        finalmesh += meshData.faces[i].export_data()

    return finalmesh


def export_mesh_v3(meshData: FileMeshData | None) -> bytes:
    if meshData is None:
        raise Exception(f"export_mesh_v3: meshData is None")
    if len(meshData.vnts) == 0 or len(meshData.faces) == 0:
        raise Exception(f"export_mesh_v3: meshData is empty")

    finalmesh: bytes = b""
    finalmesh += b"version 3.00\n"
    finalmesh += FileMeshHeaderV3(
        16,
        40,
        12,
        4,
        # There has to be at least two LODs ( [0, 1234] ) if not ROBLOX will complain about an empty mesh
        max(len(meshData.LODs), 2),
        len(meshData.vnts),
        len(meshData.full_faces) if len(meshData.LODs) > 1 and len(
            meshData.full_faces) > len(meshData.faces) else len(meshData.faces),
    ).export_data()

    for i in range(0, len(meshData.vnts)):
        finalmesh += meshData.vnts[i].export_data()

    if len(meshData.LODs) > 1 and len(meshData.full_faces) > len(meshData.faces):
        for i in range(0, len(meshData.full_faces)):
            finalmesh += meshData.full_faces[i].export_data()
    else:
        for i in range(0, len(meshData.faces)):
            finalmesh += meshData.faces[i].export_data()

    if len(meshData.LODs) > 1:
        for i in range(0, len(meshData.LODs)):
            finalmesh += meshData.LODs[i].to_bytes(4, "little")
    else:
        finalmesh += (0).to_bytes(4, "little")
        finalmesh += (len(meshData.faces)).to_bytes(4, "little")

    return finalmesh

def export_mesh_v4(meshData: FileMeshData | None) -> bytes:
    """
    Export a FileMeshData as a version 4.00 binary mesh.

    Per the spec (FileMeshHeaderV4):
      ushort sizeof_FileMeshHeaderV4  = 24
      ushort lodType                  = 0 (None)
      uint   numVerts
      uint   numFaces                 (all faces, including every LOD level)
      ushort numLodOffsets
      ushort numBones
      uint   sizeof_boneNames
      ushort numSubsets
      byte   numHighQualityLODs       = 1
      byte   unused                   = 0

    Layout after header:
      FileMeshVertex[numVerts]
      FileMeshSkinning[numVerts]   -- only if numBones > 0
      FileMeshFace[numFaces]
      uint lodOffsets[numLodOffsets]
      FileMeshBone[numBones]
      byte boneNames[sizeof_boneNames]
      FileMeshSubset[numSubsets]
    """
    if meshData is None:
        raise Exception("export_mesh_v4: meshData is None")
    if len(meshData.vnts) == 0 or len(meshData.faces) == 0:
        raise Exception("export_mesh_v4: meshData is empty")

    has_bones   = len(meshData.bones) > 0
    has_lods    = len(meshData.LODs) >= 2
    has_subsets = len(meshData.meshSubsets) > 0

    # Build the bone names buffer.
    # Each name is a null-terminated UTF-8 string; boneNameIndex on each Bone
    # is the byte offset into this buffer where that bone's name starts.
    # We rebuild it from scratch: assign offsets in bone order.
    bone_name_list: list[str] = []
    if has_bones:
        # Try to recover names from the existing boneNames string buffer.
        # boneNames is stored as a single null-delimited string blob.
        raw_names = meshData.boneNames.split("\x00") if meshData.boneNames else []
        # If we have the right count use them, otherwise generate placeholders.
        if len(raw_names) >= len(meshData.bones):
            bone_name_list = raw_names[:len(meshData.bones)]
        else:
            bone_name_list = [f"Bone{i}" for i in range(len(meshData.bones))]

    # Rebuild name buffer and fix boneNameIndex offsets so they're consistent.
    bone_names_buf: bytes = b""
    bone_name_offsets: list[int] = []
    for name in bone_name_list:
        bone_name_offsets.append(len(bone_names_buf))
        bone_names_buf += name.encode("utf-8") + b"\x00"

    # Determine all-faces list (include every LOD level as the spec requires).
    all_faces = meshData.full_faces if (
        has_lods and len(meshData.full_faces) > len(meshData.faces)
    ) else meshData.faces

    # LOD offsets array — must have at least [0, numFaces] per convention.
    if has_lods and len(meshData.LODs) >= 2:
        lod_offsets = meshData.LODs
    else:
        lod_offsets = [0, len(meshData.faces)]

    num_verts   = len(meshData.vnts)
    num_faces   = len(all_faces)
    num_lods    = len(lod_offsets)
    num_bones   = len(meshData.bones)
    num_subsets = len(meshData.meshSubsets)

    finalmesh: bytes = b""
    finalmesh += b"version 4.00\n"

    # --- Header (24 bytes) ---
    finalmesh += FileMeshHeaderV4(
        sizeof_MeshHeader   = 24,
        lodType             = 0,
        numVerts            = num_verts,
        numFaces            = num_faces,
        numLODs             = num_lods,
        numBones            = num_bones,
        sizeof_boneNamesBuffer = len(bone_names_buf),
        numSubsets          = num_subsets,
        numHighQualityLODs  = 1,
        unused              = 0,
    ).export_data()

    # --- Vertices ---
    for vnt in meshData.vnts:
        finalmesh += vnt.export_data()

    # --- Skinning (only when bones are present) ---
    if has_bones:
        if len(meshData.envelopes) == num_verts:
            for env in meshData.envelopes:
                finalmesh += env.export_data()
        else:
            # No envelope data available — write identity skinning (bone 0, full weight).
            identity_env = Envelope([0, 0, 0, 0], [255, 0, 0, 0])
            for _ in range(num_verts):
                finalmesh += identity_env.export_data()

    # --- Faces ---
    for face in all_faces:
        finalmesh += face.export_data()

    # --- LOD offsets ---
    for lod in lod_offsets:
        finalmesh += lod.to_bytes(4, "little")

    # --- Bones (with corrected name offsets) ---
    for i, bone in enumerate(meshData.bones):
        # Patch boneNameIndex to match the buffer we just built.
        patched = Bone(
            boneNameIndex  = bone_name_offsets[i] if i < len(bone_name_offsets) else 0,
            parentIndex    = bone.parentIndex,
            lodParentIndex = bone.lodParentIndex,
            culling        = bone.culling,
            r00 = bone.r00, r01 = bone.r01, r02 = bone.r02,
            r10 = bone.r10, r11 = bone.r11, r12 = bone.r12,
            r20 = bone.r20, r21 = bone.r21, r22 = bone.r22,
            x = bone.x, y = bone.y, z = bone.z,
        )
        finalmesh += patched.export_data()

    # --- Bone names buffer ---
    finalmesh += bone_names_buf

    # --- Subsets ---
    if has_subsets:
        for subset in meshData.meshSubsets:
            # Ensure boneIndicies always has exactly 26 entries (pad with 0xFFFF).
            indices = list(subset.boneIndicies)
            while len(indices) < 26:
                indices.append(0xFFFF)
            padded_subset = MeshSubset(
                facesBegin       = subset.facesBegin,
                facesLength      = subset.facesLength,
                vertsBegin       = subset.vertsBegin,
                vertsLength      = subset.vertsLength,
                numBoneIndicies  = subset.numBoneIndicies,
                boneIndicies     = indices,
            )
            finalmesh += padded_subset.export_data()
    elif has_bones:
        # No subset data but we have bones — write a single catch-all subset
        # that covers all verts/faces, referencing only bone 0.
        catchall_indices = [0] + [0xFFFF] * 25
        catchall = MeshSubset(
            facesBegin      = 0,
            facesLength     = num_faces,
            vertsBegin      = 0,
            vertsLength     = num_verts,
            numBoneIndicies = 1,
            boneIndicies    = catchall_indices,
        )
        finalmesh += catchall.export_data()

    return finalmesh


# ---------------------------------------------------------------------------
# v6 / v7 chunked mesh support
# ---------------------------------------------------------------------------

class _ByteReader:
    """Minimal binary reader helper (mirrors the JS ByteReader used in MeshParser.js)."""

    def __init__(self, data: bytes):
        self._data = data
        self._pos = 0

    def get_index(self) -> int:
        return self._pos

    def get_remaining(self) -> int:
        return len(self._data) - self._pos

    def get_length(self) -> int:
        return len(self._data)

    def jump(self, n: int):
        self._pos += n

    def set_index(self, pos: int):
        self._pos = pos

    def read(self, n: int) -> bytes:
        chunk = self._data[self._pos:self._pos + n]
        if len(chunk) < n:
            raise Exception(f"_ByteReader.read: not enough data (need {n}, have {len(chunk)})")
        self._pos += n
        return chunk

    def string(self, n: int) -> str:
        return self.read(n).decode("latin-1")

    def uint8(self) -> int:
        return struct.unpack("<B", self.read(1))[0]

    def uint16le(self) -> int:
        return struct.unpack("<H", self.read(2))[0]

    def uint32le(self) -> int:
        return struct.unpack("<I", self.read(4))[0]

    def float_le(self) -> float:
        return struct.unpack("<f", self.read(4))[0]

    def array(self, n: int) -> bytes:
        return self.read(n)

    def subarray(self, start: int, end: int) -> bytes:
        return self._data[start:end]

    def index_of(self, byte_val: int, start: int) -> int:
        idx = self._data.index(byte_val, start)
        return idx


def _decode_draco_coremesh(bitstream: bytes):
    """
    Decode a Draco-compressed COREMESH bitstream using DracoPy.
    Returns (vertices, normals, uvs, faces, tangents) as flat lists.
    Attribute unique_id mapping (matches MeshParser.js):
        0 = Position, 1 = Normals, 2 = UVs, 3 = Tangents (uint8), 4 = Colors
    """
    try:
        import DracoPy
    except ImportError:
        raise ImportError(
            "DracoPy is required to decode Draco-compressed v6/v7 meshes.\n"
            "Install it with:  pip install DracoPy"
        )

    mesh_object = DracoPy.decode(bitstream)

    # Index attributes by unique_id for easy lookup
    attr_by_id = {a['unique_id']: a['data'] for a in mesh_object.attributes}

    vertices = list(attr_by_id[0].flatten()) if 0 in attr_by_id else list(mesh_object.points.flatten())
    faces    = list(mesh_object.faces.flatten())

    normals:  list[float] = []
    uvs:      list[float] = []
    tangents: list[int]   = []

    if 1 in attr_by_id:
        normals = list(attr_by_id[1].flatten())

    if 2 in attr_by_id:
        uvs = list(attr_by_id[2].flatten())

    if 3 in attr_by_id:
        # Tangents are uint8 (0-255), stored per-vertex as 4 components
        tangents = [int(v) for v in attr_by_id[3].flatten()]

    num_verts = len(vertices) // 3
    if not normals:
        normals = [0.0, 1.0, 0.0] * num_verts
    if not uvs:
        uvs = [0.0, 0.0] * num_verts
    if not tangents:
        tangents = [127, 127, 127, 0] * num_verts

    return vertices, normals, uvs, faces, tangents


def _parse_coremesh_v1(chunk: _ByteReader):
    """Parse a plain (non-Draco) COREMESH version-1 chunk."""
    num_verts = chunk.uint32le()

    vertices: list[float] = []
    normals:  list[float] = []
    uvs:      list[float] = []
    tangents: list[int]   = []  # raw unsigned bytes: tx, ty, tz, ts per vertex

    for _ in range(num_verts):
        vertices.append(chunk.float_le())
        vertices.append(chunk.float_le())
        vertices.append(chunk.float_le())

        normals.append(chunk.float_le())
        normals.append(chunk.float_le())
        normals.append(chunk.float_le())

        u = chunk.float_le()
        v = chunk.float_le()
        uvs.append(u)
        uvs.append(v)

        # tangent bytes (tx, ty, tz, ts) — read and preserve
        tangents.append(chunk.uint8())
        tangents.append(chunk.uint8())
        tangents.append(chunk.uint8())
        tangents.append(chunk.uint8())

        # RGBA bytes — skip
        chunk.jump(4)

    num_faces = chunk.uint32le()
    faces: list[int] = []
    for _ in range(num_faces):
        faces.append(chunk.uint32le())
        faces.append(chunk.uint32le())
        faces.append(chunk.uint32le())

    return vertices, normals, uvs, faces, tangents


def _parse_coremesh_v2(chunk: _ByteReader):
    """Parse a Draco-compressed COREMESH version-2 chunk. Returns 5-tuple matching v1."""
    bitstream_size = chunk.uint32le()
    bitstream = chunk.array(bitstream_size)
    return _decode_draco_coremesh(bitstream)


def _mesh_data_from_flat(vertices: list[float], normals: list[float],
                         uvs: list[float], faces: list[int],
                         tangents: list[int] = None) -> FileMeshData:
    """
    Convert flat vertex/normal/uv/face/tangent arrays into a FileMeshData.
    All values should be in their final form (no flipping applied here).
    Tangents are 4 raw unsigned bytes per vertex: tx, ty, tz, ts.
    """
    num_verts = len(vertices) // 3
    num_faces = len(faces) // 3

    meshData = FileMeshData([], [], FileMeshHeader(0, 0, 0, 0, 0), [], [], "", [], [], [])

    for i in range(num_verts):
        vx = float(vertices[i * 3])
        vy = float(vertices[i * 3 + 1])
        vz = float(vertices[i * 3 + 2])

        nx = float(normals[i * 3])     if i * 3 + 2 < len(normals) else 0.0
        ny = float(normals[i * 3 + 1]) if i * 3 + 2 < len(normals) else 1.0
        nz = float(normals[i * 3 + 2]) if i * 3 + 2 < len(normals) else 0.0

        tu = float(uvs[i * 2])     if i * 2 + 1 < len(uvs) else 0.0
        tv = float(uvs[i * 2 + 1]) if i * 2 + 1 < len(uvs) else 0.0

        if tangents and i * 4 + 3 < len(tangents):
            tx = int(tangents[i * 4])
            ty = int(tangents[i * 4 + 1])
            tz = int(tangents[i * 4 + 2])
            ts = int(tangents[i * 4 + 3])
        else:
            tx, ty, tz, ts = 0, 0, 255, 127  # fallback

        meshData.vnts.append(
            FileMeshVertexNormalTexture3d(vx, vy, vz, nx, ny, nz, tu, tv,
                                         tx, ty, tz, ts, 255, 255, 255, 255)
        )

    for i in range(num_faces):
        a = int(faces[i * 3])
        b = int(faces[i * 3 + 1])
        c = int(faces[i * 3 + 2])
        meshData.faces.append(FileMeshFace(a, b, c))

    meshData.LODs = [0, num_faces]
    return meshData


def _build_obj_text(vertices: list[float], normals: list[float],
                    uvs: list[float], faces: list[int],
                    lods: list[int]) -> str:
    """
    Produce an OBJ file string from flat arrays.
    Mirrors the JS in extracted_common.js (only the first LOD is used).
    UV V is already un-flipped at this point (we re-flip it via 1-v when
    writing so that the obj_to_roblox round-trip comes out right).
    """
    lines = ["o Mesh"]

    num_verts = len(vertices) // 3
    for i in range(num_verts):
        lines.append(f"v {vertices[i*3]} {vertices[i*3+1]} {vertices[i*3+2]}")

    lines.append("")

    num_normals = len(normals) // 3
    for i in range(num_normals):
        lines.append(f"vn {normals[i*3]} {normals[i*3+1]} {normals[i*3+2]}")

    lines.append("")

    num_uvs = len(uvs) // 2
    for i in range(num_uvs):
        # UVs are already in Roblox-space (V flipped). Write them as-is so
        # _build_unique_vertices' 1-v flip produces the correct final value.
        lines.append(f"vt {uvs[i*2]} {uvs[i*2+1]}")

    lines.append("")

    # Only use first LOD (lods[0]..lods[1])
    lod_start = lods[0] * 3 if len(lods) >= 1 else 0
    lod_end   = lods[1] * 3 if len(lods) >= 2 else len(faces)
    lod_faces = faces[lod_start:lod_end]

    for i in range(0, len(lod_faces), 3):
        a = lod_faces[i]     + 1
        b = lod_faces[i + 1] + 1
        c = lod_faces[i + 2] + 1
        lines.append(f"f {a}/{a}/{a} {b}/{b}/{b} {c}/{c}/{c}")

    return "\n".join(lines)


# --- OBJ -> v2.00 conversion (from obj_to_roblox_mesh.py, inlined) ----------

def _parse_obj_text(obj_text: str):
    """Parse OBJ text and return (positions, normals, uvs, triangles)."""
    positions = []
    normals_list = []
    uvs_list = []
    face_triplets = []

    for line in obj_text.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        parts = line.split()
        if not parts:
            continue
        cmd = parts[0]
        if cmd == 'v':
            positions.append(tuple(map(float, parts[1:4])))
        elif cmd == 'vn':
            normals_list.append(tuple(map(float, parts[1:4])))
        elif cmd == 'vt':
            uvs_list.append(tuple(map(float, parts[1:3])))
        elif cmd == 'f':
            for token in parts[1:]:
                indices = token.split('/')
                vi = int(indices[0]) - 1
                ti = int(indices[1]) - 1 if len(indices) > 1 and indices[1] else None
                ni = int(indices[2]) - 1 if len(indices) > 2 and indices[2] else None
                face_triplets.append((vi, ti, ni))

    triangles = [face_triplets[i:i+3]
                 for i in range(0, len(face_triplets), 3)
                 if len(face_triplets[i:i+3]) == 3]
    return positions, normals_list, uvs_list, triangles


def _build_unique_vertices(positions, normals_list, uvs_list, triangles):
    """Merge OBJ indices into unique vertices (flips V like obj_to_roblox_mesh.py)."""
    vertex_map = OrderedDict()
    vertices = []
    faces_out = []

    for tri in triangles:
        face_indices = []
        for (pi, ti, ni) in tri:
            key = (pi, ti if ti is not None else -1, ni if ni is not None else -1)
            if key not in vertex_map:
                pos  = positions[pi]    if pi < len(positions)    else (0.0, 0.0, 0.0)
                norm = normals_list[ni] if ni is not None and ni < len(normals_list) else (1.0, 0.0, 0.0)
                uv   = uvs_list[ti]     if ti is not None and ti < len(uvs_list)     else (0.0, 0.0)
                uv = (uv[0], 1.0 - uv[1])   # flip V for Roblox
                vertex_map[key] = len(vertices)
                vertices.append((pos, norm, uv))
            face_indices.append(vertex_map[key])
        faces_out.append(tuple(face_indices))

    return vertices, faces_out


def _obj_text_to_mesh_data(obj_text: str) -> FileMeshData:
    """
    Convert OBJ text (as a string) directly to a FileMeshData.
    This is the same pipeline as obj_to_roblox_mesh.py but works in-memory.
    """
    positions, normals_list, uvs_list, triangles = _parse_obj_text(obj_text)
    if not triangles:
        raise Exception("_obj_text_to_mesh_data: no triangles found in OBJ data")

    vertices, faces_out = _build_unique_vertices(positions, normals_list, uvs_list, triangles)

    meshData = FileMeshData([], [], FileMeshHeader(0, 0, 0, 0, 0), [], [], "", [], [], [])

    TANGENT_DEFAULT = 0  # (0,0,-1,1) packed – fine as placeholder
    for (pos, norm, uv) in vertices:
        vnt = FileMeshVertexNormalTexture3d(
            pos[0],  pos[1],  pos[2],
            norm[0], norm[1], norm[2],
            uv[0],   uv[1],
            0, 0, 255, 127,   # tangent bytes (tx, ty, tz, ts)
            255, 255, 255, 255 # RGBA
        )
        meshData.vnts.append(vnt)

    for face in faces_out:
        meshData.faces.append(FileMeshFace(face[0], face[1], face[2]))

    num_faces = len(meshData.faces)
    meshData.LODs = [0, num_faces]
    return meshData


def _parse_skinning_chunk_v1(chunk: _ByteReader):
    """
    Parse a v1 SKINNING chunk per the spec:

        struct FileMesh_SKINNING_v1
        {
            uint numSkinnings;
            FileMeshSkinning skinning[numSkinnings];   // 8 bytes each
            uint numBones;
            FileMeshBone bones[numBones];              // 60 bytes each
            uint nameTableSize;
            byte nameTable[nameTableSize];
            uint numSubsets;
            FileMeshSubset subsets[numSubsets];        // 72 bytes each
        }

    Returns (envelopes, bones, bone_names_raw_bytes, subsets).
    bone_names_raw_bytes is the raw name-table buffer so boneNameIndex offsets
    remain valid when we pass it straight through to export_mesh_v4.
    """
    # --- Envelopes (FileMeshSkinning) ---
    num_skinnings = chunk.uint32le()
    envelopes: list[Envelope] = []
    for _ in range(num_skinnings):
        env = Envelope([], [])
        env.read_data(chunk.array(8))
        envelopes.append(env)

    # --- Bones ---
    num_bones = chunk.uint32le()
    bones: list[Bone] = []
    for _ in range(num_bones):
        bone = Bone(0, 0, 0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        bone.read_data(chunk.array(60))
        bones.append(bone)

    # --- Name table ---
    name_table_size = chunk.uint32le()
    name_table_bytes: bytes = chunk.array(name_table_size)

    # Reconstruct a null-terminated string blob whose byte offsets match
    # boneNameIndex values already embedded in each Bone (no patching needed).
    # We decode for the boneNames string field but keep raw bytes for export.
    try:
        bone_names_str = name_table_bytes.decode("utf-8", errors="replace")
    except Exception:
        bone_names_str = ""

    # --- Subsets ---
    num_subsets = chunk.uint32le()
    subsets: list[MeshSubset] = []
    for _ in range(num_subsets):
        subset = MeshSubset(0, 0, 0, 0, 0, [])
        subset.read_data(chunk.array(72))
        subsets.append(subset)

    return envelopes, bones, bone_names_str, name_table_bytes, subsets


def read_mesh_v6_v7(data: bytes, offset: int, version: str) -> FileMeshData:
    """
    Parse a v6.00, v6.01, v7.00, or v7.01 chunked Roblox mesh.

    Chunks handled:
      COREMESH  — vertices, normals, UVs, tangents, faces (v1 plain or v2 Draco)
      LODS      — LOD face-range offsets
      SKINNING  — bone envelopes, bones, name table, subsets
    
    If a SKINNING chunk with bones is present the FileMeshData will have
    bones/envelopes/subsets populated, making it ready for export_mesh_v4.
    Otherwise it is ready for export_mesh_v2.


    A temporary .obj file is written to disk for traceability/debugging, then
    deleted once the conversion is done (as requested).
    """
    reader = _ByteReader(data[offset:])

    vertices:         list[float]     = []
    normals:          list[float]     = []
    uvs:              list[float]     = []
    faces:            list[int]       = []
    tangents:         list[int]       = []
    lods:             list[int]       = []
    envelopes:        list[Envelope]  = []
    bones:            list[Bone]      = []
    bone_names_str:   str             = ""
    name_table_bytes: bytes           = b""
    subsets:          list[MeshSubset] = []


    while reader.get_remaining() >= 16:
        chunk_type    = reader.string(8)
        chunk_version = reader.uint32le()
        chunk_size    = reader.uint32le()
        chunk_data    = reader.array(chunk_size)

        if chunk_type == "COREMESH":
            chunk_reader = _ByteReader(chunk_data)
            if chunk_version == 1:
                vertices, normals, uvs, faces, tangents = _parse_coremesh_v1(chunk_reader)
            elif chunk_version == 2:
                vertices, normals, uvs, faces, tangents = _parse_coremesh_v2(chunk_reader)
            else:
                debug_print(f"read_mesh_v6_v7: unknown COREMESH version {chunk_version}, skipping")

            if not lods:
                lods = [0, len(faces) // 3]

        elif chunk_type == "LODS\0\0\0\0":
            chunk_reader = _ByteReader(chunk_data)
            if chunk_version == 1:
                _lod_type             = chunk_reader.uint16le()
                _num_high_quality     = chunk_reader.uint8()
                num_lods              = chunk_reader.uint32le()
                if num_lods > 2:
                    lods = []
                    for _ in range(num_lods):
                        lods.append(chunk_reader.uint32le())
                # else: keep the [0, faceCount] default set by COREMESH handler
		
        elif chunk_type == "SKINNING":
            chunk_reader = _ByteReader(chunk_data)
            if chunk_version == 1:
                envelopes, bones, bone_names_str, name_table_bytes, subsets = \
                    _parse_skinning_chunk_v1(chunk_reader)
                debug_print(
                    f"read_mesh_v6_v7: SKINNING — "
                    f"{len(bones)} bones, {len(envelopes)} envelopes, {len(subsets)} subsets"
                )
            else:
                debug_print(f"read_mesh_v6_v7: unknown SKINNING version {chunk_version}, skipping")
				
        # All other chunks (FACS, HSRAVIS, …) are intentionally skipped.

    if not vertices or not faces:
        raise Exception(f"read_mesh_v6_v7: no geometry found in {version} mesh")

    if not lods:
        lods = [0, len(faces) // 3]

    has_bones = len(bones) > 0
	
	# --- Temp .obj for traceability (written and immediately deleted) ----------
    tmp_obj_path = None
    try:
        obj_text = _build_obj_text(vertices, normals, uvs, faces, lods)
        with tempfile.NamedTemporaryFile(mode='w', suffix='_obj.obj',
                                         delete=False) as tmp_obj:
            tmp_obj_path = tmp_obj.name
            tmp_obj.write(obj_text)

        debug_print(f"read_mesh_v6_v7: wrote temp OBJ to {tmp_obj_path}")

    finally:
        if tmp_obj_path and os.path.exists(tmp_obj_path):
            os.remove(tmp_obj_path)
            debug_print(f"read_mesh_v6_v7: deleted temp OBJ {tmp_obj_path}")

    # --- Build FileMeshData from flat arrays (1:1, no deduplication) ----------
    # Only the first LOD range of faces is used.

    lod_face_start = lods[0] if len(lods) >= 1 else 0
    lod_face_end   = lods[1] if len(lods) >= 2 else len(faces) // 3
    lod_faces = faces[lod_face_start * 3 : lod_face_end * 3]

    meshData = _mesh_data_from_flat(vertices, normals, uvs, lod_faces, tangents)

	# Attach bone/skinning data when present so the caller can choose v4 export.
    if has_bones:
        meshData.bones       = bones
        meshData.boneNames   = bone_names_str
        meshData.envelopes   = envelopes
        meshData.meshSubsets = subsets

    target = "v4.00" if has_bones else "v2.00"

    debug_print(
        "read_mesh_v6_v7: converted %s -> %d vertices, %d faces (v2.00)" %
        (version, len(meshData.vnts), len(meshData.faces))
    )
    return meshData


# ---------------------------------------------------------------------------
# End of v6/v7 support
# ---------------------------------------------------------------------------


def read_mesh_data(data: bytes) -> FileMeshData:
    meshVersion = get_mesh_version(data)
    startingOffset = data.find(b"\n") + 1
    debug_print(f"meshVersion={meshVersion}, startingOffset={startingOffset}")

    meshData: FileMeshData
    if meshVersion == "1.00":
        meshData = read_mesh_v1(data, startingOffset, 0.5, True)
    elif meshVersion == "1.01":
        meshData = read_mesh_v1(data, startingOffset, 1.0, False)
    elif meshVersion == "2.00":
        meshData = read_mesh_v2(data, startingOffset)
    elif meshVersion == "3.00" or meshVersion == "3.01":
        meshData = read_mesh_v3(data, startingOffset)
    elif meshVersion == "4.00" or meshVersion == "4.01":
        meshData = read_mesh_v4(data, startingOffset)
    elif meshVersion == "5.00" or meshVersion == "5.01":
        meshData = read_mesh_v5(data, startingOffset)
    elif meshVersion in ("6.00", "6.01", "7.00", "7.01"):
        meshData = read_mesh_v6_v7(data, startingOffset, meshVersion)
    else:
        raise Exception(
            f"read_mesh_data: unsupported mesh version ({meshVersion})")
    return meshData


if __name__ == "__main__":
    arguments = sys.argv[1:]
    if len(arguments) < 1:
        debug_print("Usage: RBXMesh.py <mesh file location> [2.0|3.0|4.0]")
        debug_print("  v4.01 / v5.00 / v5.01 meshes are automatically converted to v4.00.")
        debug_print("  v6/v7 meshes are automatically converted to v2.00 (or v4.00 if bones).")
        debug_print("  Draco-compressed v6/v7 meshes require the DracoPy package.")
        exit(1)

    meshFile = open(arguments[0], "rb")
    meshData_bytes = meshFile.read()
    meshFile.close()

    meshData = read_mesh_data(meshData_bytes)

    if len(arguments) > 1:
        if arguments[1] == "2.0":
            out_path = f"{arguments[0]}.v2"
            with open(out_path, "wb") as f:
                f.write(export_mesh_v2(meshData))
            debug_print(f"Exported v2.00 mesh to {out_path}")
        elif arguments[1] == "3.0":
            out_path = f"{arguments[0]}.v3"
            with open(out_path, "wb") as f:
                f.write(export_mesh_v3(meshData))
            debug_print(f"Exported v3.00 mesh to {out_path}")
        elif arguments[1] == "4.0":
            out_path = f"{arguments[0]}.v4"
            with open(out_path, "wb") as f:
                f.write(export_mesh_v4(meshData))
            debug_print(f"Exported v4.00 mesh to {out_path}")
    else:
        # Default for v6/v7: auto-select v4.00 (bones present) or v2.00 (no bones)
        version = get_mesh_version(meshData_bytes)
        if version in ("6.00", "6.01", "7.00", "7.01"):
            if len(meshData.bones) > 0:
                out_path = f"{arguments[0]}.v4"
                with open(out_path, "wb") as f:
                    f.write(export_mesh_v4(meshData))
                debug_print(
                    f"v6/v7 mesh (bones present) auto-converted to v4.00 -> {out_path}"
                )
            else:
                out_path = f"{arguments[0]}.v2"
                with open(out_path, "wb") as f:
                    f.write(export_mesh_v2(meshData))
                debug_print(
                    f"v6/v7 mesh (no bones) auto-converted to v2.00 -> {out_path}"
                )
        elif version in ("4.01", "5.00", "5.01"):
            out_path = f"{arguments[0]}.v4"
            with open(out_path, "wb") as f:
                f.write(export_mesh_v4(meshData))
            debug_print(
                f"{version} mesh auto-converted and exported as v4.00 to {out_path}"
            )
