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
    database = self.server.storage.players

    # Manually parsing here since `self.query` isn't automatically populated prior.
    field_data = str(self.read_content(), encoding='utf-8')
    self.query = dict(urllib.parse.parse_qsl(field_data))

    orig_text = self.query['text']
    id_num = self.query['userId']

    user_code = database.get_player_field_from_index(
        database.player_field.ID_NUMBER,
        id_num,
        database.player_field.USER_CODE,
    )
    assert user_code is not None

    mod_text = self.game_config.server_core.filter_text(
        user_code,
        orig_text,
    )

    self.send_json({
        "success": True,
        "message": mod_text,
        "data": {
            "AgeUnder13": mod_text,
            "Age13OrOver": mod_text,
        },
    })
    return True
