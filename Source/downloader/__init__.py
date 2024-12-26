import tqdm_vendored as tqdm
import py7zr.exceptions
import urllib.request
import logger.filter
import util.resource
import util.versions
import util.const
import logger
import py7zr
import io


def get_remote_link(rōblox_version: util.versions.rōblox, bin_type: util.resource.bin_subtype) -> str:
    return util.const.ZIPPED_RELEASE_LINK_FORMAT % (
        util.const.ZIPPED_RELEASE_VERSION,
        rōblox_version.name,
        bin_type.value,
    )


def download(remote_link: str, quiet: bool = False) -> io.BytesIO:
    with urllib.request.urlopen(remote_link) as request_res:
        if request_res.status != 200:
            raise Exception(
                "Failed to download: HTTP Status %d" %
                (request_res.status),
            )

        total_size = int(request_res.info().get('Content-Length').strip())
        downloaded_data = io.BytesIO()

        with tqdm.tqdm(
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
            disable=quiet,
        ) as bar:
            while True:
                chunk = request_res.read(1024)
                if not chunk:
                    break
                downloaded_data.write(chunk)
                bar.update(len(chunk))

    downloaded_data.seek(0)
    return downloaded_data


def bootstrap_binary(
    rōblox_version: util.versions.rōblox,
    bin_type: util.resource.bin_subtype,
    log_filter: logger.filter.filter_type,
) -> None:
    link = get_remote_link(rōblox_version, bin_type)
    response = download(
        remote_link=link,
        quiet=log_filter.other_logs,
    )

    full_dir = util.resource.retr_rōblox_full_path(
        rōblox_version, bin_type,
    )

    logger.log(
        f'Extracting to {full_dir}...',
        context=logger.log_context.PYTHON_SETUP,
        filter=log_filter,
    )
    py7zr.unpack_7zarchive(response, full_dir)
