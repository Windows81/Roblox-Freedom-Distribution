import random

from web_server._logic import web_server_handler, server_path

@server_path('/device/initialize', commands={'POST'})
def _(self: web_server_handler) -> bool:
    self.send_json({"browserTrackerId": random.randint(100000000,9999999999), "appDeviceIdentifier": None})
    return True

@server_path('/v1/mobile-client-version')
@server_path('/mobileapi/check-app-version')
def _(self: web_server_handler) -> bool:
    self.send_response(200)
    self.send_json({
        "activeVersion": "SomeRandomVersion",
        "upgradeSource": "https://github.com/Windows81/Roblox-Freedom-Distribution/releases",
        "MD5Sum": "1ec0bbc0d9d9255cb0e62119e9197a12",
        "data": {"UpgradeAction": "None"}
    })
    return True