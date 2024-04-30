import util.resource
import util.versions
import dataclasses
import util.const

import launcher.routines._logic as logic
import launcher.downloader._main as downloader


@dataclasses.dataclass
class _arg_type(logic.arg_type):
    rōblox_version: util.versions.rōblox
    dir_name: str


class obj_type(logic.bin_entry):
    local_args: _arg_type

    def __init__(self, rōblox_version: util.versions.rōblox, dir_name: str):
        super().__init__()
        self.rōblox_version = rōblox_version
        self.dir_name = dir_name

    def process(self) -> None:
        downloader.download_binary(
            self.rōblox_version,
            self.dir_name,
        )


class arg_type(_arg_type):
    obj_type = obj_type
