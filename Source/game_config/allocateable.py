from config_type.types import get_type_call, type_call_data
from typing_extensions import Any
from config_type import _logic
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
            rep,
            type_call_data(
                config=self.root,
                sibling_kwargs=self.kwargs,
                typ=typ,
                key=key,
                path=path,
            )
        )

    def __init__(
        self,
        root: _logic.base_type,
        current_typ: type,
        path_prefix: str = '',
        **kwargs,
    ) -> None:
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

        self.root = root
        self.kwargs = kwargs

        for sub in self.subsections:
            setattr(self, sub.key, sub.val)

        def get_rep(key: str):
            '''
            Grabs the intermediate representation from the game config file,
            Else the default as defined in `./structure.py`.
            '''
            if key in self.kwargs:
                return self.kwargs[key]
            if hasattr(current_typ, key):
                return getattr(current_typ, key)
            raise Exception(
                'Unable to find setting "%s" in config file.' %
                (key),
            )

        # Creates `annotation` objects through individual settings in this section.
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
