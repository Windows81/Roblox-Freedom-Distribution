HEADER_SIGNATURE = 'rfd-redirect\n'


def check(data: bytes) -> bool:
    return data.startswith(HEADER_SIGNATURE)


def parse(data: bytes) -> bytes:
    if not check(data):
        return data
    uri = data[HEADER_SIGNATURE:]
    if uri.startswith('http://') or uri.startswith('https://'):
