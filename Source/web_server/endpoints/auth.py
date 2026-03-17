import json
from web_server._logic import web_server_handler, server_path
import util.versions as versions

@server_path('/v1/users/authenticated')
def _(self: web_server_handler) -> bool:
    is_authenticated = True
    if not is_authenticated:
        self.send_response(401)
        self.send_header("Content-Type", "application/json")
        self.send_json({"error":"User not authenticated"})
        return True
    self.send_response(200)
    self.send_header("Content-Type", "application/json")
    self.send_json({
        "id": 1,
        "name": "ROBLOX",
        "displayName": "ROBLOX"
    })
    return True

@server_path(r'/signup/is-username-valid', versions={versions.rōblox.v463}, commands={'GET'})
def _(self: web_server_handler) -> bool:
    '''
    Ensure there's no players with requested username
    '''
    self.send_response(200)
    self.send_json({"code": 1, "message": "Username is valid"})
    return True


@server_path(r'/signup/is-password-valid', versions={versions.rōblox.v463}, commands={'GET'})
def _(self: web_server_handler) -> bool:
    '''
    Ensure the password is correct
    '''
    self.send_response(200)
    self.send_json({"code": 1, "message": "Password is valid"})
    return True


@server_path('/v1/login')
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
