from typing import Callable
import dataclasses
import functools
import lz4.block
import pyzstd
import io

# b'<roblox!\x89\xff\r\n\x1a\n'
HEADER_SIGNATURE = bytes([
    60, 114, 111, 98, 108, 111, 120, 33, 137, 255, 13, 10, 26, 10,
])

INT_SIZE = 4


@functools.cache
def wrap_string(v: bytes) -> bytes:
    return len(v).to_bytes(INT_SIZE, 'little') + v


def split_prop_strings(data: bytes, limit: int = -1) -> list[bytes]:
    '''
    Where `data` contains a bunch of concatenates `rbxl` strings.
    '''
    splits: list[bytes] = []
    length = len(data)
    index = 0
    while index < length:
        size = int.from_bytes(data[index:index+INT_SIZE], 'little')
        str_beg = index + INT_SIZE
        str_end = str_beg + size
        chunk = data[str_beg:str_end]
        index = str_end

        splits.append(chunk)
        if limit >= 0 and len(splits) == limit:
            return splits

    assert index == length
    return splits


def join_prop_strings(data: list[bytes]) -> bytes:
    return b''.join(
        wrap_string(d)
        for d in data
    )


@dataclasses.dataclass
class chunk_info:
    chunk_name: bytes
    reserved_metadata: bytes
    chunk_data: bytes
    '''All chunk information which comes *after* the `chunk_name`'''


@dataclasses.dataclass
class inst_dict_item:
    class_name: bytes
    instance_count: int


def get_class_iden(info: chunk_info) -> bytes | None:
    '''
    For `INST` or `PROP`, refer to `ClassID`.
    https://github.com/RobloxAPI/spec/blob/master/formats/rbxl.md#instances-chunk
    https://github.com/RobloxAPI/spec/blob/master/formats/rbxl.md#properties-chunk
    '''
    if info.chunk_name not in {b'PROP', b'INST'}:
        return None
    return info.chunk_data[0:INT_SIZE]


def get_first_chunk_str(info: chunk_info) -> bytes | None:
    '''
    For `INST`, refer to `ClassName`.
    https://github.com/RobloxAPI/spec/blob/master/formats/rbxl.md#instances-chunk
    For `PROP`, refer to `Name`.
    https://github.com/RobloxAPI/spec/blob/master/formats/rbxl.md#properties-chunk
    '''
    if info.chunk_name not in {b'PROP', b'INST'}:
        return None
    str_size = int.from_bytes(
        info.chunk_data[INT_SIZE:INT_SIZE*2],
        byteorder='little',
    )
    str_start = 2 * INT_SIZE
    return info.chunk_data[str_start:str_start + str_size]


def get_pre_prop_values_bytes(info: chunk_info) -> bytes:
    '''
    Returns all `PROP` data up to the the data-type byte.
    '''
    if info.chunk_name not in {b'PROP'}:
        return info.chunk_data
    str_size = int.from_bytes(
        info.chunk_data[INT_SIZE:INT_SIZE*2],
        byteorder='little',
    )
    str_start = 2 * INT_SIZE
    return info.chunk_data[:str_start + str_size + 1]


def get_prop_values_bytes(info: chunk_info) -> bytes | None:
    '''
    For `PROP`, refer to `Values`.
    https://github.com/RobloxAPI/spec/blob/master/formats/rbxl.md#values
    '''
    if info.chunk_name not in {b'PROP'}:
        return None
    str_size = int.from_bytes(
        info.chunk_data[INT_SIZE:INT_SIZE*2],
        byteorder='little',
    )
    str_start = 2 * INT_SIZE
    return info.chunk_data[str_start + str_size + 1:]


def get_type_iden(info: chunk_info) -> int | None:
    '''
    For `PROP`, refer to `TypeID`.
    https://github.com/RobloxAPI/spec/blob/master/formats/rbxl.md#values
    '''
    if info.chunk_name not in {b'PROP'}:
        return None
    str_size = int.from_bytes(
        info.chunk_data[INT_SIZE:INT_SIZE*2],
        byteorder='little',
    )
    str_end = 2 * INT_SIZE + str_size
    return info.chunk_data[str_end]


