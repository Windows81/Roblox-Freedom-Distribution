# Standard library imports
import dataclasses
import functools
import time
import os

# Typing imports
from typing import ClassVar, override

# Local application imports
from routines.rcc import startup_scripts
from config_type.types import wrappers
from .. import _logic as logic
import util.resource
import util.versions
import game_config
import logger


@dataclasses.dataclass(kw_only=True, unsafe_hash=True)
class obj_type(logic.bin_entry, logic.loggable_entry, logic.gameconfig_entry):
    BIN_SUBTYPE = util.resource.bin_subtype.STUDIO
    DIRS_TO_ADD: ClassVar = [
        'logs', 'LocalStorage',
        'InstalledPlugins', 'placeIDEState',
        'ClientSettings',
    ]

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
    def __post_init__(self) -> None:
        super().__post_init__()

        if self.web_host == 'localhost':
            self.web_host = '127.0.0.1'

    @override
    def retr_version(self) -> util.versions.rōblox:
        return self.game_config.retr_version()

    def save_starter_scripts(self) -> None:
        server_path = self.get_versioned_path(os.path.join(
            'Content',
            'Scripts',
            'CoreScripts',
            'RFDStarterScript.lua',
        ))
        with open(server_path, 'w', encoding='utf-8') as f:
            startup_script = startup_scripts.get_script(self.game_config)
            f.write(startup_script)

    @functools.cache
    def setup_place(self) -> str:
        rbx_uri = self.game_config.server_core.place_file.rbxl_uri
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

    @override
    def process(self) -> None:
        self.save_app_settings()
        self.make_aux_directories()
        self.save_starter_scripts()
        time.sleep(self.launch_delay)
        self.make_popen(
            self.get_versioned_path('RobloxStudioBeta.exe'),
            (
                '-localPlaceFile',
                self.setup_place(),
            ))

    @override
    def wait(self):
        super().wait()
        self.kill()
