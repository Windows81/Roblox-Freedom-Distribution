from web_server._logic import web_server_handler, server_path
import re


@server_path("/users/([0-9]+)", regex=True)
def _(self: web_server_handler, match: re.Match[str]) -> bool:
    id_num = int(match.group(1))
    user_code = self.server.game_config.user_dict.get_code_from_id_num(id_num)
    if not user_code:
        return False

    user_name = self.game_config.server_core.retrieve_username(user_code)
    self.send_json({'Username': user_name})
    return True
