import launcher.subparsers.aux_tasks._logic
import os.path
import os


class obj_type(launcher.subparsers.aux_tasks._logic.action):
    HTTP_FOLDER = os.path.join(os.getenv('LocalAppData'), 'Temp', 'Roblox', 'http')

    def __init__(self, base_url: str):
        super().__init__()
        self.base_url = bytes(base_url, encoding='utf-8')

    def check_host(self, full_path: str) -> bool:
        l = len(self.base_url)
        with open(full_path, 'rb') as f:
            f.seek(12)
            b = f.read(l)
        return b == self.base_url

    def initialise(self):
        for fn in os.listdir(self.HTTP_FOLDER):
            full_path = os.path.join(self.HTTP_FOLDER, fn)
            if not self.check_host(full_path):
                continue
            os.remove(full_path)
