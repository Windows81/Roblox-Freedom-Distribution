"""
    https://github.com/PrintedScript/RBXMesh/blob/main/RBXMesh.py
    Python Library for reading and writing Roblox mesh files.
    Written by something.else on 21/9/2023

    Supported meshes up to version 5.
    Mesh Format documentation by MaximumADHD: https://devforum.roblox.com/t/roblox-mesh-format/326114
"""

import struct
from dataclasses import dataclass
import sys


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
        return bytearray(
            struct.pack("<f", self.vx) +
            struct.pack("<f", self.vy) +
            struct.pack("<f", self.vz) +
            struct.pack("<f", self.nx) +
            struct.pack("<f", self.ny) +
            struct.pack("<f", self.nz) +
            struct.pack("<f", self.tu) +
            struct.pack("<f", self.tv) +
            self.tx.to_bytes(1, "little") +
            self.ty.to_bytes(1, "little") +
            self.tz.to_bytes(1, "little") +
            self.ts.to_bytes(1, "little") +
            self.r.to_bytes(1, "little") +
            self.g.to_bytes(1, "little") +
            self.b.to_bytes(1, "little") +
            self.a.to_bytes(1, "little")
        )


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
        return bytearray(
            struct.pack("<f", self.vx) +
            struct.pack("<f", self.vy) +
            struct.pack("<f", self.vz) +
            struct.pack("<f", self.nx) +
            struct.pack("<f", self.ny) +
            struct.pack("<f", self.nz) +
            struct.pack("<f", self.tu) +
            struct.pack("<f", self.tv) +
            self.tx.to_bytes(1, "little") +
            self.ty.to_bytes(1, "little") +
            self.tz.to_bytes(1, "little") +
            self.ts.to_bytes(1, "little")
        )


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
        return bytearray(
            self.a.to_bytes(4, "little") +
            self.b.to_bytes(4, "little") +
            self.c.to_bytes(4, "little")
        )


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
        return bytearray(
            self.cbSize.to_bytes(2, "little") +
            self.cbVerticesStride.to_bytes(1, "little") +
            self.cbFaceStride.to_bytes(1, "little") +
            self.num_vertices.to_bytes(4, "little") +
            self.num_faces.to_bytes(4, "little")
        )

    def __str__(self) -> str:
        return f"FileMeshHeader(cbSize={self.cbSize}, cbVerticesStride={self.cbVerticesStride}, cbFaceStride={self.cbFaceStride}, num_vertices={self.num_vertices}, num_faces={self.num_faces})"

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
        return bytearray(
            self.cbSize.to_bytes(2, "little") +
            self.cbVerticesStride.to_bytes(1, "little") +
            self.cbFaceStride.to_bytes(1, "little") +
            self.sizeof_LOD.to_bytes(2, "little") +
            self.numLODs.to_bytes(2, "little") +
            self.num_vertices.to_bytes(4, "little") +
            self.num_faces.to_bytes(4, "little")
        )


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
        return bytearray(
            self.sizeof_MeshHeader.to_bytes(2, "little") +
            self.lodType.to_bytes(2, "little") +
            self.numVerts.to_bytes(4, "little") +
            self.numFaces.to_bytes(4, "little") +
            self.numLODs.to_bytes(2, "little") +
            self.numBones.to_bytes(2, "little") +
            self.sizeof_boneNamesBuffer.to_bytes(4, "little") +
            self.numSubsets.to_bytes(2, "little") +
            self.numHighQualityLODs.to_bytes(1, "little") +
            self.unused.to_bytes(1, "little")
        )


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
            self.bones.append(int.from_bytes(data[i:i+1], "little"))
            self.weights.append(int.from_bytes(data[i+4:i+5], "little"))

    def export_data(self) -> bytes:
        return bytearray(
            self.bones[0].to_bytes(1, "little") +
            self.bones[1].to_bytes(1, "little") +
            self.bones[2].to_bytes(1, "little") +
            self.bones[3].to_bytes(1, "little") +
            self.weights[0].to_bytes(1, "little") +
            self.weights[1].to_bytes(1, "little") +
            self.weights[2].to_bytes(1, "little") +
            self.weights[3].to_bytes(1, "little")
        )


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
        return bytearray(
            self.boneNameIndex.to_bytes(4, "little") +
            self.parentIndex.to_bytes(2, "little") +
            self.lodParentIndex.to_bytes(2, "little") +
            struct.pack("<f", self.culling) +
            struct.pack("<f", self.r00) +
            struct.pack("<f", self.r01) +
            struct.pack("<f", self.r02) +
            struct.pack("<f", self.r10) +
            struct.pack("<f", self.r11) +
            struct.pack("<f", self.r12) +
            struct.pack("<f", self.r20) +
            struct.pack("<f", self.r21) +
            struct.pack("<f", self.r22) +
            struct.pack("<f", self.x) +
            struct.pack("<f", self.y) +
            struct.pack("<f", self.z)
        )


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
            self.boneIndicies.append(int.from_bytes(data[20+i:21+i], "little"))

    def export_data(self) -> bytes:
        subsetData: bytes = bytearray(
            self.facesBegin.to_bytes(4, "little") +
            self.facesLength.to_bytes(4, "little") +
            self.vertsBegin.to_bytes(4, "little") +
            self.vertsLength.to_bytes(4, "little") +
            self.numBoneIndicies.to_bytes(4, "little")
        )
        for i in range(0, 26):
            subsetData += self.boneIndicies[i].to_bytes(1, "little")

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
        return bytearray(
            self.sizeof_MeshHeader.to_bytes(2, "little") +
            self.lodType.to_bytes(2, "little") +
            self.numVerts.to_bytes(4, "little") +
            self.numFaces.to_bytes(4, "little") +
            self.numLODs.to_bytes(2, "little") +
            self.numBones.to_bytes(2, "little") +
            self.sizeof_boneNamesBuffer.to_bytes(4, "little") +
            self.numSubsets.to_bytes(2, "little") +
            self.numHighQualityLODs.to_bytes(1, "little") +
            self.unusedPadding.to_bytes(1, "little") +
            self.facsDataFormat.to_bytes(4, "little") +
            self.facsDataSize.to_bytes(4, "little")
        )


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


