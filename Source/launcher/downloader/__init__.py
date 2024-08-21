import py7zr.exceptions
import tqdm.std as tqdm
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


def download(link: str) -> io.BytesIO:
    with urllib.request.urlopen(link) as response:
        if response.status != 200:
            raise Exception(
                "Failed to download: HTTP Status %d" %
                (response.status),
            )

        total_size = int(response.info().get('Content-Length').strip())
        response = io.BytesIO()

        with tqdm.tqdm(
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
            desc="Downloading",
        ) as bar:
            while True:
                chunk = response.read(1024)
                if not chunk:
                    break
                response.write(chunk)
                bar.update(len(chunk))

    response.seek(0)
    return response


def bootstrap_binary(rōblox_version: util.versions.rōblox, bin_type: util.resource.bin_subtype) -> None:
    link = get_remote_link(rōblox_version, bin_type)
    response = download(link)

    full_dir = util.resource.retr_rōblox_full_path(
        rōblox_version, bin_type,
    )

    print(f"Extracting to {full_dir}...")
    py7zr.unpack_7zarchive(response, full_dir)
    print("Done.")
