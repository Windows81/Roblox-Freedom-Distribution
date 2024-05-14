import launcher.routines._logic as logic
import dataclasses
import os.path
import os


@dataclasses.dataclass
class _arg_type(logic.arg_type):
    base_url: str


class obj_type(logic.entry):
    local_args: _arg_type

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


class arg_type(_arg_type):
    obj_type = obj_type
