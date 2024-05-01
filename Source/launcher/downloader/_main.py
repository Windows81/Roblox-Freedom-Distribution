import urllib.request
import util.resource
import util.versions
import util.const
import py7zr
import io


def get_remote_link(rōblox_version: util.versions.rōblox, bin_type: util.resource.bin_subtype) -> str:
    return util.const.GIT_LINK_FORMAT % (
        util.const.GIT_RELEASE_VERSION,
        rōblox_version.name,
        bin_type.value,
    )


def download_binary(rōblox_version: util.versions.rōblox, bin_type: util.resource.bin_subtype) -> None:
    link = get_remote_link(rōblox_version, bin_type)
    res = urllib.request.urlopen(link).read()
    full_dir = util.resource.retr_rōblox_full_path(rōblox_version,  bin_type)
    py7zr.unpack_7zarchive(io.BytesIO(res), full_dir)
