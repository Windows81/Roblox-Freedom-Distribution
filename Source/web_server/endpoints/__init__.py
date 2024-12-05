from web_server._logic import server_path, web_server_handler
from importlib import import_module
import pathlib


for f in pathlib.Path(__file__).parent.glob("*.py"):
    if "__" in f.stem:
        continue
    import_module(f".{f.stem}", __package__)


@server_path("/")
def _(self: web_server_handler) -> bool:
    self.send_data('ÒÓ'.encode('utf-16'))
    return True
