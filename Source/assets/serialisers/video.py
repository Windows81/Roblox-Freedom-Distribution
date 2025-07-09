import urllib.request
import re

HEADER_SIGNATURE = b'#EXTM3U'


def check(data: bytes) -> bool:
    return data.startswith(HEADER_SIGNATURE)


def get_m3u8_links(data: bytes) -> list[str]:
    format_dict = {}
    for line in data.decode('utf-8').splitlines(keepends=False):
        if line.startswith('#EXT-X-DEFINE:NAME'):
            match = re.match(
                r'#EXT-X-DEFINE:NAME="([^"]+)",VALUE="([^"]+)"',
                line,
            )
            assert match is not None
            name, value = match.group(1, 2)
            format_dict[f'${name}'] = value

        elif not line.startswith('#'):
            url = line.format_map(format_dict)
            with urllib.request.urlopen(url) as response:
                prefix = url.rsplit('/', 1)[0]
                return [
                    f'{prefix}/{line.decode('utf-8')}'
                    for line in response.read().splitlines(keepends=False)
                    if line.endswith(b'.webm')
                ]
    return []


def parse(data: bytes) -> bytes | None:
    if not check(data):
        return
    concat_data = []
    for url in get_m3u8_links(data):
        with urllib.request.urlopen(url) as response:
            concat_data.append(response.read())
    return b''.join(concat_data)
