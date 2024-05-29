from typing_extensions import Self, Callable, Union, Any
import data_transfer._main
from . import user_dict
import util.resource
import util.versions
import functools
import attr


class _base_type:
    def __init__(self) -> None:
        self.data_transferer = data_transfer._main.transferer()
        self.user_dict = user_dict.user_dict(self)
        super().__init__()


def _exec_type_call_default(config: _base_type, typ: type, path: str, *a, **kwa) -> Any:
    return typ(*a, **kwa)


def _exec_type_call_callable(config: _base_type, typ: type, path: str, _) -> Callable:
    return lambda *a: config.data_transferer and config.data_transferer.call(path, config, *a)


def _exec_type_call_union(config: _base_type, typ: type, path: str, val) -> Any | None:
    for t in typ.__args__:
        try:
            return t(val)
        except Exception:
            pass

    raise ValueError(
        'Value "%s" is not of any of the following types: %s' %
        (val, *', '.join(typ.__args__)),
    )


_TYPE_CALLS = {
    util.versions.rōblox: lambda _, __, ___, v: util.versions.rōblox.from_name(v),

    # Through `getattr`, hacky method to get callables.
    getattr(Callable, '__origin__'): _exec_type_call_callable,

    Union: _exec_type_call_union,
}


@attr.dataclass
class subsection:
    key: str
    val: Any


@attr.dataclass
class annotation:
    key: str
    typ: type
    path: str
    rep: Any
    val: Any


class allocateable:
    class path(str):
        def __new__(cls, val: str) -> Self:
            return str.__new__(cls, util.resource.retr_full_path(util.resource.dir_type.CONFIG, val))

    @classmethod
    @functools.cache
    def get_type_call(cls, typ: type) -> Callable:
        for k in [
            typ,
            getattr(typ, '__origin__', None),
        ]:
            if k not in _TYPE_CALLS:
                continue
            return _TYPE_CALLS[k]
        return _exec_type_call_default

    def serialise_object(self, path: str, key: str, typ: type, rep: Any) -> Any:
        type_call = allocateable.get_type_call(typ)
        return type_call(
            self.root,
            typ,
            path,
            rep,
        )

    def __init__(
        self,
        root: _base_type,
        current_typ: type,
        path_prefix: str = '',
        **kwargs,
    ) -> None:
        super().__init__()  # For sub-classes which have multiple parents.

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
            if isinstance(typ, type) and issubclass(typ, allocateable)
        ]

        for sub in self.subsections:
            setattr(self, sub.key, sub.val)

        # Iterates through individual settings in this section.
        self.annotations = [
            annotation(
                key=key,
                typ=typ,
                path=(path := f'{path_prefix}{key}'),
                rep=(rep := self.kwargs.get(key, None)),
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
