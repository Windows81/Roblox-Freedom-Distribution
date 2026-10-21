from . import mesh_processing


def get_version(original_data: bytes) -> str:
    return mesh_processing._mesh_header(original_data)


def is_valid(original_data: bytes) -> bool:
    return mesh_processing.is_mesh_data(original_data)


def skip_version(mesh_version: str) -> bool:
    return mesh_version < "version 4.01"


def parse(original_data: bytes) -> bytes | None:
    try:
        mesh_version = get_version(original_data)
    except Exception:
        return None

    if skip_version(mesh_version):
        return original_data

    v2_data = mesh_processing.convert(original_data)
    if v2_data is None:
        return None

    return v2_data


def should_parse(data: bytes) -> bool:
    if not is_valid(data):
        return False

    mesh_version = get_version(data)
    return not skip_version(mesh_version)
