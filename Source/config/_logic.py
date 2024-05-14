# This module is very convoluted and has one purpose: to serialise your `GameConfig.toml`.
# The data structure is defined in `./_main.py`.
# All you need to know is that the `_configtype` class will make your config file easier for your IDE's auto-complete to handle.

from typing_extensions import Self, Callable, Union, Any
import data_transfer._main
import util.resource
import util.versions
import functools
import tomli
import attr


def _exec_type_call_default(config: '_configtype', typ: type, path: str, *a, **kwa) -> Any:
    return typ(*a, **kwa)


def _exec_type_call_callable(config: '_configtype', typ: type, path: str, _) -> Callable:
    return lambda *a: config.data_transferer and config.data_transferer.call(path, config, *a)


def _exec_type_call_union(config: '_configtype', typ: type, path: str, val) -> Any | None:
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

    def __init__(self, root: '_configtype', path_prefix: str = '', **kwargs) -> None:
        self.root = root
        self.kwargs = kwargs

        # Iterates through sub-sections; makes recursive calls to this `__init__`.
        self.subsections = [
            subsection(
                key,
                typ(
                    root=root,
                    path_prefix=f'{path_prefix}{key}.',
                    **kwargs.get(key, {}),
                ),
            )
            for key, typ in self.__class__.__dict__.items()
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
            for key, typ in self.__class__.__annotations__.items()
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


class _configtype(allocateable):
    def __init__(self, path: str = util.resource.DEFAULT_CONFIG_PATH) -> None:
        '''
        Retrieves the game configuration data and serialises it through some weird custom method that I made in the `allocateable` class.
        '''
        self.data_transferer = None
        with open(util.resource.retr_config_full_path(path), 'rb') as f:
            self.data_dict: dict = tomli.load(f)
        super().__init__(root=self, **self.data_dict)

    def set_data_transferer(self, transferer: data_transfer._main.transferer):
        self.data_transferer = transferer
