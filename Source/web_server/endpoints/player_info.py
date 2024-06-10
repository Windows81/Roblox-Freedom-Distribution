from web_server._logic import web_server_handler, server_path
import storage
import re


@server_path("/users/([0-9]+)", regex=True)
def _(self: web_server_handler, match: re.Match[str]) -> bool:
    '''
    GetUsernameFromUserId
    '''
    database = self.server.database.players

    id_num = match.group(1)
    username = database.get_player_field_from_index(
        database.player_field.ID_NUMBER,
        id_num,
        database.player_field.USERNAME,
    )

    if not username:
        return False

    self.send_json({'Username': username})
    return True


@server_path("/users/get-by-username")
def _(self: web_server_handler) -> bool:
    database = self.server.database.players

    username = self.query['username']
    id_num = database.get_player_field_from_index(
        database.player_field.USERNAME,
        username,
        database.player_field.ID_NUMBER,
    )

    if not id_num:
        return False

    self.send_data(id_num)
    return True


@server_path("/points/get-point-balance")
def _(self: web_server_handler) -> bool:
    # TODO: maybe implement the old player-point sytem.
    self.send_json({"success": True, "pointBalance": 0})
    return True


# TODO: handle social requests.
@server_path('/Game/LuaWebService/HandleSocialRequest.ashx')
def _(self: web_server_handler) -> bool:
    match self.query['method']:
        case 'GetGroupRank':
            self.send_data(
                bytes(f'<Value Type="integer">{255}</Value>', encoding='utf-8'))
            return True

    self.send_json({})
    return True


@server_path('/v2/users/([0-9]+)/groups/roles', regex=True)
def _(self: web_server_handler, match: re.Match[str]) -> bool:
    self.send_json({
        "data": [
            {
                "group": {
                    "id": group_id,
                    "name": "string",
                    "memberCount": 0,
                    "hasVerifiedBadge": True,
                },
                "role": {
                    "id": group_id,
                    "name": "string",
                    "rank": 255,
                },
                "isNotificationsEnabled": True,
            }
            for group_id in [
                1200769,
                2868472,
                4199740,
                4265462,
                4265456,
                4265443,
                4265449,
            ]
        ]
    })
    return True


@server_path('/gametransactions/getpendingtransactions/', min_version=400)
def _(self: web_server_handler) -> bool:
    self.send_json([])
    return True
