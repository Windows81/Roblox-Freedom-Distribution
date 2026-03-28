import re

from web_server._logic import web_server_handler, server_path


def send_user_details_v1(
    self: web_server_handler,
    user_id: int,
) -> bool:
    user = self.server.storage.user.check_object(user_id)
    if user is None:
        self.send_json({
            "errors": [
                {
                    "code": 3,
                    "message": "The user id is invalid.",
                }
            ]
        }, 404)
        return True

    self.send_json({
        "description": user.description,
        "created": user.created,
        "isBanned": user.accountstatus != 1,
        "externalAppDisplayName": user.username,
        "hasVerifiedBadge": False,
        "id": user.id,
        "name": user.username,
        "displayName": user.username,
    })
    return True


@server_path(r'/v1/users/(\d+)', regex=True, commands={'GET'})
def _(self: web_server_handler, match: re.Match[str]) -> bool:
    return send_user_details_v1(self, int(match.group(1)))
