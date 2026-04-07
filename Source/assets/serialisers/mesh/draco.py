import dataclasses
import struct
import math


@dataclasses.dataclass
class Attribute:
    attributeType: int
    dataType: int
    numComponents: int
    normalized: int
    uniqueId: int
    decoderType: int
    output: list[int] | list[float]


@dataclasses.dataclass
class Decoder:
    attributes: list[Attribute]
    pointIds: list[int]
    index:  int


class Parser:
    rans: 'RANSDecoder'
    bits_value: int
    bits_length: int
    numFaces: int
    numPoints: int
    attributes: list[Attribute]
    decoders: list[Decoder]
    faces: list[int]


class ByteReader:
    """Binary file reader with support for various data types"""

    def __init__(self, data: bytes):
        self.data = data
        self.index = 0
        self.length = len(data)

    def get_remaining(self) -> int:
        return self.length - self.index

    def get_index(self) -> int:
        return self.index

    def set_index(self, n: int):
        self.index = n

    def jump(self, n: int):
        self.index += n

    def array(self, n: int) -> bytes:
        result = self.data[self.index:self.index + n]
        self.index += n
        return result

    def uint8(self) -> int:
        val = self.data[self.index]
        self.index += 1
        return val

    def uint16_le(self) -> int:
        val = struct.unpack('<H', self.data[self.index:self.index + 2])[0]
        self.index += 2
        return val

    def uint32_le(self) -> int:
        val = struct.unpack('<I', self.data[self.index:self.index + 4])[0]
        self.index += 4
        return val

    def float_le(self) -> float:
        val = struct.unpack('<f', self.data[self.index:self.index + 4])[0]
        self.index += 4
        return val

    def string(self, n: int) -> str:
        return self.array(n).decode('latin1')

    def find_byte(self, byte: int, start: int) -> int:
        """Find the index of a byte starting from a position"""
        try:
            return self.data.index(byte, start)
        except ValueError:
            return -1


