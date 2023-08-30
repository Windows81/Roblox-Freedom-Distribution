from web_server._logic import web_server_handler, server_path
import urllib.parse
import re


@server_path("/.127.0.0.1/game/players/[0-9]+/", regex=True)
def _(self: web_server_handler, match: re.Match[str]) -> bool:
    self.send_json({"ChatFilter": "blacklist"})
    return True


@server_path("/moderation/v2/filtertext")
def _(self: web_server_handler) -> bool:
    length = int(self.headers.get('content-length'))
    field_data = self.rfile.read(length)
    qs = urllib.parse.parse_qs(field_data)

    orig_text = str(qs[b'text'][0], encoding='utf-8')
    mod_text = "".join(reversed(orig_text))
    uid = int(qs[b'userId'][0])

    self.send_json({
        "success": True,
        "message": mod_text,
        "data": {
            "AgeUnder13": mod_text,
            "Age13OrOver": mod_text,
        },
    })
    return True
