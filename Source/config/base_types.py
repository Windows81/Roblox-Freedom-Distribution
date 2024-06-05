from typing_extensions import Callable, Union, Any
from . import user_dict
import util.resource
import util.versions
import data_transfer
import dataclasses
import functools
import os.path


class _base_type:
    file_path: str

    def __init__(self) -> None:
        self.data_transferer = data_transfer.transferer()
        self.user_dict = user_dict.user_dict(self)
        super().__init__()


@functools.cache
def get_type_call(typ: type) -> Callable:
    for k in [
        typ,
        getattr(typ, '__origin__', None),
    ]:
        if k not in _TYPE_CALLS:
            continue
        return _TYPE_CALLS[k]
    return _exec_type_call_default


def _exec_type_call_default(config: _base_type, typ: type, path: str, *args, **kwargs) -> Any:
    return typ(*args, **kwargs)


def _exec_type_call_callable(config: _base_type, typ: type, path: str, val) -> Callable:
    return lambda *args: config.data_transferer and config.data_transferer.call(path, config, *args)


def _exec_type_call_union(config: _base_type, typ: type, path: str, val) -> Any | None:
    for t in typ.__args__:
        try:
            type_call = get_type_call(t)
            return type_call(
                config,
                typ,
                path,
                val,
            )
        except Exception:
            pass

    raise ValueError(
        'Value "%s" is not of any of the following types: %s' %
        (val, *', '.join(typ.__args__)),
    )


class file_path(str):
    @staticmethod
    def evaluate(config: _base_type, val: str) -> 'file_path':
        root = os.path.dirname(config.file_path)
        return file_path(os.path.join(root, val))


_TYPE_CALLS = {
    util.versions.rōblox: lambda config, typ, path, val: util.versions.rōblox.from_name(val),

    # Through `getattr`, hacky method to get callables.
    getattr(Callable, '__origin__'): _exec_type_call_callable,

    Union: _exec_type_call_union,

    file_path: lambda config, typ, path, val: file_path.evaluate(config, val),
}


@dataclasses.dataclass
class subsection:
    key: str
    val: Any


@dataclasses.dataclass
class annotation:
    key: str
    typ: type
    path: str
    rep: Any
    val: Any


class allocateable:
    def serialise_object(self, path: str, key: str, typ: type, rep: Any) -> Any:
        type_call = get_type_call(typ)
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
