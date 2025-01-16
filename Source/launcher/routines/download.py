from typing import override
import util.resource
import util.versions
import dataclasses
import util.const
import logger

from . import _logic as logic
import downloader


@dataclasses.dataclass
class _arg_type(logic.loggable_arg_type):
    rōblox_version: util.versions.rōblox
    bin_subtype: str
    log_filter: logger.filter.filter_type


class obj_type(logic.bin_entry, logic.loggable_entry):
    local_args: _arg_type

    def __init__(
            self,
            rōblox_version: util.versions.rōblox,
            bin_subtype: str) -> None:
        super().__init__()
        self.rōblox_version = rōblox_version
        self.bin_subtype = bin_subtype

    @override
    def process(self) -> None:
        downloader.bootstrap_binary(
            rōblox_version=self.rōblox_version,
            bin_type=self.BIN_SUBTYPE,
            log_filter=self.local_args.log_filter,
        )


class arg_type(_arg_type):
    obj_type = obj_type
