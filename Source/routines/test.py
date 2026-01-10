from typing import override
import dataclasses

from . import _logic as logic
import tester


@dataclasses.dataclass(kw_only=True, unsafe_hash=True)
class obj_type(logic.obj_type):
    tests: set[str]

    @override
    def process(self) -> None:
        tester.run_test(self.tests)
