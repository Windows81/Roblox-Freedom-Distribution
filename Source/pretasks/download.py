import functools
import sys
import urllib.request
import shutil
import io
import os
import ssl

# Third-party imports
from vendored import tqdm
import py7zr

# Local application/library specific imports
import util.resource
import util.versions
import util.const
import logger


def get_remote_link(
    rōblox_version: util.versions.rōblox,
    bin_type: util.resource.bin_subtype
) -> str:
    return util.const.ZIPPED_RELEASE_LINK_FORMAT % (
        util.const.ZIPPED_RELEASE_VERSION,
        rōblox_version.name,
        bin_type.value,
    )


def download(remote_link: str, quiet: bool = False) -> io.BytesIO:
    ctx = ssl._create_unverified_context()
    with urllib.request.urlopen(remote_link, context=ctx) as response:
        if response.status != 200:
            raise Exception(
                "Failed to download: HTTP Status %d" %
                (response.status),
            )

        total_size = int(response.info().get('Content-Length').strip())
        downloaded_data = io.BytesIO()

        with tqdm.tqdm(
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
            disable=quiet,
        ) as bar:
            while True:
                chunk = response.read(1024)
                if not chunk:
                    break
                downloaded_data.write(chunk)
                bar.update(len(chunk))

    downloaded_data.seek(0)
    return downloaded_data


def get_full_dir(rōblox_version: util.versions.rōblox, bin_type: util.resource.bin_subtype) -> str:
    return util.resource.retr_rōblox_full_path(rōblox_version, bin_type)


def bootstrap_binary(
    rōblox_version: util.versions.rōblox,
    bin_type: util.resource.bin_subtype,
    log_filter: logger.obj_type,
    force_overwrite: bool = False,
) -> None:
    full_dir = get_full_dir(rōblox_version, bin_type)

    if os.path.isdir(full_dir):
        if force_overwrite:
            shutil.rmtree(full_dir)
        else:
            log_filter.log(
                text='Rōblox installation exists, skipping...',
                context=logger.log_context.PYTHON_SETUP,
            )
            return

    log_filter.log(
        text=(
            'Downloading %s/%s (%s)...' %
            (
                rōblox_version.name,
                bin_type.name,
                util.const.ZIPPED_RELEASE_VERSION,
            )
        ),
        context=logger.log_context.PYTHON_SETUP,
    )

    remote_link = get_remote_link(
        rōblox_version,
        bin_type,
    )

    download_response = download(
        remote_link=remote_link,
        quiet=not log_filter.other_logs,
    )

    log_filter.log(
        text=f'Extracting to {full_dir}...',
        context=logger.log_context.PYTHON_SETUP,
    )
    py7zr.unpack_7zarchive(
        archive=download_response,
        path=full_dir,
    )
