from . import rbxmesh


def parse(originalData: bytes) -> bytes:
    try:
        meshVersion = rbxmesh.get_mesh_version(originalData)
        if meshVersion in {2.0, 3.0, 3.1, 5.0, 5.1}:
            return originalData

        meshData = rbxmesh.read_mesh_data(originalData, meshVersion)
        return rbxmesh.export_mesh_v2(meshData)
    except Exception:
        return originalData
