import web_server._logic as web_server_logic
from config_type.types import wrappers
from . import _logic as logic
from textwrap import dedent
import util.resource
import util.versions
import game_config
import dataclasses
import util.const
import functools
import logger
import time


class obj_type(logic.bin_ssl_entry, logic.loggable_entry):
    local_args: 'arg_type'
    BIN_SUBTYPE = util.resource.bin_subtype.STUDIO

    def retr_version(self) -> util.versions.rōblox:
        res = self.local_args.send_request('/rfd/roblox-version')
        return util.versions.rōblox.from_name(str(res.read(), encoding='utf-8'))

    @functools.cache
    def setup_place(self) -> str:
        rbx_uri = self.local_args.game_config.server_core.place_file.rbxl_uri
        # If the file is local, simply have Studio load its path directly.
        if rbx_uri.uri_type == wrappers.uri_type.LOCAL:
            assert isinstance(rbx_uri.value, wrappers.path_str)
            return str(rbx_uri.value)

        # If the file is remote, have RFD fetch the data and save it locally.
        new_path = util.resource.retr_full_path(
            util.resource.dir_type.MISC,
            "_.rbxl",
        )
        rbxl_data = rbx_uri.extract()
        if rbxl_data is None:
            raise Exception('RBXL was not found.')
        with open(new_path, 'wb') as f:
            f.write(rbxl_data)
        return new_path

    def save_app_setting(self) -> str:
        '''
        Modifies settings to point to correct host name.
        '''
        path = self.get_versioned_path('AppSettings.xml')
        app_base_url = self.local_args.get_app_base_url()
        with open(path, 'w', encoding='utf-8') as f:
            f.write(dedent(f'''\
                <?xml version="1.0" encoding="UTF-8"?>
                <Settings>
                    <ContentFolder>Content</ContentFolder>
                    <BaseUrl>{app_base_url}</BaseUrl>
                </Settings>
            '''))
        return path

    def process(self) -> None:
        self.save_app_setting()
        self.save_ssl_cert(
            include_system_certs=True,
        )

        time.sleep(self.local_args.launch_delay)
        self.make_popen([
            self.get_versioned_path('RobloxStudioBeta.exe'),
            self.setup_place(),
        ])


@dataclasses.dataclass
class arg_type(logic.bin_ssl_arg_type, logic.loggable_arg_type):
    obj_type = obj_type

    web_host: str
    web_port: web_server_logic.port_typ
    game_config: game_config.obj_type
    log_filter: logger.filter.filter_type
    launch_delay: float = 0

    def get_base_url(self) -> str:
        return (
            f'http{"s" if self.web_port.is_ssl else ""}://' +
            f'{self.web_host}:{self.web_port.port_num}'
        )

    def get_app_base_url(self) -> str:
        return self.get_base_url()
