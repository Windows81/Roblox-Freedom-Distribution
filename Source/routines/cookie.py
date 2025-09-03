# Standard library imports
import dataclasses

# Typing imports
from typing import override

# Local application imports
from . import _logic as logic
from assets import extractor


@dataclasses.dataclass
class _arg_type(logic.arg_type):
    verbose: bool


class obj_type(logic.entry):
    local_args: _arg_type

    @override
    def process(self) -> None:
        cookie = extractor.get_rōblox_cookie()
        if cookie is None:
            print('No cookie is provided.')
            return

        if self.local_args.verbose:
            print(cookie)
        else:
            print('A cookie is provided.')


class arg_type(_arg_type):
    obj_type = obj_type
