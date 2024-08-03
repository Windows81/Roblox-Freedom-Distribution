from typing_extensions import Callable, Union, Any
from .._logic import base_type as config_base_type
from util.types import wrappers
import util.resource
import util.versions
import dataclasses
import functools
import os


@functools.cache
def get_type_call(object_type: type) -> Callable:
    if dataclasses.is_dataclass(object_type):
        return type_calls[dataclasses.dataclass]

    # Through `getattr`, hacky method to get callables.
    if getattr(object_type, '__origin__', None) == getattr(Callable, '__origin__'):
        return type_calls[Callable]

    if type(object_type) == type(str | None):
        return type_calls[Union]

    for k in object_type.mro():
        if k not in type_calls:
            continue
        return type_calls[k]
    else:
        return _type_call_default


def _type_call_default(value, config: config_base_type, typ: type, path: str, *args, **kwargs) -> Any:
    return typ(value, *args, **kwargs)


def _type_call_dicter(value: list, config: config_base_type, typ: type, path: str) -> Any:
    item_type: type = typ.item_type
    type_call = get_type_call(item_type)
    item_list = [
        type_call(
            item,
            config,
            item_type,
            path,
        )
        for item in value
    ]
    return typ(item_list)


def _type_call_with_config(value, config: config_base_type, typ: type, path: str, *args, **kwargs) -> Any:
    return typ(value, config, *args, **kwargs)


def _type_call_path_str(value, config: config_base_type, typ: type, path: str, *args, **kwargs) -> Any:
    return typ(value, os.path.dirname(config.config_path), *args, **kwargs)


def _type_call_rōblox_version(value, config: config_base_type, typ: type, path: str) -> util.versions.rōblox:
    return util.versions.rōblox.from_name(value)


def _type_call_callable(value, config: config_base_type, typ: type, path: str) -> Callable:
    result_typ = typ.__args__[-1]
    result_type_call = get_type_call(result_typ)

    def call(*args):
        return result_type_call(
            config.data_transferer.call(path, config, *args),
            config,
            result_typ,
            path,
        )
    return call


def _type_call_dataclass_as_dict(value, config: config_base_type, typ: type, path: str) -> Callable:
    '''
    Entries which are typed as `dataclass` in-program
    should be written as Python `dict` objects in the config file.
    This snippet is responsible for casting the `dict` to  a `dataclass`.
    '''
    fields = getattr(typ, dataclasses._FIELDS)  # type: ignore
    casted_values = {
        field_name: get_type_call(field.type)(
            value.get(field_name, field.default),
            config,
            field.type,
            path,
        )
        for field_name, field in fields.items()
    }
    return typ(**casted_values)


def _type_call_union(value, config: config_base_type, typ: type, path: str) -> Any | None:
    type_args: tuple[type] = typ.__args__
    if type_args[-1] == type(None):
        type_args = (type_args[-1], *type_args[:-1])
    for sub_typ in type_args:
        try:
            return get_type_call(sub_typ)(
                value,
                config,
                sub_typ,
                path,
            )
        except Exception:
            pass

    raise Exception(
        'Value "%s" is not of any of the following types: %s.' %
        (value, *', '.join(typ.__args__)),
    )


def _type_call_none_type(value, config: config_base_type, typ: type, path: str) -> None:
    if value is not None:
        raise Exception("Nothing can be `None`.")


type_calls = {
    Callable:
        _type_call_callable,
    util.versions.rōblox:
        _type_call_rōblox_version,
    wrappers.path_str:
        _type_call_path_str,
    wrappers.uri_obj:
        _type_call_path_str,
    wrappers.dicter:
        _type_call_dicter,
    dataclasses.dataclass:
        _type_call_dataclass_as_dict,
    Union:
        _type_call_union,
    type(None):
        _type_call_none_type,
}
