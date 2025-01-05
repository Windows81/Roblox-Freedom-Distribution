import json
from warnings import catch_warnings
from web_server._logic import web_server_handler, server_path
import util.versions as versions
import util.const
import util.ssl
import time


@server_path('/studio/e.png')
def _(self: web_server_handler) -> bool:
    self.send_data(b'')
    return True

#


@server_path('/login/RequestAuth.ashx')
def _(self: web_server_handler) -> bool:
    self.send_data(self.hostname+'/login/negotiate.ashx')
    return True


@server_path('/v2/login')
def _(self: web_server_handler) -> bool:
    try:
        assert (
            '1' not in json.loads(self.read_content())['password']
        )  # Password must not contain '1'.  This for debugging purposes only.
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
    self.send_json({
        'UserId': 1630228,
        'Username': 'nsg-cache-archive-x86',
        'DisplayName': 'nsg-cache-archive-x86',
        'HasPasswordSet': True,
        'Email': {'Value': 'n**@roblox.com', 'IsVerified': True},
        'AgeBracket': 0,
        'Roles': ['BetaTester', 'Beta17', 'Roblox.Slack.Models.Contractor.Name', 'Soothsayer'],
        'MembershipType': 0,
        'RobuxBalance': 98763,
        'NotificationCount': 223,
        'EmailNotificationEnabled': False,
        'PasswordNotificationEnabled': False,
        'CountryCode': 'RU',
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
