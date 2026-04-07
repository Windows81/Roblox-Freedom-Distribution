# Standard library imports
import threading
import os.path
import os


NUM_THREADS = 4


def process(base_url: str) -> int:
    remove_count = 0

    def check_host(full_path: str) -> bool:
        try:
            l = len(base_url_bytes)
            with open(full_path, 'rb') as f:
                f.seek(12)
                b = f.read(l)
            return b == base_url_bytes

        # This error rarely happens when being called by `remove_hosts`.
        except FileNotFoundError:
            return False

    def remove_hosts(full_paths: list[str]) -> None:
        nonlocal remove_count
        for full_path in full_paths:
            if not check_host(full_path):
                continue
            try:
                remove_count += 1
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

    threads = [
        threading.Thread(
            target=remove_hosts,
            args=(full_paths[i::NUM_THREADS],),
            daemon=True,
        )
        for i in range(NUM_THREADS)
    ]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    return remove_count
