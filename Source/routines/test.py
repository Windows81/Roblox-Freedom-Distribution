from typing import override
import dataclasses

from . import _logic as logic
import tester


@dataclasses.dataclass(kw_only=True, unsafe_hash=True)
class obj_type(logic.base_entry):
    tests: set[str]

    @override
    def process(self) -> None:
        super().process()
        tester.run_test(self.tests)
