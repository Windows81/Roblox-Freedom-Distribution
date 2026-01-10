# Standard library imports
import dataclasses
import os
import os.path
import threading

# Typing imports
from typing import override

# Local application imports
from . import _logic as logic


NUM_THREADS = 4


@dataclasses.dataclass
class obj_type(logic.obj_type):
    base_url: str
    base_url_bytes: bytes = dataclasses.field(init=False)

    def check_host(self, full_path: str) -> bool:
        try:
            l = len(self.base_url_bytes)
            with open(full_path, 'rb') as f:
                f.seek(12)
                b = f.read(l)
            return b == self.base_url_bytes

        # This error rarely happens when being called by `remove_hosts`.
        except FileNotFoundError:
            return False

    def remove_hosts(self, full_paths: list[str]) -> None:
        for full_path in full_paths:
            if not self.check_host(full_path):
                continue
            try:
                os.remove(full_path)
            except Exception:
                pass

    @override
    def process(self) -> None:
        self.base_url_bytes = bytes(self.base_url, encoding='utf-8')
        http_folder = os.path.join(
            os.getenv('LocalAppData', ''),
            'Temp',
            'Roblox',
            'http',
        )

        if not os.path.isdir(http_folder):
            return

        full_paths = [
            os.path.join(http_folder, fn)
            for fn in os.listdir(http_folder)
        ]

        threads = [
            threading.Thread(
                target=self.remove_hosts,
                args=(full_paths[i::NUM_THREADS],),
                daemon=True,
            )
            for i in range(NUM_THREADS)
        ]

        for t in threads:
            t.start()

        for t in threads:
            t.join()
