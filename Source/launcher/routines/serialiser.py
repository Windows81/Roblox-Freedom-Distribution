from . import _logic as logic
from typing import override
import assets.serialisers
import dataclasses


class obj_type(logic.entry):
    local_args: 'arg_type'

    @override
    def process(self) -> None:
        for (r, w) in self.local_args.files:
            with open(r, 'rb') as fr:
                data = assets.serialisers.parse(
                    fr.read(),
                    self.local_args.methods,
                )
            with open(w, 'wb') as fw:
                fw.write(data)


@dataclasses.dataclass
class arg_type(logic.arg_type):
    obj_type = obj_type
    methods: set[assets.serialisers.method]
    files: list[tuple[str, str]]
