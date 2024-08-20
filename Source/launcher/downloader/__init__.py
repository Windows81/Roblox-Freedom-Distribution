import urllib.request
import util.resource
import util.versions
import util.const
import py7zr
import io
from tqdm import tqdm

def get_remote_link(rōblox_version: util.versions.rōblox, bin_type: util.resource.bin_subtype) -> str:
    return util.const.GIT_LINK_FORMAT % (
        util.const.GIT_RELEASE_VERSION,
        rōblox_version.name,
        bin_type.value,
    )

def download_binary(rōblox_version: util.versions.rōblox, bin_type: util.resource.bin_subtype) -> None:
    link = get_remote_link(rōblox_version, bin_type)
    
    try:
        with urllib.request.urlopen(link) as response:
            if response.status != 200:
                raise Exception(f"Failed to download: HTTP Status {response.status}")

            total_size = int(response.info().get('Content-Length').strip())
            res = io.BytesIO()
            
            with tqdm(total=total_size, unit='B', unit_scale=True, unit_divisor=1024, desc="Downloading") as bar:
                while True:
                    chunk = response.read(1024)
                    if not chunk:
                        break
                    res.write(chunk)
                    bar.update(len(chunk))

        res.seek(0)

        full_dir = util.resource.retr_rōblox_full_path(rōblox_version, bin_type)
        
        print(f"Extracting to {full_dir}...")
        try:
            py7zr.unpack_7zarchive(res, full_dir)
            print("Extraction completed successfully.")
        except py7zr.exceptions.Bad7zFile as e:
            raise Exception("Downloaded file is not a valid 7z archive") from e
        except py7zr.exceptions.CrcError as e:
            raise Exception(f"CRC error while extracting file. Error details: {e}") from e

    except Exception as e:
        raise Exception(f"An error occurred: {e}") from e
