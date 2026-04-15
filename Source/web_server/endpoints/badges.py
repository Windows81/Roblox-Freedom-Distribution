from .._logic import web_server_handler, server_path
import util.versions as versions
import re


@server_path('/Game/Badge/HasBadge.ashx', commands={'GET'}, versions={versions.rōblox.v347})
def _(self: web_server_handler) -> bool:
    user_id_num = int(self.query.get("UserID", 0))
    badge_id = self.query.get("BadgeID", "0")

    database = self.server.storage.badges
    self.send_data("Success" if database.check(user_id_num, int(badge_id)) is not None else "Failure")

    return True

@server_path('/assets/award-badge')
def _(self: web_server_handler) -> bool:
    user_id_num = int(self.query.get("userId", 0))
    badge_id = self.query.get("badgeId", "0")

    database = self.server.storage.badges
    badge_data = self.game_config.remote_data.badges.get(int(badge_id))
    username = self.server.storage.players.get_player_field_from_index(self.server.storage.players.player_field.IDEN_NUM, user_id_num, self.server.storage.players.player_field.USERNAME)
    if not badge_data:
        self.send_data('0')
        return True
    if not username:
        self.send_data('0')
        return True
    if database.check(user_id_num, int(badge_id)) is not None:
        self.send_data('0')
        return True

    database.award(user_id_num, int(badge_id))
    self.send_data(f'{username[0]} won {self.game_config.server_core.metadata.creator_name}\'s "{badge_data.name}" award!')

    return True

@server_path(r'/v1/users/(\d+)/badges/awarded-dates', regex=True, commands={'GET'}, versions={versions.rōblox.v463})
def _(self: web_server_handler, match: re.Match[str]) -> bool:
    '''
    TODO: properly award badges.
    https://github.com/MightyPart/openblox/blob/bde5bd486153cfb47990a8e00f63ce4b6bfa8e34/src/apis/classic/badges/badges.types.ts#L61
    '''

    user_id_num = int(match.group(1))
    badge_ids = self.query_lists.get('badgeIds', [])
    database = self.server.storage.badges

    results = []
    for badge_id in badge_ids:
        date_str = database.check(user_id_num, int(badge_id))
        if date_str is None:
            continue
        results.append({
            'badgeId': int(badge_id),
            'awardedDate': date_str,
        })

    self.send_json({f'data': results})
    return True