def get_instance_count(info: chunk_info) -> int | None:
    '''
    For `INST`, refer to `Length`.
    https://github.com/RobloxAPI/spec/blob/master/formats/rbxl.md#instances-chunk
    '''
    if info.chunk_name not in {b'INST'}:
        return None
    str_size = int.from_bytes(
        info.chunk_data[INT_SIZE:INT_SIZE*2],
        byteorder='little',
    )
    prop_start = 2 * INT_SIZE + str_size + 1
    return int.from_bytes(
        info.chunk_data[prop_start:prop_start + INT_SIZE],
        byteorder='little',
    )


class rbxl_parser:
    def __init__(self, data: bytes) -> None:
        super().__init__()
        self.file_data = data

    def parse_file(
        self,
        transforms: list[Callable[['rbxl_parser', chunk_info], bytes | None]],
    ) -> bytes:

        self.read_stream = io.BytesIO(self.file_data)
        self.write_stream = io.BytesIO()

        # Copies the header from `read_stream` to `write_stream`.
        header = self.__process_header(self.read_stream)
        if header is None:
            return self.file_data
        self.write_stream.write(header)

        # https://github.com/RobloxAPI/spec/blob/master/formats/rbxl.md#properties-chunk
        while True:
            info = self.__process_chunk()
            if info is None:
                break
            for trans in transforms:
                info.chunk_data = (
                    trans(self, info)
                    or info.chunk_data
                )
            new_chunk = self.compile_chunk(info)
            self.write_stream.write(new_chunk)

        result = self.write_stream.getvalue()
        self.read_stream.close()
        self.write_stream.close()
        return result

    def __process_header(self, read_stream: io.BytesIO) -> bytes | None:
        if read_stream.read(len(HEADER_SIGNATURE)) != HEADER_SIGNATURE:
            return None

        self.header_info = read_stream.read(18)
        self.format_version = int.from_bytes(
            self.header_info[0:2],
            byteorder='little',
        )
        self.class_count = int.from_bytes(
            self.header_info[2:6],
            byteorder='little',
        )
        self.instance_count = int.from_bytes(
            self.header_info[6:10],
            byteorder='little',
        )
        self.reserved_metadata = int.from_bytes(
            self.header_info[10:18],
            byteorder='little',
        )
        self.class_dict: dict[bytes, inst_dict_item] = {}

        return b''.join([
            HEADER_SIGNATURE,
            self.header_info,
        ])

    def __process_chunk(self) -> chunk_info | None:
        info = self.decompress_chunk()
        if info is None:
            return None

        if info.chunk_name == b'INST':
            class_id = get_class_iden(info)
            if class_id is None:
                return

            class_name = get_first_chunk_str(info)
            if class_name is None:
                return

            instance_count = get_instance_count(info)
            if instance_count is None:
                return

            self.class_dict[class_id] = inst_dict_item(
                class_name=class_name,
                instance_count=instance_count,
            )

        return info

    def decompress_chunk(self) -> chunk_info | None:
        chunk_name = self.read_stream.read(4)
        if chunk_name == b'':
            return None

        assert chunk_name == chunk_name.upper()

        compressed_size = int.from_bytes(
            self.read_stream.read(4),
            byteorder='little',
        )
        uncompressed_size = int.from_bytes(
            self.read_stream.read(4),
            byteorder='little',
        )
        reserved_metadata = self.read_stream.read(4)

        # https://dom.rojo.space/binary.html#chunks
        if compressed_size == 0:
            chunk_data = self.read_stream.read(uncompressed_size)
        else:
            compressed_chunk_data = self.read_stream.read(compressed_size)
            if compressed_chunk_data.startswith(b'\x28\xB5\x2F\xFD'):
                chunk_data = pyzstd.decompress(compressed_chunk_data)
            else:
                chunk_data = lz4.block.decompress(
                    source=compressed_chunk_data,
                    uncompressed_size=uncompressed_size,
                )

        assert len(chunk_data) == uncompressed_size
        return chunk_info(
            chunk_name=chunk_name,
            reserved_metadata=reserved_metadata,
            chunk_data=chunk_data,
        )

    @staticmethod
    def compile_chunk(info: chunk_info) -> bytes:
        new_size = len(info.chunk_data)
        return b''.join([
            info.chunk_name,
            int.to_bytes(
                0,
                byteorder='little',
                length=4,
            ),
            int.to_bytes(
                new_size,
                byteorder='little',
                length=4,
            ),
            info.reserved_metadata,
            info.chunk_data,
        ])
