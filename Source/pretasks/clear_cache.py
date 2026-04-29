# Standard library imports
from concurrent.futures import ThreadPoolExecutor
import threading
import os.path
import os


NUM_THREADS = 4


def check_host(base_url_bytes: bytes, full_path: str) -> bool:
    try:
        l = len(base_url_bytes)
        with open(full_path, 'rb') as f:

            # The start of the URL is at address 0xC.
            f.seek(0xC)

            return f.read(l) == base_url_bytes

    # This error rarely happens when being called by `remove_hosts`.
    except FileNotFoundError:
        return False


def remove_hosts(base_url_bytes: bytes, full_path: str) -> None:
    if not check_host(base_url_bytes, full_path):
        return
    try:
        os.remove(full_path)
    except Exception:
        pass


def process(base_url: str) -> int:
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
    return len(list(executor.map(
        lambda full_path: remove_hosts(base_url_bytes, full_path),
        full_paths,
    )))
