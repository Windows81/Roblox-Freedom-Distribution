from typing_extensions import Any
from .custom_types import type_calls, get_type_call
from . import _logic
import dataclasses
import functools


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


class obj_type:
    def serialise_object(self, path: str, key: str, typ: type, rep: Any) -> Any:
        if type(rep) == typ:
            return rep
        type_call = get_type_call(typ)
        return type_call(
            self.root,
            typ,
            path,
            rep,
        )

    def __init__(
        self,
        root: _logic.base_type,
        current_typ: type,
        path_prefix: str = '',
        **kwargs,
    ) -> None:
        self.root = root
        self.kwargs = kwargs

        # Iterates through sub-sections; makes recursive calls to this `__init__`.
        self.subsections = [
            subsection(
                key,
                typ(
                    root=root,
                    current_typ=typ,
                    path_prefix=f'{path_prefix}{key}.',
                    **kwargs.get(key, {}),
                ),
            )
            for key, typ in current_typ.__dict__.items()
            if isinstance(typ, type) and issubclass(typ, obj_type)
        ]

        for sub in self.subsections:
            setattr(self, sub.key, sub.val)

        def get_rep(key: str):
            '''
            Grabs the intermediate representation from the game config file,
            Else the default as defined in `./structure.py`.
            '''
            return self.kwargs.get(key, getattr(current_typ, key, None))

        # Iterates through individual settings in this section.
        self.annotations = [
            annotation(
                key=key,
                typ=typ,
                path=(path := f'{path_prefix}{key}'),
                rep=(rep := get_rep(key)),
                val=self.serialise_object(path, key, typ, rep),
            )
            for key, typ in current_typ.__annotations__.items()
        ]

        for ann in self.annotations:
            setattr(self, ann.key, ann.val)

    @functools.cache
    def flatten(self) -> dict[str, annotation]:
        return {
            ann.key: ann
            for ann in self.annotations
        } | {
            key: res
            for sub in self.subsections
            for key, res in sub.val.flatten().items()
        }
