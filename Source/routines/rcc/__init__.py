# Standard library imports
from typing import IO, override
import dataclasses
import subprocess
import functools
import threading
import time
import json
import os

# Local application/library specific imports
from config_type.types import structs, wrappers, callable
from .. import _logic as logic
import util.const as const
import assets.serialisers
import util.resource
import util.versions
import game_config
import logger

from . import (
    startup_scripts,
    log_action,
)


class obj_type(logic.bin_entry, logic.gameconfig_entry):
    local_args: 'arg_type'
    BIN_SUBTYPE = util.resource.bin_subtype.SERVER

    @functools.cache
    def retr_version(self) -> util.versions.rōblox:
        return self.game_config.game_setup.roblox_version

    def save_thumbnail(self) -> None:
        '''
        Saves the thumbnail data for the current game config.
        '''
        config = self.game_config
        cache = config.asset_cache
        icon_uri = config.server_core.metadata.icon_uri
        if icon_uri is None:
            return

        try:
            thumbnail_data = icon_uri.extract() or bytes()
            cache.add_asset(const.THUMBNAIL_ID_CONST, thumbnail_data)
        except Exception as _:
            logger.log(
                text='Warning: thumbnail data not found.',
                context=logger.log_context.PYTHON_SETUP,
                filter=self.local_args.log_filter,
            )

    def save_place_file(self) -> None:
        '''
        Parses and copies the place file (specified in the config file) to the asset cache.
        '''
        config = self.game_config
        place_uri = config.server_core.place_file.rbxl_uri

        cache = config.asset_cache
        raw_data = place_uri.extract()
        if raw_data is None:
            raise Exception(f'Failed to extract data from {place_uri}.')

        # Parses the raw data using the `rbxl` method.
        rbxl_data, _changed = assets.serialisers.parse(
            raw_data, {assets.serialisers.method.rbxl}
        )

        # Saves `rbxl_data` to a local file in `AssetCache`.
        cache.add_asset(
            self.local_args.place_iden,
            rbxl_data,
        )

        if (
            place_uri.uri_type != wrappers.uri_type.LOCAL and
            config.server_core.place_file.enable_saveplace
        ):
            logger.log(
                (
                    'Warning: config option "enable_saveplace" is redundant '
                    'when the place file is an online resource.'
                ),
                context=logger.log_context.PYTHON_SETUP,
                filter=self.local_args.log_filter,
            )

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

    def update_fflags(self) -> None:
        '''
        Updates the FFlags in the game configuration based on the Rōblox version.
        Individual FFlags, rather than the entire file, override the ones that already exist.
        '''
        # TODO: move FFlag loading to an API endpoint.
        version = self.retr_version()
        new_flags = {
            **self.local_args.log_filter.rcc_logs.get_level_table(),
        }

        match version:
            case util.versions.rōblox.v348:
                path = self.get_versioned_path(
                    'ClientSettings',
                    'RCCService.json',
                )
                with open(path, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)

                json_data |= new_flags
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(json_data, f, indent='\t')

            case util.versions.rōblox.v463:
                path = self.get_versioned_path(
                    'DevSettingsFile.json',
                )
                with open(path, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)

                # 2021E stores the RCC flags in a JSON sub-dictionary named `applicationSettings`.
                json_data['applicationSettings'] |= new_flags
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(json_data, f, indent='\t')

    def save_gameserver(self) -> str:
        '''
        Saves `GameServer.json`, which will be used when the RCC process is created.
        '''
        base_url = self.local_args.get_base_url()
        path = self.get_versioned_path('GameServer.json')

        with open(path, 'w', encoding='utf-8') as f:
            json.dump({
                "Mode": "GameServer",
                "GameId": 13058,
                "Settings": {
                    "Type":
                        "Avatar",
                    "PlaceId":
                        self.local_args.place_iden,
                    "GameId":
                        "Test",
                    "MachineAddress":
                        base_url,
                    "PlaceFetchUrl":
                        f"{base_url}/asset/?id={self.local_args.place_iden}",
                    "MaxPlayers":
                        int(1e9),
                    "PreferredPlayerCapacity":
                        int(1e9),
                    "CharacterAppearance":
                        f"{base_url}/v1.1/avatar-fetch",
                    "MaxGameInstances":
                        1,
                    "GsmInterval":
                        5,
                    "ApiKey":
                        "",
                    "DataCenterId":
                        "69420",
                    "PlaceVisitAccessKey":
                        "",
                    "UniverseId":
                        13058,
                    "MatchmakingContextId":
                        1,
                    "CreatorId":
                        0,
                    "CreatorType":
                        "Group",
                    "PlaceVersion":
                        1,
                    "BaseUrl":
                        f"{base_url}/.127.0.0.1",
                    "JobId":
                        "Test",
                    "PreferredPort":
                        self.local_args.rcc_port,
                },
                "Arguments": {},
            }, f)
        return path

    def gen_cmd_args(self) -> tuple[str, ...]:
        suffix_args: list[str] = []

        # There is a chance that RFD can be overwhelmed with processing output.
        # Removing the `-verbose` flag here will reduce the amount of data piped from RCC.
        if not self.local_args.log_filter.rcc_logs.is_empty():
            suffix_args.append('-verbose')

        match self.retr_version():
            case util.versions.rōblox.v348:
                return (
                    self.get_versioned_path('RCCService.exe'),
                    f'-PlaceId:{self.local_args.place_iden}',
                    '-LocalTest', self.get_versioned_path(
                        'GameServer.json',
                    ),
                    *suffix_args,
                )
            case util.versions.rōblox.v463:
                return (
                    self.get_versioned_path('RCCService.exe'),
                    f'-PlaceId:{self.local_args.place_iden}',
                    '-LocalTest', self.get_versioned_path(
                        'GameServer.json',
                    ),
                    '-SettingsFile', self.get_versioned_path(
                        'DevSettingsFile.json',
                    ),
                    *suffix_args,
                )

    def read_rcc_output(self) -> None:
        '''
        Pipes output from the RCC server to the logger module for processing.
        This is done in a separate thread to avoid blocking the main process from terminating RCC when necessary.
        '''
        stdout: IO[bytes] = self.popen_mains[0].stdout  # type: ignore[reportAssignmentType]
        assert stdout is not None
        while True:
            line = stdout.readline()
            if not line:
                break
            logger.log(
                line.rstrip(b'\r\n'),
                context=logger.log_context.RCC_SERVER,
                filter=self.local_args.log_filter,
            )

            action = log_action.check(line)

            # The `restart` and `kill` methods must take place in a new thread.
            # It waits for *this* thread to finish running.
            if action == log_action.LogAction.RESTART:
                threading.Thread(target=self.restart).start()
                break
            elif action == log_action.LogAction.TERMINATE:
                threading.Thread(target=self.kill).start()
                break

        stdout.flush()

    def make_popen_threads(self) -> None:
        self.make_popen(
            cmd_args=self.gen_cmd_args(),
            cwd=self.get_versioned_path(),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )

        pipe_thread = threading.Thread(
            target=self.read_rcc_output,
            daemon=True,
        )
        pipe_thread.start()

        file_change_thread = threading.Thread(
            target=self.track_file_changes,
            daemon=True,
        )
        file_change_thread.start()

        self.threads.extend([
            pipe_thread,
            file_change_thread,
        ])

    def track_file_changes(self) -> None:
        config = self.game_config
        if not config.server_core.place_file.track_file_changes:
            return

        place_uri = config.server_core.place_file.rbxl_uri
        if place_uri.uri_type != wrappers.uri_type.LOCAL:
            return

        file_path = place_uri.value
        last_modified = os.path.getmtime(file_path)

        while self.is_running and not self.is_terminated:
            current_modified = os.path.getmtime(file_path)
            if current_modified == last_modified:
                time.sleep(1)
                continue
            # The `restart` method must take place in a new thread.
            # It waits for *this* thread to finish running.
            threading.Thread(target=self.restart).start()
            return

    @override
    def process(self) -> None:
        self.get_versioned_path()
        log_filter = self.local_args.log_filter
        logger.log(
            (
                f"{log_filter.bcolors.BOLD}[UDP %d]{log_filter.bcolors.ENDC}: " +
                "initialising Rōblox Cloud Compute"
            ) % (
                self.local_args.rcc_port,
            ),
            context=logger.log_context.PYTHON_SETUP,
            filter=log_filter,
        )
        self.save_starter_scripts()
        self.save_place_file()
        self.save_thumbnail()
        self.save_app_settings()
        self.update_fflags()
        self.save_gameserver()
        self.make_popen_threads()


@dataclasses.dataclass
class arg_type(logic.bin_arg_type):
    obj_type = obj_type

    web_host: str | None
    rcc_port: int | None
    web_port: int | None
    game_config: game_config.obj_type
    log_filter: logger.filter.filter_type

    track_file_changes: bool = True

    # TODO: fix the way place idens work.
    place_iden: int = const.PLACE_IDEN_CONST

    @override
    def get_base_url(self) -> str:
        return f'https://{self.web_host}:{self.web_port}'

    @override
    def get_app_base_url(self) -> str:
        return f'{self.get_base_url()}/'
