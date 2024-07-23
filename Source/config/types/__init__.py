from typing_extensions import Callable, Union, Any
from .._logic import base_type as config_base_type
from . import wrappers
import util.resource
import util.versions
import dataclasses
import functools


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
    else:
        return _type_call_default


def _type_call_default(config: config_base_type, typ: type, path: str, *args, **kwargs) -> Any:
    return typ(*args, **kwargs)


def _type_call_with_config(config: config_base_type, typ: type, path: str, *args, **kwargs) -> Any:
    return typ(config, *args, **kwargs)


def _type_call_rōblox_version(config: config_base_type, typ: type, path: str, val) -> util.versions.rōblox:
    return util.versions.rōblox.from_name(val)


def _type_call_callable(config: config_base_type, typ: type, path: str, val) -> Callable:
    result_typ = typ.__args__[-1]
    result_type_call = get_type_call(result_typ)
    return lambda *args: result_type_call(
        config,
        result_typ,
        path,
        config.data_transferer.call(path, config, *args)
    )


def _type_call_dataclass_as_dict(config: config_base_type, typ: type, path: str, val) -> Callable:
    '''
    Entries typed as `dataclass` in-program are written as Python `dict` objects in the config file.
    This snippet is responsible for casting the `dict` to  a `dataclass`.
    '''
    return typ(**val)


def _type_call_union(config: config_base_type, typ: type, path: str, val) -> Any | None:
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
    wrappers.path_str:
        _type_call_with_config,
    wrappers.uri_obj:
        _type_call_with_config,
    dataclasses.dataclass:
        _type_call_dataclass_as_dict,
}
