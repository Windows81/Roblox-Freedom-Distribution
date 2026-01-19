from .._logic import web_server_handler, server_path
import util.versions as versions
import re


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
