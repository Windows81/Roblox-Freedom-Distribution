from . import rbxmesh


def get_version(original_data: bytes) -> str:
    return rbxmesh.get_mesh_version(original_data)


def check(original_data: bytes) -> bool:
    try:
        get_version(original_data)
        return True
    except:
        return False


def parse(original_data: bytes) -> bytes | None:
    try:
        version = rbxmesh.get_mesh_version(original_data)
        if version < "4.00":
            return

        mesh_data = rbxmesh.read_mesh_data(original_data)
        return bytes(rbxmesh.export_mesh_v2(mesh_data))

    except Exception:
        return
