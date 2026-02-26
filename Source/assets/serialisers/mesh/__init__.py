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
        mesh_data = rbxmesh.read_mesh_data(original_data)

        if version in ("6.00", "6.01", "7.00", "7.01"):
            # v6/v7: export as v4 if bones present, v2 otherwise (I didn't test bones yet)
            if len(mesh_data.bones) > 0:
                return bytes(rbxmesh.export_mesh_v4(mesh_data))
            else:
                return bytes(rbxmesh.export_mesh_v2(mesh_data))

        elif version in ("4.01", "5.00", "5.01"):
            # Always downgrade to v4, even if no bones
            return bytes(rbxmesh.export_mesh_v4(mesh_data))

        else:
            # All other versions: return as-is
            return original_data

    except Exception:
        return
