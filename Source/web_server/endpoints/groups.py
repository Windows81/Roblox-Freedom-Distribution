from web_server._logic import web_server_handler, server_path
import util.versions as versions
from game_config import obj_type
import re


def get_rank_dict(user_id_num: int, game_config: obj_type) -> dict[str, int]:
    database = game_config.storage.players
    user_code = database.get_player_field_from_index(
        database.player_field.ID_NUMBER,
        user_id_num,
        database.player_field.USER_CODE,
    )
    assert user_code is not None

    return game_config.server_core.retrieve_groups(
        user_id_num, user_code,
    )


@server_path('/Game/LuaWebService/HandleSocialRequest.ashx', versions={versions.rōblox.v348})
def _(self: web_server_handler) -> bool:
    match self.query['method']:
        case 'GetGroupRank':
            group_id_str = self.query['groupid']
            user_id_num = int(self.query['playerid'])
            rank_dict = get_rank_dict(user_id_num, self.game_config)
            rank = rank_dict.get(group_id_str, 0)

            self.send_data(
                b'<Value Type="integer">%d</Value>' %
                (rank),
            )
            return True

    self.send_json({})
    return True


@server_path(r'/v2/users/(\d+)/groups/roles',
             regex=True, versions={versions.rōblox.v463})
def _(self: web_server_handler, match: re.Match[str]) -> bool:
    user_id_num = int(match.group(1))
    groups = get_rank_dict(user_id_num, self.game_config)

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
