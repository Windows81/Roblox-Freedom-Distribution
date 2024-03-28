from web_server._logic import web_server_handler, server_path
import urllib.parse
import re


@server_path("/game/players/([0-9]+)/", regex=True)
@server_path("/.127.0.0.1/game/players/([0-9]+)/", regex=True)
def _(self: web_server_handler, match: re.Match[str]) -> bool:
    self.send_json({"ChatFilter": "blacklist"})
    return True


@server_path("/moderation/v2/filtertext")
def _(self: web_server_handler) -> bool:
    length = int(self.headers.get('content-length', -1))
    field_data = str(self.rfile.read(length), encoding='utf-8')
    qs = urllib.parse.parse_qs(field_data)

    orig_text = qs['text'][0]
    user_code = self.server.users.get_code_from_id(int(qs['userId'][0])) or ''
    mod_text = self.game_config.server_core.filter_text(user_code, orig_text)

    self.send_json({
        "success": True,
        "message": mod_text,
        "data": {
            "AgeUnder13": mod_text,
            "Age13OrOver": mod_text,
        },
    })
    return True
