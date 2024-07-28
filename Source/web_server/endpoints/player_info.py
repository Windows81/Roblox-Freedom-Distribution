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
    database = self.server.database.players

    id_num = match.group(1)
    username = database.get_player_field_from_index(
        database.player_field.ID_NUMBER,
        id_num,
        database.player_field.USERNAME,
    )

    if username is None:
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

    if id_num is None:
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
            def get_rank() -> int:
                group_id_str = self.query['groupid']
                user_id_str = self.query['playerid']

                database = self.server.database.players
                user_code = database.get_player_field_from_index(
                    database.player_field.ID_NUMBER,
                    user_id_str,
                    database.player_field.USER_CODE,
                )

                if user_code is None:
                    return 0
                return self.server.game_config.server_core.retrieve_groups(user_code).get(group_id_str, 0)

            self.send_data(
                bytes(f'<Value Type="integer">{get_rank()}</Value>', encoding='utf-8'))
            return True

    self.send_json({})
    return True


@server_path('/v2/users/([0-9]+)/groups/roles', regex=True)
def _(self: web_server_handler, match: re.Match[str]) -> bool:
    database = self.server.database.players
    user_id_num = int(match.group(1))

    user_code = database.get_player_field_from_index(
        database.player_field.ID_NUMBER,
        user_id_num,
        database.player_field.USER_CODE,
    )
    if not user_code:
        return False

    groups = self.server.game_config.server_core.retrieve_groups(user_code)

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
                    "id": int(group_id),
                    "rank": group_rank,
                    "name": "string",
                },
                "isNotificationsEnabled": True,
            }
            for group_id, group_rank in groups.items()
        ]
    })
    return True


@server_path('/gametransactions/getpendingtransactions/')
def _(self: web_server_handler) -> bool:
    '''
    Something to do with developer products.
    Won't be implemented in RFD right now.
    https://github.com/InnitGroup/syntaxsource/blob/71ca82651707ad88fb717f3cc5e106ff62ac3013/syntaxwebsite/app/routes/gametransactions.py#L8
    '''
    self.send_json([])
    return True


@server_path('/v1/users/([0-9]+)/items/gamepass/([0-9]+)', regex=True)
def _(self: web_server_handler, match: re.Match[str]) -> bool:
    '''
    https://github.com/SushiDesigner/Meteor-back/blob/dc561b5af196ca9c375530d30d593fc8d7f0486c/routes/marketplace.js#L129
    '''
    user_id_num = int(match.group(1))
    gamepass_id = int(match.group(2))
    gamepass_catalogue = self.server.game_config.remote_data.gamepasses

    has_gamepass = self.server.database.gamepasses.check(
        user_id_num,
        gamepass_id,
    )

    data = (
        [
            {
                "type": "GamePass",
                "id": gamepass_id,
                "name": gamepass_catalogue.get(gamepass_id),
                "instanceId": None,
            }
        ]
        if has_gamepass else
        []
    )

    self.send_json({
        "previousPageCursor": None,
        "nextPageCursor": None,
        "data": data,
    })
    return True
