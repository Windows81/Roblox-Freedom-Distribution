# Standard library imports
import dataclasses

# Typing imports
from typing import override

# Local application imports
import assets.serialisers
from . import _logic as logic


@dataclasses.dataclass
class obj_type(logic.base_entry):
    methods: set[assets.serialisers.method]
    files: list[tuple[str, str]]

    @override
    def process(self) -> None:
        super().process()
        for (r, w) in self.files:
            with open(r, 'rb') as fr:
                data, changed = assets.serialisers.parse(
                    fr.read(),
                    self.methods,
                )
            if changed:
                print(w)
            with open(w, 'wb') as fw:
                fw.write(data)
