# Standard library imports
import json

# Local application imports
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
