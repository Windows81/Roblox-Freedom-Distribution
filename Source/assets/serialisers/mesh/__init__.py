from . import rbxmesh


def parse(originalData: bytes) -> bytes | None:
    try:
        meshVersion = rbxmesh.get_mesh_version(originalData)
        if meshVersion < 4.0:
            return originalData

        meshData = rbxmesh.read_mesh_data(originalData)
        return bytes(rbxmesh.export_mesh_v2(meshData))

    except Exception:
        return
