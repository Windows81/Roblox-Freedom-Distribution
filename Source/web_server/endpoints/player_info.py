from web_server._logic import web_server_handler, server_path
import util.versions as versions
import re


@server_path("/v1/users/([0-9]+)/friends", regex=True, versions={versions.rōblox.v463}, commands={'POST', 'GET'})
def _(self: web_server_handler, match: re.Match[str]) -> bool:
    '''
    Dummy endpoint for 2021E.
    Script 'Chat.ChatModules.FriendJoinNotifier', Line 46
    '''
    self.send_json({"data": []})
    return True


@server_path("/users/([0-9]+)", regex=True)
def _(self: web_server_handler, match: re.Match[str]) -> bool:
    '''
    GetUsernameFromUserId
    '''
    database = self.server.storage.players

    id_num = match.group(1)
    username = database.get_player_field_from_index(
        database.player_field.ID_NUMBER,
        id_num,
        database.player_field.USERNAME,
    )
    assert username is not None

    self.send_json({'Username': username})
    return True


@server_path("/users/get-by-username")
def _(self: web_server_handler) -> bool:
    database = self.server.storage.players

    username = self.query['username']
    id_num = database.get_player_field_from_index(
        database.player_field.USERNAME,
        username,
        database.player_field.ID_NUMBER,
    )
    assert id_num is not None

    self.send_data(id_num)
    return True


@server_path("/points/get-point-balance")
def _(self: web_server_handler) -> bool:
    # TODO: maybe implement the old player-point sytem.
    self.send_json({"success": True, "pointBalance": 0})
    return True
