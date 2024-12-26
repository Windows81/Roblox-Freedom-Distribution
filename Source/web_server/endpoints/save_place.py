from web_server._logic import web_server_handler, server_path
from config_type.types import structs, wrappers, callable
import util.const
import shutil
import struct
import gzip
import zlib
import re
import io


def decompress_gzip(data, file_handle) -> None:
    """
    Decompress a gzip compressed string into a file handle.
    Modified from `gzip.decompress` to write directly to disk.
    """
    while True:
        fp = io.BytesIO(data)
        if gzip._read_gzip_header(fp) is None:  # type: ignore
            return
        # Use a zlib raw deflate compressor
        do = zlib.decompressobj(wbits=-zlib.MAX_WBITS)
        # Read all the data except the header
        decompressed = do.decompress(data[fp.tell():])
        if not do.eof or len(do.unused_data) < 8:
            raise EOFError(
                "Compressed file ended before the end-of-stream "
                "marker was reached"
            )
        crc, length = struct.unpack("<II", do.unused_data[:8])
        if crc != zlib.crc32(decompressed):
            raise gzip.BadGzipFile("CRC check failed")
        if length != (len(decompressed) & 0xffffffff):
            raise gzip.BadGzipFile("Incorrect length of data produced")
        file_handle.write(decompressed)
        data = do.unused_data[8:].lstrip(b"\x00")


@server_path(r'/v1/places/(\d+)/symbolic-links', regex=True)
def _(self: web_server_handler, match: re.Match[str]) -> bool:
    '''
    Dummy function to return an empty list of packages.
    Rōblox's "package" feature is not used in RFD.
    '''
    self.send_json({
        "previousPageCursor": None,
        "nextPageCursor": None,
        "data": []
    })
    return True


@server_path("/ide/publish/UploadExistingAsset")
def _(self: web_server_handler) -> bool:
    '''
    game:SavePlace()
    '''
    assert self.is_privileged

    # Returns false if the thing trying to be saved isn't the place we're in.
    if self.query['assetId'] != str(util.const.PLACE_IDEN_CONST):
        return False

    place_config = self.game_config.server_core.place_file
    assert place_config.enable_saveplace

    # Don't save place if the URI is from online.
    if place_config.rbxl_uri.uri_type == wrappers.uri_type.ONLINE:
        return False

    # Backups are important in case RFD crashes mid-save.
    place_path = place_config.rbxl_uri.value
    backup_path = f'{place_path}.bak'
    shutil.copy(place_path, backup_path)

    zipped_content = self.read_content()
    with open(place_path, 'wb') as f:
        decompress_gzip(zipped_content, f)

    self.send_json([])
    return True
