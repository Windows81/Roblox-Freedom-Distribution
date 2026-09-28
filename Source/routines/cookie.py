# Standard library imports
import dataclasses

# Typing imports
from typing import override

# Local application imports
from . import _logic as logic
from assets import default_grabber


@dataclasses.dataclass(kw_only=True, unsafe_hash=True)
class obj_type(logic.base_entry):
    verbose: bool

    @override
    def process(self) -> None:
        super().process()
        cookie = default_grabber.get_rōblox_cookie()
        if cookie is None:
            print('No cookie is provided.')
            return

        if self.verbose:
            print(cookie)
        else:
            print('A cookie is provided.')
