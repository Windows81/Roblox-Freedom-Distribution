
from .._logic import base_type as config_base_type
from typing_extensions import Any
import dataclasses


@dataclasses.dataclass
class type_call_data:
    config: config_base_type
    sibling_kwargs: dict[str, Any]
    typ: type
    key: str
    path: str
