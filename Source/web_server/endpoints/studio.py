# Standard library imports
import json
import time

# Local application imports
import util.auth
import util.resource
from web_server._logic import web_server_handler, server_path


@server_path('/studio/e.png')
def _(self: web_server_handler) -> bool:
    self.send_data(b'')
    return True


@server_path('/login/RequestAuth.ashx')
def _(self: web_server_handler) -> bool:
    self.send_data(self.hostname + '/login/negotiate.ashx')
    return True


@server_path('/v2/login')
def _(self: web_server_handler) -> bool:
    return util.auth.HandleLogin(self)


@server_path('/Users/1630228')
@server_path('/game/GetCurrentUser.ashx')
def _(self: web_server_handler) -> bool:
    time.sleep(2)  # HACK: Studio 2021E won't work without it.
    user = util.auth.GetCurrentUser(self)
    self.send_json(0 if user is None else user.id)
    return True


@server_path('/users/account-info')
def _(self: web_server_handler) -> bool:
    user = util.auth.GetCurrentUser(self)
    if user is not None:
        user_id = user.id
        has_password_set = bool(user.password)
    else:
        session_raw = self.headers.get('Roblox-Session-Id')
        if session_raw:
            try:
                session = json.loads(session_raw)
                user_id = session.get("UserId", 1)
            except Exception:
                user_id = 1
        else:
            user_id = 1
        has_password_set = False

    funds = self.server.storage.funds.check(user_id)
    body = json.dumps({
        "UserId": user_id,
        "RobuxBalance": funds or 0,
        "HasPasswordSet": has_password_set,
        "AgeBracket": 0,
        "Roles": [],
        "EmailNotificationEnabled": False,
        "PasswordNotifcationEnabled": False
    })

    self.send_response(200)
    self.send_header("Content-Type", "application/json")
    self.send_header("Content-Length", str(len(body.encode())))
    self.end_headers()
    self.wfile.write(body.encode())
    self.wfile.flush()
    return True


@server_path('/my/settings/json', commands={'GET'})
def _(self: web_server_handler) -> bool:
    self.send_json({})
    return True

@server_path('/universal-app-configuration/v1/behaviors/studio/content')
def _(self: web_server_handler) -> bool:
    config_path = util.resource.retr_full_path(
        util.resource.dir_type.WORKING_DIR,
        'app_config_studio.json',
    )
    with open(config_path, 'r', encoding='utf-8') as f:
        self.send_json(json.load(f))
    return True