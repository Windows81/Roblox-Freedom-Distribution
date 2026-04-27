from assets.serialisers.csg import csgphs8
from .util import CSG_HEADER
from . import csgmdl5


def replace_header(data: bytes, fr_header: bytes, to_header: bytes) -> bytes:
    '''
    This function accounts for the possibility of `data` being XOR-encrypted,
    Assuming that an unencrypted form of `data` begins with the contents of `fr_header`.
    '''
    data_start = len(fr_header)
    assert data_start == len(to_header)

    new_version_header = bytes(
        v ^ fr ^ to
        for v, fr, to in zip(
            data[:data_start],
            fr_header,
            to_header,
        )
    )

    return b''.join([
        new_version_header,
        data[data_start:],
    ])


def splice_without_middle_elements(data: bytes, fr: int, ln: int) -> bytes:
    return b''.join([
        data[:fr],
        data[fr+ln:],
    ])


def parse(data: bytes) -> bytes | None:
    if data.startswith(CSG_HEADER.MDL4.value):
        return replace_header(
            data,
            fr_header=CSG_HEADER.MDL4.value,
            to_header=CSG_HEADER.MDL2.value,
        )

    elif data.startswith(CSG_HEADER.MDL5.value):
        return csgmdl5.convert_to_csgmdl2(data)

    elif data.startswith(CSG_HEADER.PHS5.value):
        '''
        CSGPHS5 is identical in data format to CSGPHS3.
        https://github.com/krakow10/rbx_mesh/blob/d10bcdf727dd9c2504560189a5cb106aa9107ec5/src/physics_data.rs#L71
        '''
        return replace_header(
            data,
            fr_header=CSG_HEADER.PHS5.value,
            to_header=CSG_HEADER.PHS3.value,
        )

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
        CSGPHS6 and CSGPHS7 both contain `PhysicsInfo` structs, which as above indicate a length of 40 bytes.
        We want to get rid of these `PhysicsInfo` structs for CSGPHS3.
        https://github.com/krakow10/rbx_mesh/blob/d10bcdf727dd9c2504560189a5cb106aa9107ec5/src/physics_data.rs#L8-L16
        '''
        return splice_without_middle_elements(
            data=replace_header(
                data,
                fr_header=CSG_HEADER.PHS6.value,
                to_header=CSG_HEADER.PHS3.value,
            ),
            fr=len(CSG_HEADER.PHS6.value), ln=40,
        )

    elif data.startswith(CSG_HEADER.PHS7.value):
        '''
        Why 41 bytes in CSGPHS7?
        +40: `PhysicsInfo`, as per above.
        + 1: the mysterious magic number `03` (one byte) that takes place after the versioned header.
        https://github.com/krakow10/rbx_mesh/blob/d10bcdf727dd9c2504560189a5cb106aa9107ec5/src/physics_data.rs#L54
        '''
        return splice_without_middle_elements(
            data=replace_header(
                data,
                fr_header=CSG_HEADER.PHS7.value,
                to_header=CSG_HEADER.PHS3.value,
            ),
            fr=len(CSG_HEADER.PHS7.value), ln=41,
        )

    elif data.startswith(CSG_HEADER.PHS8.value):
        return csgphs8.convert_to_csgphs3(data)
