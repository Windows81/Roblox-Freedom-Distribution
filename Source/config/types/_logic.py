
from typing_extensions import Any
import dataclasses


@dataclasses.dataclass
class type_call_data:
    config: Any
    sibling_kwargs: dict[str, Any]
    typ: type
    key: str
    path: str


@dataclasses.dataclass
class subsection:
    key: str
    val: Any


@dataclasses.dataclass
class annotation:
    key: str
    typ: type
    path: str
    rep: Any  # As in 'Pythonic representation'.  Needs to be clarified.
    val: Any
