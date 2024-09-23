from web_server._logic import web_server_handler, server_path
from game import obj_type as game
import util.versions as versions
import re


def get_rank_dict(user_id_num: int, game_data: game) -> dict[str, int]:
    database = game_data.storage.players
    user_code = database.get_player_field_from_index(
        database.player_field.ID_NUMBER,
        user_id_num,
        database.player_field.USER_CODE,
    )
    assert user_code is not None

    return game_data.config.server_core.retrieve_groups(
        user_id_num, user_code,
    )


@server_path('/Game/LuaWebService/HandleSocialRequest.ashx', versions={versions.rōblox.v348})
def _(self: web_server_handler) -> bool:
    match self.query['method']:
        case 'GetGroupRank':
            group_id_str = self.query['groupid']
            user_id_num = int(self.query['playerid'])
            rank_dict = get_rank_dict(user_id_num, self.game_data)
            rank = rank_dict.get(group_id_str, 0)

            self.send_data(
                b'<Value Type="integer">%d</Value>' %
                (rank),
            )
            return True

    self.send_json({})
    return True


@server_path('/v2/users/([0-9]+)/groups/roles', regex=True, versions={versions.rōblox.v463})
def _(self: web_server_handler, match: re.Match[str]) -> bool:
    user_id_num = int(match.group(1))
    groups = get_rank_dict(user_id_num, self.game_data)

    self.send_json({
        "data": [
            {
                "group": {
                    "id": int(group_id),
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
