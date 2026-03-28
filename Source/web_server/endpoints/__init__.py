from web_server._logic import server_path, web_server_handler
import util.const

from . import (
    authentication,
    assets,
    avatar,
    badges,
    data_transfer,
    funds,
    games_api,
    groups,
    image,
    join_data,
    marketplace,
    mobile,
    persistence,
    player_info,
    save_place,
    setup_player,
    setup_rcc,
    telemetry,
    text_filter,
    studio,
    users_api,
)


@server_path("/")
def _(self: web_server_handler) -> bool:
    if self.try_proxy_frontend(fallback_on_error=True):
        return True

    # Handle OAuth authorization requests (v554 browser login)
    state = self.query.get('state', '')
    code_challenge = self.query.get('code_challenge', '')
    if state or code_challenge:
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        html = f'''<!DOCTYPE html>
<html><head><title>Studio Login</title></head>
<body style="background:#212529;color:#fff;display:flex;justify-content:center;align-items:center;min-height:100vh;margin:0;font-family:Arial">
<div style="text-align:center;background:#30363b;padding:20px;border-radius:10px">
<h1>Roblox Studio Login</h1>
<p>Click below to log in.</p>
<button onclick="window.location.href='roblox-studio-auth:/?code=a&state={state}'"
style="background:#4CAF50;color:white;padding:10px 20px;border:none;border-radius:5px;cursor:pointer;font-size:16px">
Login</button></div></body></html>'''
        self.wfile.write(html.encode())
        return True

    # Default response
    data_string = (
        'Roblox Freedom Distribution webserver %s [%s]' %
        (
            util.const.GIT_RELEASE_VERSION,
            self.game_config.game_setup.roblox_version.value[0],
        )
    )
    self.send_data(data_string.encode('utf-8'))
    return True
