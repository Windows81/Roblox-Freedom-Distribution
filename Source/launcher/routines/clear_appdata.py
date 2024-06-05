from . import _logic as logic
import dataclasses
import threading
import os.path
import os

NUM_THREADS = 4


class obj_type(logic.entry):
    local_args: 'arg_type'

    def check_host(self, full_path: str) -> bool:
        l = len(self.base_url_bytes)
        with open(full_path, 'rb') as f:
            f.seek(12)
            b = f.read(l)
        return b == self.base_url_bytes

    def remove_hosts(self, full_paths: list[str]) -> None:
        for full_path in full_paths:
            if not self.check_host(full_path):
                continue
            os.remove(full_path)

    def process(self) -> None:
        self.base_url_bytes = bytes(self.local_args.base_url, encoding='utf-8')
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


@dataclasses.dataclass
class arg_type(logic.arg_type):
    obj_type = obj_type

    base_url: str
