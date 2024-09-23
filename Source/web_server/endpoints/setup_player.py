from web_server._logic import web_server_handler, server_path, web_server_ssl
import assets.returns as returns
import util.resource
import util.const
import util.ssl
import time
import re


@server_path('/rfd/default-user-code')
def _(self: web_server_handler) -> bool:
    config = self.game_data.config
    result = config.server_core.retrieve_default_user_code(
        time.time(),
    )
    self.send_data(bytes(result, encoding='utf-8'))
    return True


@server_path('/rfd/certificate')
def _(self: web_server_handler) -> bool:
    assert isinstance(self.server, web_server_ssl)
    self.server.add_identities(self.ip_addr)
    self.send_data(self.server.ssl_mutable.get_client_cert())
    return True


@server_path('/rfd/is-player-allowed')
def _(self: web_server_handler) -> bool:
    database = self.server.storage.players

    id_num = int(self.query['userId'])
    user_code = database.get_player_field_from_index(
        database.player_field.ID_NUMBER,
        id_num,
        database.player_field.USER_CODE,
    )

    if user_code is None:
        self.send_data(b'false')
        return True

    # This function was also called during joinscript creation.
    # It's called a second time here (potentially) for additional protection.
    if self.game_data.config.server_core.check_user_allowed(id_num, user_code):
        self.send_data(b'true')
        return True

    self.send_data(b'false')
    return True


@server_path('/rfd/roblox-version')
def _(self: web_server_handler) -> bool:
    '''
    Used by clients to automatically detect which version to run.
    '''
    version = self.game_data.config.game_setup.roblox_version
    self.send_data(bytes(version.name, encoding='utf-8'))
    return True


@server_path('/login/negotiate.ashx')
@server_path('/universes/validate-place-join')
def _(self: web_server_handler) -> bool:
    self.send_json(True)
    return True


@server_path('/game/validate-machine')
def _(self: web_server_handler) -> bool:
    self.send_json({"success": True})
    return True


@server_path('/Setting/QuietGet/ClientAppSettings/')
def _(self: web_server_handler) -> bool:
    self.send_json({})
    return True


@server_path('/avatar-thumbnail/json')
def _(self: web_server_handler) -> bool:
    '''
    To simplify the server program, let not there be avatar thumbnail storage.
    '''
    self.send_json({})
    return True


@server_path('/avatar-thumbnail/image')
def _(self: web_server_handler) -> bool:
    '''
    To simplify the server program, let there not be avatar thumbnail images.
    '''
    return True


@server_path('/asset-thumbnail/json')
def _(self: web_server_handler) -> bool:
    '''
    TODO: properly deflect thumbnail generation.
    '''
    self.send_json({
        'Url': f'{self.hostname}/Thumbs/GameIcon.ashx',
        'Final': True,
        'SubstitutionType': 0,
    })
    return True


@server_path('/Thumbs/GameIcon.ashx')
def _(self: web_server_handler) -> bool:
    asset_cache = self.game_data.asset_cache
    thumbnail_data = asset_cache.get_asset(util.const.THUMBNAIL_ID_CONST)
    if isinstance(thumbnail_data, returns.ret_data):
        self.send_data(thumbnail_data.data)
    return True


@server_path('/v1/settings/application')
def _(self: web_server_handler) -> bool:
    self.send_json({'applicationSettings': {}})
    return True


@server_path('/v1/player-policies-client')
def _(self: web_server_handler) -> bool:
    self.send_json({
        'isSubjectToChinaPolicies': False,
        'arePaidRandomItemsRestricted': False,
        'isPaidItemTradingAllowed': True,
        'areAdsAllowed': True,
    })
    return True


@server_path('/users/([0-9]+)/canmanage/([0-9]+)', regex=True)
def _(self: web_server_handler, match: re.Match[str]) -> bool:
    self.send_json({"Success": True, "CanManage": True})
    return True


@server_path('/v1/user/([0-9]+)/is-admin-developer-console-enabled', regex=True)
def _(self: web_server_handler, match: re.Match[str]) -> bool:
    database = self.server.storage.players

    id_num = int(match.group(1))
    user_code = database.get_player_field_from_index(
        database.player_field.ID_NUMBER,
        id_num,
        database.player_field.USER_CODE,
    )

    if user_code is None:
        result = False
    else:
        result = self.game_data.config.server_core.check_user_has_admin(
            id_num, user_code,
        )

    self.send_json({"isAdminDeveloperConsoleEnabled": result})
    return True
