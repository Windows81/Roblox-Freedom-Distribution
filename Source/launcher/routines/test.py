import util.resource
import util.versions
import dataclasses
import util.const

from . import _logic as logic
import tester


@dataclasses.dataclass
class _arg_type(logic.arg_type):
    tests: set[str]


class obj_type(logic.entry):
    local_args: _arg_type

    def process(self) -> None:
        tester.run_test(self.local_args.tests)


class arg_type(_arg_type):
    obj_type = obj_type
