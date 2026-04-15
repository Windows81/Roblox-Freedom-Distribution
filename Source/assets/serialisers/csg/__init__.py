from .util import INT_SIZE, CSG_HEADER
from . import csgmdl5


def replace_header_version(data: bytes, versioned_header: bytes, from_version: int, to_version: int) -> bytes:
    '''
    The redundant `from_version` argument is used here to account for the possibility of the data being XOR-encrypted.
    '''
    version_loc = len(versioned_header) - INT_SIZE
    old_version = int.from_bytes(
        data[version_loc:version_loc+INT_SIZE],
        byteorder='little',
    )
    new_version = old_version ^ (from_version ^ to_version)

    return b''.join([
        data[:version_loc],
        new_version.to_bytes(length=INT_SIZE, byteorder='little'),
        data[version_loc+INT_SIZE:],
    ])


def splice_without_middle_elements(data: bytes, fr: int, ln: int) -> bytes:
    return b''.join([
        data[:fr],
        data[fr+ln:],
    ])


def parse(data: bytes) -> bytes | None:
    if data.startswith(CSG_HEADER.MDL4.value):
        return replace_header_version(data, CSG_HEADER.MDL4.value, 4, 2)

    elif data.startswith(CSG_HEADER.MDL5.value):
        return csgmdl5.convert_to_csgmdl2(data)

    elif data.startswith(CSG_HEADER.PHS5.value):
        '''
        CSGPHYS5 is identical in data format to CSGPHYS3.
        https://github.com/krakow10/rbx_mesh/blob/d10bcdf727dd9c2504560189a5cb106aa9107ec5/src/physics_data.rs#L71
        '''
        return replace_header_version(data, CSG_HEADER.PHS5.value, 5, 3)

    elif data.startswith(CSG_HEADER.PHS6.value):
        '''
        Why 40 bytes?
        ```rs
        #[binrw::binrw]
        #[brw(little)]
        #[derive(Debug,Clone)]
        pub struct PhysicsInfo{
            pub volume:f32,
            pub center_of_gravity:[f32;3],
            // upper triangular matrix read left to right top to bottom
            pub moment_of_inertia_packed:[f32;6],
        }
        ```
        CSGPHYS6 and CSGPHYS7 both contain `PhysicsInfo` structs, which as above indicate a length of 40 bytes.
        https://github.com/krakow10/rbx_mesh/blob/d10bcdf727dd9c2504560189a5cb106aa9107ec5/src/physics_data.rs#L8-L16
        '''
        return splice_without_middle_elements(
            replace_header_version(data, CSG_HEADER.PHS6.value, 6, 3),
            len(CSG_HEADER.PHS6.value), 40,
        )

    elif data.startswith(CSG_HEADER.PHS7.value):
        '''
        Why 41 bytes in CSGPHYS7?
        +40: `PhysicsInfo`, as per above.
        + 1: the mysterious magic number `03` (one byte) that takes place after the versioned header.
        https://github.com/krakow10/rbx_mesh/blob/d10bcdf727dd9c2504560189a5cb106aa9107ec5/src/physics_data.rs#L54
        '''
        return splice_without_middle_elements(
            replace_header_version(data, CSG_HEADER.PHS7.value, 7, 3),
            len(CSG_HEADER.PHS7.value), 41,
        )

    elif data.startswith(CSG_HEADER.PHS8.value):
        # TODO: implement CSGPHS8; returns an empty CSPHS object for now.
        return (
            b'CSGPHS\x03\x00\x00\x00' +
            b'\x10\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\x10\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\x80\x3F' +
            b'\x00\x00\x00\x00' +
            b'\x04\x00\x00\x00' +
            b'\x00\x00\x00\x00'
        )
