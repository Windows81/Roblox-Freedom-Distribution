from web_server._logic import web_server_handler, server_path
import util.versions as versions
import urllib.parse
import json


@server_path('/currency/balance', commands={'GET'})
def _(self: web_server_handler) -> bool:
    # TODO: actually make gamepass sales secure.
    user_id_num = json.loads(self.headers['Roblox-Session-Id'])['UserId']
    funds = self.server.storages.funds.check(user_id_num)
    self.send_json({
        "success": True,
        "robux": funds or 0,
        "tickets": 0
    })
    return True


@server_path('/marketplace/purchase', commands={'POST'})
def _(self: web_server_handler) -> bool:
    form_content = str(self.read_content(), encoding='utf-8')
    form_data = dict(urllib.parse.parse_qsl(form_content))
    gamepass_id = int(form_data['productId'])

    # TODO: actually make gamepass sales secure.
    user_id_num = json.loads(self.headers['Roblox-Session-Id'])['UserId']

    # The item being purchased isn't a gamepass.
    gamepass = self.game_data_group.configs.remote_data.gamepasses.get(
        gamepass_id)
    assert gamepass is not None

    storage = self.server.storages
    if storage.gamepasses.check(user_id_num, gamepass_id):
        self.send_json({"status": "error", "error": "You already own this!"})
        return True

    funds = self.server.storages.funds.check(user_id_num)
    if funds is None:
        self.send_json({"status": "error", "error": "Couldn't load funds"})
        return True

    if funds < gamepass.price:
        self.send_json({"status": "error", "error": "Too poor!"})
        return True

    self.server.storages.gamepasses.update(user_id_num, gamepass_id)
    self.server.storages.funds.add(user_id_num, -gamepass.price)

    self.send_json({"success": True, "status": "Bought"})
    return True
