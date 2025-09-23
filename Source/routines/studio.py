# Standard library imports
import dataclasses
import util.const
import functools
import threading
import time
from textwrap import dedent

# Typing imports
from typing import override

# Local application imports
import game_config
import logger
import util.resource
import util.versions
from config_type.types import wrappers
from . import _logic as logic


class obj_type(logic.bin_web_entry, logic.loggable_entry):
    local_args: 'arg_type'
    BIN_SUBTYPE = util.resource.bin_subtype.STUDIO

    @override
    def retr_version(self) -> util.versions.rōblox:
        return self.local_args.game_config.retr_version()

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

    @staticmethod
    def get_warning_message(version: util.versions.rōblox, filter: logger.filter.filter_type) -> str | None:
        '''
        TODO: remove any need to display a warning message.
        '''
        prefix = (
            '\n' +
            filter.bcolors.BOLD +
            "Studio is not 'stable' and can take some help." +
            filter.bcolors.ENDC +
            '\n'
        )
        match version:
            case util.versions.rōblox.v348:
                return None
            case _:
                return None

    @override
    def process(self) -> None:
        self.save_app_setting()

        # Let's warn the user that Studio requires additional user intervention.
        warn_str = self.get_warning_message(
            self.retr_version(),
            self.local_args.log_filter,
        )

        # If no warning string is included, assume that no warning is needed.
        if warn_str is not None and self.local_args.warn_drag:
            warn_thread = threading.Thread(
                target=input,
                args=(warn_str,),
            )
            warn_thread.start()
            time.sleep(self.local_args.launch_delay)
            warn_thread.join()
        else:
            time.sleep(self.local_args.launch_delay)

        self.make_popen([
            self.get_versioned_path('RobloxStudioBeta.exe'),
            self.setup_place(),
        ])


@dataclasses.dataclass
class arg_type(logic.bin_web_arg_type, logic.loggable_arg_type):
    obj_type = obj_type

    web_host: str
    web_port: int
    game_config: game_config.obj_type
    log_filter: logger.filter.filter_type
    launch_delay: float = 0
    warn_drag: bool = True

    @override
    def get_base_url(self) -> str:
        return f'https://{self.web_host}:{self.web_port}'

    @override
    def get_app_base_url(self) -> str:
        return self.get_base_url()

    @override
    def sanitise(self) -> None:
        super().sanitise()

        if self.web_host == '127.0.0.1':
            self.web_host = 'localhost'
