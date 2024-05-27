from web_server._logic import web_server_handler, server_path
import util.ssl
import util.const


@server_path('/api.GetAllowedMD5Hashes/')
def _(self: web_server_handler) -> bool:
    self.send_json(util.const.ALLOWED_MD5_HASHES)
    return True


@server_path('/api.GetAllowedSecurityVersions/')
def _(self: web_server_handler) -> bool:
    self.send_json({
        'data': self.server.game_config.game_setup.roblox_version.security_versions(),
    })
    return True


@server_path('/v1.1/Counters/BatchIncrement')
def _(self: web_server_handler) -> bool:
    self.send_json({})
    return True


@server_path('/v1.1/game-start-info', min_version=400)
def _(self: web_server_handler) -> bool:
    self.send_json({
        "gameAvatarType": "PlayerChoice",
        "allowCustomAnimations": "True",
        "universeAvatarCollisionType": "OuterBox",
        "universeAvatarBodyType": "Standard",
        "jointPositioningType": "ArtistIntent",
        "message": "",
        "universeAvatarMinScales": {
            "height": 0,
            "width": 0,
            "head": 0,
            "depth": 0,
            "proportion": 0,
            "bodyType": 0,
        },
        "universeAvatarMaxScales": {
            "height": 1e9,
            "width": 1e9,
            "head": 1e9,
            "depth": 1e9,
            "proportion": 1e9,
            "bodyType": 1e9,
        },
        "universeAvatarAssetOverrides": [],
        "moderationStatus": None,
    })
    return True