def get_mesh_version(data: bytes) -> float:
    """Gets the version of the mesh file. Throws an exception if the version is not supported."""

    if len(data) < 12:
        raise Exception(
            f"get_mesh_version: data is too short ({len(data)} bytes)")
    if not data[0:8] == b"version ":
        raise Exception(f"get_mesh_version: invalid mesh header ({data[0:8]})")

    if data[0:12] == b"version 1.00":
        return 1.0
    elif data[0:12] == b"version 1.01":
        return 1.1
    elif data[0:12] == b"version 2.00":
        return 2.0
    elif data[0:12] == b"version 3.00":
        return 3.0
    elif data[0:12] == b"version 3.01":
        return 3.1
    elif data[0:12] == b"version 4.00":
        return 4.0
    elif data[0:12] == b"version 4.01":
        return 4.1
    elif data[0:12] == b"version 5.00":
        return 5.0
    elif data[0:12] == b"version 5.01":
        return 5.1
    else:
        raise Exception(
            f"get_mesh_version: unsupported mesh version ({data[0:12]})")


def read_mesh_v1(data_bytes: bytes, offset: int, scale: float = 0.5, invertUV: bool = True) -> FileMeshData:
    data = data_bytes.decode("ASCII")

    meshData: FileMeshData = FileMeshData(
        [], [], FileMeshHeader(0, 0, 0, 0, 0), [], [], "", [], [], [])
    numFaces: int = int(data.split("\n")[1])
    debug_print(f"read_mesh_v1: numFaces={numFaces}")

    # [0.551563,-0.0944613,0.0862401] we need to find every vector3 in the file
    # Each vert has 3 vector3 values so we need to find 3 vector3 values for each vert
    startingIndex = data.find("[")
    allVectorStrs: list[str] = data[startingIndex:].split("]")
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
        [], [], FileMeshHeader(0, 0, 0, 0, 0), [], [], "", [], [], [])
    meshHeader: FileMeshHeaderV4 = FileMeshHeaderV4(
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
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
    offset += meshHeader.sizeof_boneNamesBuffer
    debug_print(f"read_mesh_v4: boneNames={boneNames}")

    meshSubsets: list[MeshSubset] = []
    for i in range(0, meshHeader.numSubsets):
        meshSubsets.append(MeshSubset(0, 0, 0, 0, 0, []))
        meshSubsets[i].read_data(read_data(data, offset + i * 72, 72))

        debug_print(f"read_mesh_v4: meshSubsets[{i}]={meshSubsets[i]}")
    meshData.meshSubsets = meshSubsets
    offset += meshHeader.numSubsets * 72
    offset += meshHeader.unused

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
            temp = Envelope([], [])
            temp.read_data(read_data(data, offset + i * 8, 8))
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


def export_mesh_v2(meshData: FileMeshData) -> bytes:
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


def export_mesh_v3(meshData: FileMeshData) -> bytes:
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


def read_mesh_data(data: bytes, meshVersion: float) -> FileMeshData:
    startingOffset = data.find(b"\n")

    if meshVersion == 1.0:
        meshData: FileMeshData = read_mesh_v1(
            data, startingOffset + 1, 0.5)

    elif meshVersion == 1.1:
        meshData: FileMeshData = read_mesh_v1(
            data, startingOffset + 1, 1.0, False)

    elif meshVersion == 2.0:
        meshData: FileMeshData = read_mesh_v2(
            data, startingOffset + 1)

    elif meshVersion == 3.0 or meshVersion == 3.1:
        meshData: FileMeshData = read_mesh_v3(
            data, startingOffset + 1)

    elif meshVersion == 4.0 or meshVersion == 4.01 or meshVersion == 4.1:
        meshData: FileMeshData = read_mesh_v4(
            data, startingOffset + 1)

    elif meshVersion == 5.0 or meshVersion == 5.1:
        meshData: FileMeshData = read_mesh_v5(
            data, startingOffset + 1)
    else:
        raise Exception(
            f"read_mesh_data: unsupported mesh version ({meshVersion})")
    return meshData


def convert_mesh(originalData: bytes) -> bytes:
    meshVersion = get_mesh_version(originalData)
    if meshVersion < 4:
        return originalData

    meshData = read_mesh_data(originalData, meshVersion)
    return export_mesh_v2(meshData)
