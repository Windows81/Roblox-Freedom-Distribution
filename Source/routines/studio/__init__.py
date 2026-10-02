import dataclasses
import functools
import textwrap
import time
import os

from typing import ClassVar, override

import assets
from routines.rcc import startup_scripts
from config_type.types import wrappers
from .. import _logic as logic
import util.resource
import util.versions


@dataclasses.dataclass(kw_only=True, unsafe_hash=True)
class obj_type(logic.bin_entry, logic.loggable_entry, logic.gameconfig_entry):
    BIN_SUBTYPE = util.resource.bin_subtype.STUDIO
    DIRS_TO_ADD: ClassVar = [
        'logs', 'LocalStorage',
        'InstalledPlugins', 'placeIDEState',
        'ClientSettings',
    ]

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
        if rbx_uri.uri_type != wrappers.uri_type.LOCAL:
            raise Exception('RFD only supports local-based `rbxl` paths.')

        rbxl_data = rbx_uri.extract()
        if rbxl_data is None:
            raise FileNotFoundError('Your selected file does not exist.')

        if assets.serialisers.rbxl.should_parse(rbxl_data):
            raise Exception(textwrap.dedent(f'''
                Your `rbxl` file needs to be serialised by RFD; try running this one-liner, then try opening Studio again:
                mv "%(f)s" "%(f)s.BAK" && %(a)s serialise -r "%(f)s.BAK" -w "%(f)s" -m rbxl
            ''' % {'f': rbx_uri.value, 'a': util.resource.get_cli_prefix()}))

        assert isinstance(rbx_uri.value, wrappers.path_str)
        return str(rbx_uri.value)

    @override
    def bootstrap(self) -> None:
        super().bootstrap()
        self.save_app_settings()
        self.make_aux_directories()
        self.save_starter_scripts()
        time.sleep(self.launch_delay)
        self.init_popen(
            self.get_versioned_path('RobloxStudioBeta.exe'),
            (
                '-localPlaceFile',
                self.setup_place(),
            ))

    @override
    def wait(self):
        super().wait()
        self.kill()
