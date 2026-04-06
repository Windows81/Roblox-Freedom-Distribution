# Standard library imports
import json
import re

# Local application imports
import util.auth
from web_server._logic import web_server_handler, server_path


@server_path('/currency/balance', commands={'GET'})
def _(self: web_server_handler) -> bool:
    # TODO: actually make gamepass sales secure.
    user_id_num = json.loads(self.headers['Roblox-Session-Id'])['UserId']
    funds = self.server.storage.funds.check(user_id_num)
    self.send_json({
        "success": True,
        "robux": funds or 0,
        "tickets": 0
    })
    return True


def send_user_currency_v1(
    self: web_server_handler,
    user_id: int,
) -> bool:
    authenticated_user = util.auth.GetCurrentUser(self)
    if authenticated_user is None or authenticated_user.id != user_id:
        self.send_json({
            "success": False,
            "message": "Unauthorized",
        }, 401)
        return True

    funds = self.server.storage.funds.check(authenticated_user.id)
    self.send_json({
        "robux": funds or 0,
        "tickets": 0,
    })
    return True


@server_path(r'/v1/users/(\d+)/currency', regex=True, commands={'GET'})
@util.auth.authenticated_required_api
def _(self: web_server_handler, match: re.Match[str]) -> bool:
    return send_user_currency_v1(self, int(match.group(1)))
