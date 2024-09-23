
from typing_extensions import Any
import dataclasses


@dataclasses.dataclass
class type_call_data:
    config: Any
    sibling_kwargs: dict[str, Any]
    typ: type
    key: str
    path: str
