# Standard library imports
import json
import time

# Local application imports
import util.versions as versions
from web_server._logic import web_server_handler, server_path


@server_path('/studio/e.png')
def _(self: web_server_handler) -> bool:
    self.send_data(b'')
    return True

#


@server_path('/login/RequestAuth.ashx')
def _(self: web_server_handler) -> bool:
    self.send_data(self.hostname + '/login/negotiate.ashx')
    return True


@server_path('/v2/login')
def _(self: web_server_handler) -> bool:
    try:
        # Password must not contain '1'.  This for debugging purposes only.
        assert (
            '1' not in json.loads(self.read_content())['password']
        )
        self.send_response(200)
        self.send_header('set-cookie', '.ROBLOSECURITY=_ROBLOSECURITY_')
        self.send_json({
            'user': {
                'id': 1630228,
                'name': 'qwer',
                'displayName': 'qwer',
            },
            'isBanned': False,
        }, status=None)
    except Exception:
        self.send_response(401)
    return True


@server_path('/Users/1630228')
@server_path('/game/GetCurrentUser.ashx')
def _(self: web_server_handler) -> bool:
    time.sleep(2)  # HACK: Studio 2021E won't work without it.
    self.send_json(1630228)
    return True


@server_path('/users/account-info')
def _(self: web_server_handler) -> bool:
    user_id_num = json.loads(self.headers['Roblox-Session-Id'])['UserId']

    funds = self.server.storage.funds.check(user_id_num)
    self.send_json({
        "UserId": user_id_num,
        "RobuxBalance": funds or 0,
    })
    return True


@server_path('/device/initialize')
def _(self: web_server_handler) -> bool:
    self.send_json({"browserTrackerId": 0, "appDeviceIdentifier": None})
    return True


@server_path('/v1/users/authenticated')
def _(self: web_server_handler) -> bool:
    self.send_json({
        "id": 1,
        "name": "ROBLOX",
        "displayName": "ROBLOX"
    })
    return True
