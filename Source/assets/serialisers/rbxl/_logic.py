from typing import Callable
import dataclasses
import itertools
import lz4.block
import pyzstd
import io
import re

HEADER_SIGNATURE = b'\x3c\x72\x6f\x62\x6c\x6f\x78\x21\x89\xff\x0d\x0a\x1a\x0a'

INT_SIZE = 4


class string_replacer:
    '''
    Rōblox has its own way of storing variable-length strings.
    This class gracefully replaces instances of one such string with another.
    '''

    @dataclasses.dataclass
    class input_info:
        match: re.Match[bytes]
        string_size: int
        match_size: int
        match_bytes: bytes
        match_start: int
        match_end: int

    def __init__(
        self,
        pattern: bytes,
        replacement_func: Callable[[re.Match[bytes]], bytes],
        chunk_data: bytes,
        max_replacements: int | None = None,
        prepend_new_length: bool = True,
    ) -> None:
        super().__init__()
        self.data = chunk_data

        self.pattern = pattern
        self.replacement_func = replacement_func
        self.max_replacements = max_replacements
        self.prepend_new_length = prepend_new_length

    def calc(self) -> bytes:
        # Extracts data on where existing strings are.
        infos = [
            info
            for match in itertools.islice(
                re.finditer(
                    br'(.{%d})(?=%s)' % (INT_SIZE, self.pattern),
                    self.data,
                ),
                self.max_replacements,
            )
            if (info := self.get_input_info(match))
        ]

        splits: list[tuple[int, string_replacer.input_info | None]] = [
            (0, None),
            *[
                split
                for info in infos
                for split in (
                    (info.match_start, info),
                    (info.match_end, None),
                )
            ],
            (len(self.data), None),
        ]

        parts = [
            self.process_info(split_start[1])
            if split_start[1] else
            self.data[split_start[0]:split_end[0]]
            for split_start, split_end in zip(splits, splits[1:])
        ]

        return b''.join(parts)

    def get_input_info(self, arg: re.Match[bytes]) -> input_info | None:
        (match_start, span_end) = arg.span()
        string_pos = match_start + INT_SIZE

        string_size = int.from_bytes(
            self.data[match_start:string_pos],
            byteorder='little',
        )

        string_end = string_pos + string_size
        full_string = arg.string[string_pos:string_end]

        new_match = re.match(
            b'%s$' % self.pattern,
            full_string,
        )

        if new_match is None:
            return None

        new_match_bytes = new_match.group()
        new_match_size = len(new_match_bytes)
        match_end = match_start + INT_SIZE + new_match_size
        assert new_match_size == string_size
        return string_replacer.input_info(
            match=new_match,
            string_size=string_size,
            match_size=new_match_size,
            match_bytes=new_match_bytes,
            match_start=match_start,
            match_end=match_end,
        )

    def process_info(self, info: input_info) -> bytes:
        result = self.replacement_func(info.match)
        result_size = len(result)

        new_size = info.string_size - info.match_size + result_size
        prefix = (
            int.to_bytes(
                new_size,
                byteorder='little',
                length=4,
            )
            if self.prepend_new_length
            else b''
        )

        return b''.join([
            prefix,
            result,
        ])


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


def get_class_id(info: chunk_info) -> bytes | None:
    '''
    For `INST` or `PROP`, refer to `ClassID`.
    https://github.com/RobloxAPI/spec/blob/master/formats/rbxl.md#instances-chunk
    https://github.com/RobloxAPI/spec/blob/master/formats/rbxl.md#properties-chunk
    '''
    if info.chunk_name not in {b'PROP', b'INST'}:
        return None
    return info.chunk_data[0:4]


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
        info.chunk_data[4:8],
        byteorder='little',
    )
    str_start = 8
    return info.chunk_data[str_start:str_start + str_size]


def get_prop_values(info: chunk_info) -> bytes | None:
    '''
    For `PROP`, refer to `Values`.
    https://github.com/RobloxAPI/spec/blob/master/formats/rbxl.md#values
    '''
    if info.chunk_name not in {b'PROP'}:
        return None
    str_size = int.from_bytes(
        info.chunk_data[4:8],
        byteorder='little',
    )
    str_start = 8
    return info.chunk_data[str_start + str_size + 1:]


def get_type_id(info: chunk_info) -> int | None:
    '''
    For `PROP`, refer to `TypeID`.
    https://github.com/RobloxAPI/spec/blob/master/formats/rbxl.md#values
    '''
    if info.chunk_name not in {b'PROP'}:
        return None
    str_size = int.from_bytes(
        info.chunk_data[4:8],
        byteorder='little',
    )
    str_end = 8 + str_size
    return info.chunk_data[str_end]


def get_instance_count(info: chunk_info) -> int | None:
    '''
    For `INST`, refer to `Length`.
    https://github.com/RobloxAPI/spec/blob/master/formats/rbxl.md#instances-chunk
    '''
    if info.chunk_name not in {b'INST'}:
        return None
    str_size = int.from_bytes(
        info.chunk_data[4:8],
        byteorder='little',
    )
    prop_start = 8 + str_size + 1
    return int.from_bytes(
        info.chunk_data[prop_start:prop_start + 4],
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
            class_id = get_class_id(info)
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
