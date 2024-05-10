# This module is very convoluted and has one purpose: to serialise your `GameConfig.toml`.
# The data structure is defined in `./_main.py`.
# All you need to know is that the `_configtype` class will make your config file easier for your IDE's auto-complete to handle.

from typing_extensions import Self, Callable, Union, Any
import util.resource
import util.versions
import functools
import tomli


def _exec_type_call_default(typ: type, *a, **kwa) -> Any:
    return typ(*a, **kwa)


def _exec_type_call_callable(typ: type, v) -> functools._lru_cache_wrapper | None:
    if exec(v, {}, t := {}) == None:
        return functools.cache(t.get('RESULT'))  # type: ignore


def _exec_type_call_union(typ: type, v) -> Any | None:
    for t in typ.__args__:
        try:
            return t(v)
        except Exception:
            pass

    raise ValueError(
        'Value "%s" is not of any of the following types: %s' %
        (v, *', '.join(typ.__args__)),
    )


_TYPE_CALLS = {
    util.versions.rōblox: lambda cls, v: util.versions.rōblox.from_name(v),

    # Hacky method to get callables to resolve to the following lambda.
    getattr(Callable, '__origin__'): _exec_type_call_callable,

    Union: _exec_type_call_union,
}


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

    def __init__(self, **kwargs) -> None:
        # Iterates through individual settings in this section.
        for k, typ in self.__class__.__annotations__.items():
            setattr(
                self, k,
                allocateable.get_type_call(typ)(
                    typ,
                    kwargs.get(k, None),
                )
            )

        # Iterates through sub-sections; makes recursive calls to this `__init__`.
        for k, typ in self.__class__.__dict__.items():
            if not isinstance(typ, type):
                continue
            if not issubclass(typ, allocateable):
                continue
            setattr(
                self, k,
                self.get_type_call(typ)(
                    typ,
                    **kwargs[k],
                )
            )


class _configtype(allocateable):
    def __init__(self, path: str = util.resource.DEFAULT_CONFIG_PATH) -> None:
        '''
        Retrieves the game configuration data and serialises it through some weird custom method that I made in the `allocateable` class.
        '''
        with open(util.resource.retr_config_full_path(path), 'rb') as f:
            self.data_dict: dict = tomli.load(f)
        super().__init__(**self.data_dict)
