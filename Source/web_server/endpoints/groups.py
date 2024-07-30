from web_server._logic import web_server_handler, server_path
import util.versions as versions
import re


@server_path('/Game/LuaWebService/HandleSocialRequest.ashx')
def _(self: web_server_handler) -> bool:
    match self.query['method']:
        case 'GetGroupRank':
            def get_rank() -> int:
                group_id_str = self.query['groupid']
                user_id_str = self.query['playerid']

                database = self.server.storage.players
                user_code = database.get_player_field_from_index(
                    database.player_field.ID_NUMBER,
                    user_id_str,
                    database.player_field.USER_CODE,
                )

                if user_code is None:
                    return 0
                return self.server.game_config.server_core.retrieve_groups(user_code).get(group_id_str, 0)

            self.send_data(bytes(
                '<Value Type="integer">' +
                str(get_rank()) +
                '</Value>',
                encoding='utf-8'
            ))
            return True

    self.send_json({})
    return True


@server_path('/v2/users/([0-9]+)/groups/roles', regex=True)
def _(self: web_server_handler, match: re.Match[str]) -> bool:
    database = self.server.storage.players
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
