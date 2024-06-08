from typing_extensions import Callable, Union, Any
from ._logic import base_type
import util.resource
import util.versions
import dataclasses
import functools
import os.path
import storage


class file_path(str):
    @staticmethod
    def evaluate(config: base_type, val: str) -> 'file_path':
        root = os.path.dirname(config.config_path)
        return file_path(os.path.join(root, val))


@functools.cache
def get_type_call(typ: type) -> Callable:
    if dataclasses.is_dataclass(typ):
        return type_calls[dataclasses.dataclass]

    # Through `getattr`, hacky method to get callables.
    if getattr(typ, '__origin__', None) == getattr(Callable, '__origin__'):
        return type_calls[Callable]

    for k in [
        typ,
    ]:
        if k not in type_calls:
            continue
        return type_calls[k]
    return _type_call_default


def _type_call_default(config: base_type, typ: type, path: str, *args, **kwargs) -> Any:
    return typ(*args, **kwargs)


def _type_call_storager(config: base_type, typ: type, path: str, val) -> storage.storager:
    full_path = file_path.evaluate(config, val)
    return storage.storager(full_path)


def _type_call_rōblox_version(config: base_type, typ: type, path: str, val) -> util.versions.rōblox:
    return util.versions.rōblox.from_name(val)


def _type_call_callable(config: base_type, typ: type, path: str, val) -> Callable:
    result_typ = typ.__args__[-1]
    result_type_call = get_type_call(result_typ)
    return lambda *args: result_type_call(
        config,
        result_typ,
        path,
        config.data_transferer.call(path, config, *args)
    )


def _type_call_dataclass(config: base_type, typ: type, path: str, val) -> Callable:
    return typ(**val)


def _type_call_file_path(config: base_type, typ: type, path: str, val) -> file_path:
    return file_path.evaluate(config, val)


def _type_call_union(config: base_type, typ: type, path: str, val) -> Any | None:
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


type_calls = {
    Callable:
        _type_call_callable,
    util.versions.rōblox:
        _type_call_rōblox_version,
    Union:
        _type_call_union,
    file_path:
        _type_call_file_path,
    dataclasses.dataclass:
        _type_call_dataclass,
    storage.storager:
        _type_call_storager,
}
