# Standard library imports
import functools
import urllib.request
import shutil
import io
import os

# Third-party imports
import tqdm_vendored as tqdm
import py7zr

# Local application/library specific imports
import logger.filter
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
    with urllib.request.urlopen(remote_link) as response:
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


@functools.cache
def should_overwrite(full_dir: str) -> bool:
    rfd_ver_path = os.path.join(
        full_dir, 'rfd_version',
    )
    if not os.path.isfile(rfd_ver_path):
        version_str = ''
    else:
        with open(rfd_ver_path, 'r') as f:
            version_str = f.read()

    if version_str.startswith(util.const.ZIPPED_RELEASE_VERSION):
        return False

    return input('Should RFD overwrite the `%s`? (y/N) ' % full_dir).lower().startswith('y')


def bootstrap_binary(
    rōblox_version: util.versions.rōblox,
    bin_type: util.resource.bin_subtype,
    log_filter: logger.filter.filter_type,
) -> None:
    full_dir = util.resource.retr_rōblox_full_path(
        rōblox_version, bin_type,
    )

    if os.path.isdir(full_dir):
        if should_overwrite(full_dir):
            shutil.rmtree(full_dir)
        else:
            logger.log(
                text='Rōblox installation exists, skipping...',
                context=logger.log_context.PYTHON_SETUP,
                filter=log_filter,
            )
            return

    logger.log(
        text=(
            'Downloading %s/%s (%s)...' %
            (
                rōblox_version.name,
                bin_type.name,
                util.const.ZIPPED_RELEASE_VERSION,
            )
        ),
        context=logger.log_context.PYTHON_SETUP,
        filter=log_filter,
    )

    remote_link = get_remote_link(
        rōblox_version,
        bin_type,
    )

    download_response = download(
        remote_link=remote_link,
        quiet=not log_filter.other_logs,
    )

    logger.log(
        text=f'Extracting to {full_dir}...',
        context=logger.log_context.PYTHON_SETUP,
        filter=log_filter,
    )
    py7zr.unpack_7zarchive(
        archive=download_response,
        path=full_dir,
    )