class DracoBitstream:
    """Draco bitstream decoder for compressed mesh data"""

    # Constants
    TRIANGULAR_MESH = 1
    MESH_SEQUENTIAL_ENCODING = 0
    SEQUENTIAL_UNCOMPRESSED_INDICES = 1

    SEQUENTIAL_ATTRIBUTE_ENCODER_GENERIC = 0
    SEQUENTIAL_ATTRIBUTE_ENCODER_INTEGER = 1
    SEQUENTIAL_ATTRIBUTE_ENCODER_QUANTIZATION = 2
    SEQUENTIAL_ATTRIBUTE_ENCODER_NORMALS = 3

    PREDICTION_NONE = -2
    PREDICTION_DIFFERENCE = 0

    PREDICTION_TRANSFORM_DELTA = 0
    PREDICTION_TRANSFORM_WRAP = 1
    PREDICTION_TRANSFORM_NORMAL_OCTAHEDRON_CANONICALIZED = 3

    @staticmethod
    def leb128(stream: ByteReader) -> int:
        """Decode LEB128 (Little Endian Base 128) variable-length integer"""
        result = 0
        shift = 0
        while True:
            value = stream.uint8()
            result |= (value & 0x7F) << shift
            shift += 7
            if not (value & 0x80):
                break
        return result

    @staticmethod
    def parse(stream: ByteReader) -> Parser:
        """Parse Draco compressed mesh data"""

        parser = Parser()

        # Parse header
        magic = stream.string(5)
        if magic != "DRACO":
            raise ValueError("Invalid Draco bitstream")

        major_version = stream.uint8()
        minor_version = stream.uint8()
        encoder_type = stream.uint8()
        encoder_method = stream.uint8()
        flags = stream.uint16_le()

        print(
            f"DRACO {major_version}.{minor_version} | encoderType: {encoder_type}, encoderMethod: {encoder_method}")

        if encoder_type != DracoBitstream.TRIANGULAR_MESH:
            raise NotImplementedError(
                "Only triangular mesh encoding supported")

        if flags & 0x8000:  # METADATA_FLAG_MASK
            raise NotImplementedError("Metadata not supported")

        # Decode connectivity
        DracoBitstream._decode_connectivity(stream, parser, encoder_method)

        # Decode attributes
        DracoBitstream._decode_attribute_data(stream, parser, encoder_method)

        # Generate sequence
        DracoBitstream._generate_sequence(parser, encoder_method)

        # Decode attributes
        DracoBitstream._decode_attributes(stream, parser)

        parser.attributes = parser.decoders[-1].attributes

        return parser

    @staticmethod
    def _decode_connectivity(stream: ByteReader, parser: Parser, encoder_method: int):
        """Decode mesh connectivity (faces)"""
        if encoder_method == DracoBitstream.MESH_SEQUENTIAL_ENCODING:
            num_faces = DracoBitstream.leb128(stream)
            num_points = DracoBitstream.leb128(stream)
            connectivity_method = stream.uint8()

            parser.numFaces = num_faces
            parser.numPoints = num_points

            faces = []

            if connectivity_method != DracoBitstream.SEQUENTIAL_UNCOMPRESSED_INDICES:
                if num_points < (1 << 8):
                    for _ in range(num_faces):
                        faces.extend([
                            stream.uint8(),
                            stream.uint8(),
                            stream.uint8(),
                        ])
                elif num_points < (1 << 16):
                    for _ in range(num_faces):
                        faces.extend([
                            stream.uint16_le(),
                            stream.uint16_le(),
                            stream.uint16_le(),
                        ])
                elif num_points < (1 << 21):
                    for _ in range(num_faces):
                        faces.extend([
                            DracoBitstream.leb128(stream),
                            DracoBitstream.leb128(stream),
                            DracoBitstream.leb128(stream),
                        ])
                else:
                    for _ in range(num_faces):
                        faces.extend([
                            stream.uint32_le(),
                            stream.uint32_le(),
                            stream.uint32_le(),
                        ])
            else:
                raise NotImplementedError("Compressed indices not supported")

            parser.faces = faces
        else:
            raise NotImplementedError("Only sequential encoding supported")

    @staticmethod
    def _decode_attribute_data(stream: ByteReader, parser: Parser, encoder_method: int):
        """Decode attribute metadata"""
        num_decoders = stream.uint8()

        decoders = list[Decoder]()
        for i in range(num_decoders):
            decoders.append(Decoder(
                attributes=[],
                pointIds=[],
                index=i,
            ))

        for decoder in decoders:
            num_attributes = DracoBitstream.leb128(stream)

            attributes = list[Attribute]()
            for _ in range(num_attributes):
                attributes.append(Attribute(
                    attributeType=stream.uint8(),
                    dataType=stream.uint8(),
                    numComponents=stream.uint8(),
                    normalized=stream.uint8(),
                    uniqueId=DracoBitstream.leb128(stream),
                    decoderType=-1,
                    output=[],
                ))

            for attr in attributes:
                attr.decoderType = stream.uint8()

            decoder.attributes = attributes

        parser.decoders = decoders

    @staticmethod
    def _generate_sequence(parser: Parser, encoder_method: int):
        """Generate point ID sequence"""
        if encoder_method == DracoBitstream.MESH_SEQUENTIAL_ENCODING:
            for decoder in parser.decoders:
                decoder.pointIds = list(range(parser.numPoints))
        else:
            raise NotImplementedError("Only sequential encoding supported")

    @staticmethod
    def _decode_attributes(stream: ByteReader, parser: Parser):
        """Decode attribute values"""
        # Initialize RANS decoder
        rans = DracoBitstream._create_rans()
        parser.rans = rans
        parser.bits_value = 0
        parser.bits_length = 0

        for decoder in parser.decoders:
            for attribute in decoder.attributes:
                decoder_type = attribute.decoderType

                if decoder_type == DracoBitstream.SEQUENTIAL_ATTRIBUTE_ENCODER_GENERIC:
                    DracoBitstream._decode_attribute_generic(
                        stream, parser, decoder, attribute)
                else:
                    DracoBitstream._decode_attribute_compressed(
                        stream, parser, decoder, attribute, decoder_type)

            # Transform attributes
            for attribute in decoder.attributes:
                decoder_type = attribute.decoderType

                if decoder_type == DracoBitstream.SEQUENTIAL_ATTRIBUTE_ENCODER_QUANTIZATION:
                    DracoBitstream._decode_and_transform_quantized(
                        stream, parser, decoder, attribute)
                elif decoder_type == DracoBitstream.SEQUENTIAL_ATTRIBUTE_ENCODER_NORMALS:
                    DracoBitstream._decode_and_transform_normals(
                        stream, parser, decoder, attribute)
                else:
                    DracoBitstream._transform_generic(
                        parser, decoder, attribute)

    @staticmethod
    def _decode_attribute_generic(stream: ByteReader, parser: Parser, decoder: Decoder, attribute: Attribute):
        """Decode generic (uncompressed) attribute"""
        num_entries = len(decoder.pointIds)
        num_components = attribute.numComponents
        num_values = num_entries * num_components

        output = []
        data_type = attribute.dataType

        # Data type sizes: 1=INT8, 2=UINT8, 3=INT16, 4=UINT16, 5=INT32, 6=UINT32, 9=FLOAT32
        if data_type in (1, 2):  # 1 byte
            for _ in range(num_values):
                output.append(stream.uint8())
        elif data_type in (3, 4):  # 2 bytes
            for _ in range(num_values):
                output.append(stream.uint16_le())
        elif data_type in (5, 6, 9):  # 4 bytes
            for _ in range(num_values):
                output.append(stream.uint32_le())
        else:
            raise NotImplementedError(f"Data type {data_type} not implemented")

        attribute.output = output

    @staticmethod
    def _decode_attribute_compressed(stream: ByteReader, parser: Parser, decoder: Decoder, attribute: Attribute, decoder_type: int):
        """Decode compressed attribute with prediction"""
        num_entries = len(decoder.pointIds)
        num_components = attribute.numComponents
        num_values = num_entries * num_components

        # Read prediction scheme
        prediction_scheme = stream.uint8()
        if prediction_scheme < 0:
            prediction_scheme = prediction_scheme + 256  # Handle signed byte
        if prediction_scheme >= 128:
            prediction_scheme = prediction_scheme - 256

        # Read prediction transform
        prediction_transform = stream.uint8()
        if prediction_transform >= 128:
            prediction_transform = prediction_transform - 256

        if decoder_type == DracoBitstream.SEQUENTIAL_ATTRIBUTE_ENCODER_INTEGER:
            # Simple integer encoding
            output = DracoBitstream._decode_symbols(stream, parser, num_values)
            attribute.output = output

            # Apply prediction
            if prediction_scheme == DracoBitstream.PREDICTION_DIFFERENCE:
                DracoBitstream._apply_prediction_difference(
                    attribute, num_components, num_entries)
        else:
            # For other encoder types, use simplified decoding
            output = DracoBitstream._decode_symbols(stream, parser, num_values)
            attribute.output = output

            if prediction_scheme == DracoBitstream.PREDICTION_DIFFERENCE:
                DracoBitstream._apply_prediction_difference(
                    attribute, num_components, num_entries)

    @staticmethod
    def _decode_symbols(stream: ByteReader, parser: Parser, num_values: int) -> list[int]:
        """Decode symbols using RANS"""
        rans = parser.rans

        # Read bit length
        bit_length = stream.uint8()

        # Initialize RANS for symbols
        rans.init_symbols(stream, bit_length)

        # Decode values
        output = []
        for _ in range(num_values):
            output.append(rans.read_symbol())

        return output

    @staticmethod
    def _apply_prediction_difference(attribute: Attribute, num_components: int, num_entries: int):
        """Apply differential prediction to decode values"""
        output = attribute.output

        for i in range(num_components, len(output)):
            output[i] = (output[i] + output[i - num_components]) & 0xFFFFFFFF

    @staticmethod
    def _decode_and_transform_quantized(stream: ByteReader, parser: Parser, decoder: Decoder, attribute: Attribute):
        """Decode and dequantize attribute values"""
        num_components = attribute.numComponents
        output = attribute.output

        # Read quantization parameters
        min_values = [stream.float_le() for _ in range(num_components)]
        range_val = stream.float_le()
        quantization_bits = stream.uint8()

        max_quantized = (1 << quantization_bits) - 1
        delta = range_val / max_quantized

        # Dequantize
        for i in range(0, len(output), num_components):
            for j in range(num_components):
                output[i + j] = min_values[j] + output[i + j] * delta

    @staticmethod
    def _decode_and_transform_normals(stream: ByteReader, parser: Parser, decoder: Decoder, attribute: Attribute):
        """Decode and transform octahedron-encoded normals"""
        input_data = attribute.output
        quantization_bits = stream.uint8()

        max_value = (1 << quantization_bits) - 2
        dequantization_scale = 2.0 / max_value

        output = []
        for i in range(0, len(input_data), 2):
            s = input_data[i]
            t = input_data[i + 1]

            y = s * dequantization_scale - 1.0
            z = t * dequantization_scale - 1.0
            x = 1.0 - abs(y) - abs(z)

            x_offset = max(0, -x)
            y += x_offset if y < 0 else -x_offset
            z += x_offset if z < 0 else -x_offset

            norm_squared = x*x + y*y + z*z

            if norm_squared < 1e-6:
                output.extend([0, 0, 0])
            else:
                d = 1.0 / math.sqrt(norm_squared)
                output.extend([x * d, y * d, z * d])

        attribute.output = output

    @staticmethod
    def _transform_generic(parser: Parser, decoder: Decoder, attribute: Attribute):
        """Transform generic attributes (convert uint32 to float)"""
        output = attribute.output
        data_type = attribute.dataType

        if data_type == 9:  # FLOAT32
            for i in range(len(output)):
                # Convert uint32 bits to float
                output[i] = struct.unpack('f', struct.pack('I', output[i]))[0]

    @staticmethod
    def _create_rans():
        """Create RANS decoder object"""
        return RANSDecoder()


