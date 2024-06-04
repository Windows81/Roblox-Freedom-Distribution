from typing_extensions import Callable
import dataclasses
import itertools
import lz4.block
import lz4
import io
import re


HEADER_SIGNATURE = b'\x3c\x72\x6f\x62\x6c\x6f\x78\x21\x89\xff\x0d\x0a\x1a\x0a'


def parse_header(stream: io.BytesIO):
    signature = stream.read(len(HEADER_SIGNATURE))
    if signature != HEADER_SIGNATURE:
        return None

    format_version = stream.read(2)
    class_count = stream.read(4)
    instance_count = stream.read(4)
    reserved_metadata = stream.read(8)
    return b''.join([
        signature,
        format_version,
        class_count,
        instance_count,
        reserved_metadata,
    ])

# TODO: replace:
# 50 52 4F 50 5A 00 00 00 72 00 00 00 00 00 00 00 FF 36 00 00 00 00 08 00 00 00 46 6F 6E 74 46 61 63 65 20 2C 00 00 00 72 62 78 61 73 73 65 74 3A 2F 2F 66 6F 6E 74 73 2F 66 61 6D 69 6C 69 65 73 2F 53 6F 75 72 63 65 53 61 6E 73 50 72 6F 2E 6A 73 6F 6E 90 01 00 2A 33 00 01 09 2A 00 C0 2D 52 65 67 75 6C 61 72 2E 74 74 66
# with
# 50 52 4F 50 13 00 00 00 11 00 00 00 00 00 00 00 F0 02 00 00 00 00 04 00 00 00 46 6F 6E 74 12 00 00 00 03


class string_replacer:
    INT_SIZE = 4

    @dataclasses.dataclass
    class input_info:
        match: re.Match[bytes]
        string_size: int
        match_size: int
        match_bytes: bytes
        remainder: bytes
        match_start: int
        match_end: int

    def __init__(
        self,
        pattern: bytes,
        replacement_func: Callable[[re.Match[bytes]], bytes],
        chunk_data: bytes,
        num_replacements: int | None = None,
        prepend_new_length: bool = True,
    ) -> None:
        self.data = chunk_data

        self.pattern = pattern
        self.replacement_func = replacement_func
        self.num_replacements = num_replacements
        self.prepend_new_length = prepend_new_length

    def calc(self) -> bytes:
        # Performs replacement twice to account for
        infos = [
            info
            for match in itertools.islice(
                re.finditer(
                    br'(.{%d})(?=%s)' % (self.INT_SIZE, self.pattern),
                    self.data,
                ),
                self.num_replacements,
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
        string_pos = match_start + self.INT_SIZE

        string_size = int.from_bytes(
            self.data[match_start:string_pos],
            byteorder='little',
        )
        if string_size >= 1024:
            return None

        arg_bytes = arg.group()[self.INT_SIZE:]
        new_match = re.match(
            self.pattern,
            arg.string[string_pos:string_pos+string_size],
        )
        if not new_match:
            return None

        new_match_bytes = new_match.group()
        new_match_size = len(new_match_bytes)
        match_end = match_start + self.INT_SIZE + new_match_size
        return string_replacer.input_info(
            match=new_match,
            string_size=string_size,
            match_size=new_match_size,
            match_bytes=new_match_bytes,
            remainder=arg_bytes[new_match_size:],
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
        suffix = info.remainder

        return b''.join([
            prefix,
            result,
            suffix,
        ])


def get_prop_name(data: bytes) -> bytes:
    size = int.from_bytes(
        data[4:8],
        byteorder='little',
    )
    return data[8:8+size]


def replace_rōblox_links(chunk_data: bytes) -> bytes:
    '''
    Redirects `assetdelivery.roblox.com` links within any `rbxm` data container to your local URL.
    '''
    replacer = string_replacer(
        br'https://assetdelivery\.roblox\.com/(v1/asset/?\?id=([0-9]+))',
        lambda m: b'rbxassetid://%s' % m.group(2),
        chunk_data,
    )
    return replacer.calc()


def replace_font_faces(chunk_data: bytes):
    if get_prop_name(chunk_data) != b'FontFace':
        return chunk_data

    class_id = chunk_data[0:4]
    prop_info = b'\x04\x00\x00\x00Font\x12'
    # len(class_id + b'\x08\x00\x00\x00FontFace\x20') == 17
    chunk_values = chunk_data[17:]

    enum_values = [
        (3).to_bytes(length=1)
        for m in re.finditer(
            br'.\x00\x00\x00rbxasset://fonts/([^\.]+\.json)' +
            br'.{4}\x00\x00\x00rbxasset://fonts/(.+?)tf',
            chunk_values,
        )
    ]

    return b''.join([
        class_id,
        prop_info,
        b'\x00'*len(enum_values)*3,
        *enum_values,
    ])


def parse_chunk(stream: io.BytesIO):
    chunk_name = stream.read(4)
    if chunk_name == b'':
        return None

    compressed_size = int.from_bytes(
        stream.read(4),
        byteorder='little',
    )
    uncompressed_size = int.from_bytes(
        stream.read(4),
        byteorder='little',
    )
    reserved_metadata = stream.read(4)

    # TODO: learn from https://github.com/jmkd3v/rbxl/blob/a36eb799f596a68ab2130876f5021a76bb6726d4/rbxl/binary/chunks/__init__.py#L7.
    if compressed_size == 0:
        chunk_data = stream.read(uncompressed_size)

    else:
        chunk_data = lz4.block.decompress(
            source=stream.read(compressed_size),
            uncompressed_size=uncompressed_size,
        )

    chunk_data = replace_rōblox_links(chunk_data)
    chunk_data = replace_font_faces(chunk_data)
    new_size = len(chunk_data)

    if new_size != uncompressed_size:
        print(f'PROP CHANGED: {get_prop_name(chunk_data)}')

    return b''.join([
        chunk_name,
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
        reserved_metadata,
        chunk_data,
    ])


def parse(data: bytes):
    read_stream = io.BytesIO(data)
    write_stream = io.BytesIO()

    header = parse_header(read_stream)
    if not header:
        return data
    write_stream.write(header)

    while True:
        chunk_data = parse_chunk(read_stream)
        if not chunk_data:
            break
        write_stream.write(chunk_data)

    return write_stream.getvalue()
