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
        mesh_version = rbxmesh.get_mesh_version(original_data)
    except Exception:
        return None

    if mesh_version < "4.01":
        return original_data

    '''
    # Quite simply replaces the header with `version 4.00`.
    elif mesh_version == "4.01":
        return b''.join([
            b'version 4.00',
            original_data[0xc:],
        ])
    '''

    mesh_data = rbxmesh.read_mesh_data(original_data)
    # Exports as v4 if bones present, v2 otherwise; bones are not yet tested.
    if len(mesh_data.bones) > 0:
        return bytes(rbxmesh.export_mesh_v4(mesh_data))
    else:
        return bytes(rbxmesh.export_mesh_v2(mesh_data))
