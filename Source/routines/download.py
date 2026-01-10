# Standard library imports
import dataclasses

# Typing imports
from typing import override

# Local application imports
import downloader
import logger
import util.versions
from . import _logic as logic


@dataclasses.dataclass(kw_only=True, unsafe_hash=True)
class obj_type(logic.bin_entry, logic.loggable_entry):
    @override
    def process(self) -> None:
        downloader.bootstrap_binary(
            rōblox_version=self.rōblox_version,
            bin_type=self.BIN_SUBTYPE,
            log_filter=self.log_filter,
        )
