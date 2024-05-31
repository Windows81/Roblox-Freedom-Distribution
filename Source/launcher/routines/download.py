import util.resource
import util.versions
import dataclasses
import util.const

from . import _logic as logic
import launcher.downloader._main as downloader


@dataclasses.dataclass
class _arg_type(logic.arg_type):
    rōblox_version: util.versions.rōblox
    bin_subtype: str


class obj_type(logic.bin_entry):
    local_args: _arg_type

    def __init__(self, rōblox_version: util.versions.rōblox, bin_subtype: str):
        super().__init__()
        self.rōblox_version = rōblox_version
        self.bin_subtype = bin_subtype

    def process(self) -> None:
        downloader.download_binary(
            self.rōblox_version,
            self.BIN_SUBTYPE,
        )


class arg_type(_arg_type):
    obj_type = obj_type
