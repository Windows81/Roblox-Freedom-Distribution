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
