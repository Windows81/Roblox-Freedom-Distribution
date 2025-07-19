import copy
import hashlib
from typing import Callable, override
import dataclasses
import lz4.block
import pyzstd
import io

HEADER_SIGNATURE = b'<roblox!\x89\xff\r\n\x1a\n'
INT_SIZE = 4


def wrap_string(v: bytes) -> bytes:
    return len(v).to_bytes(INT_SIZE, 'little') + v


def read_int(data: bytes) -> int:
    return int.from_bytes(data, byteorder='little')


def split_prop_strings(data: bytes, limit: int = -1) -> list[bytes]:
    '''
    Where `data` contains a bunch of concatenates `rbxl` strings.
    '''
    splits: list[bytes] = []
    length = len(data)
    index = 0
    while index < length:
        size = int.from_bytes(data[index:index+INT_SIZE])
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


class chunk_data_type:
    CLASS_MAPPING: dict[bytes, type['chunk_data_type']] = {}
    CLASS_NAME = b''

    def __init__(self, chunk_data: bytes) -> None:
        super().__init__()
        self.__chunk_data = chunk_data

    @staticmethod
    def from_bytes(chunk_name: bytes, data: bytes) -> 'chunk_data_type':
        return chunk_data_type.CLASS_MAPPING[chunk_name](data)

    def to_bytes(self) -> bytes:
        return self.__chunk_data

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        chunk_data_type.CLASS_MAPPING[cls.CLASS_NAME] = cls


def write_int(value: int) -> bytes:
    return value.to_bytes(INT_SIZE, byteorder='little')


class chunk_data_type_prop(chunk_data_type):
    CHUNK_NAME = b'PROP'

    def __init__(self, chunk_data: bytes) -> None:
        super().__init__(chunk_data)
        reader = io.BytesIO(chunk_data)
        self.class_iden: int = read_int(reader.read(INT_SIZE))
        strlen: int = read_int(reader.read(INT_SIZE))
        self.prop_name: bytes = reader.read(strlen)
        self.prop_type: int = read_int(reader.read(1))
        self.prop_values: bytes = reader.read()

    @override
    def to_bytes(self) -> bytes:
        writer = io.BytesIO()
        writer.write(write_int(self.class_iden))
        writer.write(wrap_string(self.prop_name))
        writer.write(self.prop_type.to_bytes(1))
        writer.write(self.prop_values)
        return writer.getvalue()


class chunk_data_type_sstr(chunk_data_type):
    CHUNK_NAME = b'SSTR'

    def __init__(self, chunk_data: bytes) -> None:
        super().__init__(chunk_data)
        reader = io.BytesIO(chunk_data)
        self.version: int = read_int(reader.read(INT_SIZE))
        self.length: int = read_int(reader.read(INT_SIZE))
        self.strings: list[tuple[bytes, bytes]] = []
        for _ in range(self.length):
            hash_value: bytes = reader.read(16)
            strlen: int = read_int(reader.read(INT_SIZE))
            string_value: bytes = reader.read(strlen)
            self.strings.append((hash_value, string_value))

    @override
    def to_bytes(self) -> bytes:
        writer = io.BytesIO()
        writer.write(write_int(self.version))
        writer.write(write_int(self.length))

        # @21098765432109: Is the `md5` taken for the whole shared string *including* or *excluding* its length?
        # @regg.ie: Excluding, it's a sum of the payload itself. The hash is ignored by the engine and not actually ever emitted by Studio, though
        # @regg.ie: As per rbx-dom's spec
        for _, string_value in self.strings:
            wrapped = wrap_string(string_value)
            md5_hash = hashlib.md5(string_value).digest()
            writer.write(md5_hash)
            writer.write(wrapped)
        return writer.getvalue()


class chunk_data_type_inst(chunk_data_type):
    CHUNK_NAME = b'INST'

    def __init__(self, chunk_data: bytes) -> None:
        super().__init__(chunk_data)
        reader = io.BytesIO(chunk_data)
        self.class_iden: int = read_int(reader.read(INT_SIZE))
        str_size: int = read_int(reader.read(INT_SIZE))
        self.class_name: bytes = reader.read(str_size)
        self.has_service: bool = reader.read(1) != b'\x00'
        self.instant_count: int = read_int(reader.read(INT_SIZE))
        self.rest_of_data: bytes = reader.read()

    @override
    def to_bytes(self) -> bytes:
        writer = io.BytesIO()
        writer.write(write_int(self.class_iden))
        writer.write(wrap_string(self.class_name))
        writer.write(b'\x01' if self.has_service else b'\x00')
        writer.write(write_int(self.instant_count))
        writer.write(self.rest_of_data)
        return writer.getvalue()


@dataclasses.dataclass
class inst_dict_item:
    class_name: bytes
    instance_count: int


@dataclasses.dataclass
class chunk_info:
    chunk_name: bytes
    reserved_metadata: bytes
    chunk_data: chunk_data_type


type TRANSFORM_TYPE = list[Callable[[
    'rbxl_parser', chunk_data_type], chunk_data_type | None]]


class rbxl_parser:
    def __init__(self, data: bytes) -> None:
        super().__init__()
        self.file_data = data

    def parse_file(self, transforms: TRANSFORM_TYPE) -> bytes:
        self.read_stream = io.BytesIO(self.file_data)
        self.write_stream = io.BytesIO()

        # Copies the header from `read_stream` to `write_stream`.
        header = self.__process_header(self.read_stream)
        if header is None:
            return self.file_data
        self.write_stream.write(header)

        # https://github.com/RobloxAPI/spec/blob/master/formats/rbxl.md#properties-chunk
        while True:
            info = self.__process_chunk(transforms)
            if info is None:
                break

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
        self.class_dict: dict[int, inst_dict_item] = {}

        return b''.join([
            HEADER_SIGNATURE,
            self.header_info,
        ])

    def __process_chunk(self, transforms: TRANSFORM_TYPE) -> chunk_info | None:
        info = self.decompress_chunk()
        if info is None:
            return None

        if isinstance(info.chunk_data, chunk_data_type_inst):
            class_iden = info.chunk_data.class_iden
            class_name = info.chunk_data.class_name
            instance_count = info.chunk_data.instant_count

            self.class_dict[class_iden] = inst_dict_item(
                class_name=class_name,
                instance_count=instance_count,
            )

        for trans in transforms:
            result = trans(self, copy.copy(info.chunk_data))
            if result is None:
                result = info.chunk_data
            info.chunk_data = result

        new_chunk = self.compile_chunk(info)
        self.write_stream.write(new_chunk)

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
            chunk_data_bytes = self.read_stream.read(uncompressed_size)
        else:
            compressed_chunk_data = self.read_stream.read(compressed_size)
            if compressed_chunk_data.startswith(b'\x28\xB5\x2F\xFD'):
                chunk_data_bytes = pyzstd.decompress(compressed_chunk_data)
            else:
                chunk_data_bytes = lz4.block.decompress(
                    source=compressed_chunk_data,
                    uncompressed_size=uncompressed_size,
                )

        assert len(chunk_data_bytes) == uncompressed_size
        return chunk_info(
            chunk_name=chunk_name,
            reserved_metadata=reserved_metadata,
            chunk_data=chunk_data_type.from_bytes(
                chunk_name, chunk_data_bytes),
        )

    @staticmethod
    def compile_chunk(info: chunk_info) -> bytes:
        chunk_data_bytes = info.chunk_data.to_bytes()
        new_size = len(chunk_data_bytes)
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
            info.chunk_data.to_bytes(),
        ])
