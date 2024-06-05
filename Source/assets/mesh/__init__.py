from . import rbxmesh


def parse(originalData: bytes) -> bytes:
    try:
        meshVersion = rbxmesh.get_mesh_version(originalData)
        if meshVersion < 4:
            return originalData

        meshData = rbxmesh.read_mesh_data(originalData, meshVersion)
        return rbxmesh.export_mesh_v2(meshData)
    except Exception:
        return originalData
