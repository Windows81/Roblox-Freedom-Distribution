from ..logic import webserver_handler, server_path
import re


@server_path("/.127.0.0.1/game/players/[0-9]+/", regex=True)
def _(self: webserver_handler, match: re.Match[str]) -> bool:
    self.send_json({"ChatFilter": "blacklist"})
    return True
