# Standard library imports
from concurrent.futures import ThreadPoolExecutor
import threading
import os.path
import os


NUM_THREADS = 4


def process(base_url: str) -> int:

    def check_host(full_path: str) -> bool:
        try:
            l = len(base_url_bytes)
            with open(full_path, 'rb') as f:

                # The start of the URL is at address 0xC.  Seeks 0x4 more bytes ahead to skip `http` string.
                f.seek(0xC + 0x4)

                # Quickly seeks to the hostname, accounting for whether the URL begins with `http://` or `https://`.
                match f.read(0x2):
                    case b's:':
                        f.seek(2, os.SEEK_CUR)
                    case b':/':
                        f.seek(3, os.SEEK_CUR)
                    case _:
                        return False
                b = f.read(l)
            return b == base_url_bytes

        # This error rarely happens when being called by `remove_hosts`.
        except FileNotFoundError:
            return False

    def remove_hosts(full_path: str) -> None:
        if not check_host(full_path):
            return
        try:
            os.remove(full_path)
        except Exception:
            pass

    base_url_bytes = bytes(base_url, encoding='utf-8')
    http_folder = os.path.join(
        os.getenv('LocalAppData', ''),
        'Temp',
        'Roblox',
        'http',
    )

    if not os.path.isdir(http_folder):
        return 0

    full_paths = [
        os.path.join(http_folder, fn)
        for fn in os.listdir(http_folder)
    ]

    executor = ThreadPoolExecutor(NUM_THREADS)
    return len(list(executor.map(remove_hosts, full_paths)))
