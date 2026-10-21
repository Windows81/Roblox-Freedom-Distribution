from web_server._logic import web_server_handler, server_path
from config_type.types import structs, wrappers
from util import versions

import util.fvars


def produce_settings(self: web_server_handler) -> structs.settings_type:
    return util.fvars.DEFAULT_SETTINGS[self.rōblox_version] | self.game_config.server_core.roblox_setting_overrides


@server_path('/Setting/QuietGet/RCCService/', versions={versions.rōblox.v347})
@server_path('/Setting/QuietGet/StudioAppSettings/', versions={versions.rōblox.v347})
@server_path('/Setting/QuietGet/ClientAppSettings/', versions={versions.rōblox.v347})
@server_path('/Setting/QuietGet/AndroidAppSettings/', versions={versions.rōblox.v347})
@server_path('/Setting/Get/AndroidAppSettings/', versions={versions.rōblox.v347})
def _(self: web_server_handler) -> bool:
    self.send_json(
        produce_settings(self),
    )
    return True


@server_path('/v1/settings/application', versions={versions.rōblox.v463})
def _(self: web_server_handler) -> bool:
    # Expect this to be `PCDesktopClient` or `RCCService`.
    # application_name = self.query.get('applicationName', None)

    self.send_json(
        {'applicationSettings': produce_settings(self)},
    )
    return True
