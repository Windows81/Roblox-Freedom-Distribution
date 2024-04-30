import urllib.request
import util.resource
import util.versions
import util.const
import py7zr
import io


def get_link(rōblox_version: util.versions.rōblox, dir_name: str) -> str:
    return util.const.GIT_LINK_FORMAT % (
        util.const.GIT_RELEASE_VERSION,
        rōblox_version.name,
        dir_name,
    )


def download_binary(rōblox_version: util.versions.rōblox, dir_name: str) -> None:
    res = urllib.request.urlopen(get_link(rōblox_version, dir_name)).read()
    full_dir = util.resource.retr_rōblox_full_path(rōblox_version,  dir_name)
    py7zr.unpack_7zarchive(io.BytesIO(res), full_dir)