class RANSDecoder:
    """rANS (range Asymmetric Numeral Systems) decoder"""

    def __init__(self):
        self.probability_table = []
        self.lookup_table = []
        self.buffer = []
        self.start_index = 0
        self.offset = 0
        self.state = 0
        self.base = 0
        self.precision = 0
        self.prob_zero = 0

    def decode_tables(self, stream: ByteReader, expected_cum_prob: int):
        """Decode probability tables"""
        num_symbols = DracoBitstream.leb128(stream)

        self.probability_table = []
        self.lookup_table = [0] * expected_cum_prob

        cum_prob = 0
        act_prob = 0

        i = 0
        while i < num_symbols:
            data = stream.uint8()
            token = data & 3

            if token == 3:
                offset = data >> 2
                for j in range(offset + 1):
                    self.probability_table.append(
                        {'prob': 0, 'cum_prob': cum_prob})
                i += offset
            else:
                prob = data >> 2
                for j in range(token):
                    eb = stream.uint8()
                    prob |= eb << (8 * (j + 1) - 2)

                self.probability_table.append(
                    {'prob': prob, 'cum_prob': cum_prob})
                cum_prob += prob

                for j in range(act_prob, cum_prob):
                    self.lookup_table[j] = i

                act_prob = cum_prob

            i += 1

        if cum_prob != expected_cum_prob:
            raise ValueError(
                f"Probability mismatch: {cum_prob} != {expected_cum_prob}")

    def _start(self, buffer: bytes, start_index: int, offset: int, base: int, precision: int):
        """Initialize RANS state"""
        self.buffer = buffer
        self.start_index = start_index
        self.base = base
        self.precision = precision

        x = buffer[start_index + offset - 1] >> 6

        if x == 0:
            self.offset = offset - 1
            self.state = buffer[start_index + offset - 1] & 0x3F
        elif x == 1:
            self.offset = offset - 2
            self.state = ((buffer[start_index + offset - 1] << 8) |
                          buffer[start_index + offset - 2]) & 0x3FFF
        elif x == 2:
            self.offset = offset - 3
            self.state = ((buffer[start_index + offset - 1] << 16) |
                          (buffer[start_index + offset - 2] << 8) |
                          buffer[start_index + offset - 3]) & 0x3FFFFF
        elif x == 3:
            self.offset = offset - 4
            self.state = ((buffer[start_index + offset - 1] << 24) |
                          (buffer[start_index + offset - 2] << 16) |
                          (buffer[start_index + offset - 3] << 8) |
                          buffer[start_index + offset - 4]) & 0x3FFFFFFF

        self.state += base

    def read_symbol(self) -> int:
        """Read next symbol"""
        while self.state < self.base and self.offset > 0:
            self.state = (
                (self.state << 8) |
                self.buffer[self.start_index + self.offset - 1]
            )
            self.offset -= 1

        quo = self.state // self.precision
        rem = self.state % self.precision

        symbol = self.lookup_table[rem]
        entry = self.probability_table[symbol]
        prob = entry['prob']
        cum_prob = entry['cum_prob']

        self.state = quo * prob + rem - cum_prob
        return symbol

    def init_symbols(self, stream: ByteReader, bit_length: int):
        """Initialize for symbol decoding"""
        precision_bits = (3 * bit_length) // 2
        precision_bits = max(12, min(20, precision_bits))

        precision = 1 << precision_bits
        base = precision * 4

        self.decode_tables(stream, precision)

        data_size = DracoBitstream.leb128(stream)
        buffer = stream.array(data_size)

        self._start(buffer, 0, data_size, base, precision)
