import launcher.routines._logic as logic
import dataclasses
import os.path
import os


class obj_type(logic.entry):
    local_args: 'arg_type'

    def check_host(self, full_path: str) -> bool:
        l = len(self.base_url_bytes)
        with open(full_path, 'rb') as f:
            f.seek(12)
            b = f.read(l)
        return b == self.base_url_bytes

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

        for fn in os.listdir(http_folder):
            full_path = os.path.join(http_folder, fn)
            if not self.check_host(full_path):
                continue
            os.remove(full_path)


@dataclasses.dataclass
class arg_type(logic.arg_type):
    obj_type = obj_type

    base_url: str
