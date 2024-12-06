from typing_extensions import Callable, Union, Any
from ._logic import type_call_data
from . import wrappers, callable
import util.resource
import util.versions
import dataclasses
import functools
import os


@functools.cache
def get_type_call(object_type: type) -> Callable:
    if dataclasses.is_dataclass(object_type):
        return type_calls[dataclasses.dataclass]

    if type(object_type) == type(str | None):
        return type_calls[Union]

    for k in object_type.mro():
        if k not in type_calls:
            continue
        return type_calls[k]
    else:
        return _type_call_default


def _type_call_default(value, data: type_call_data, *args, **kwargs) -> Any:
    return data.typ(value, *args, **kwargs)


def _type_call_dicter(value: list, data: type_call_data) -> Any:
    item_type: type = data.typ.item_type
    type_call = get_type_call(item_type)
    new_data = dataclasses.replace(data, typ=item_type)
    item_list = [
        type_call(item, new_data)
        for item in value
    ]
    return data.typ(item_list)


def _type_call_with_config(value, data: type_call_data, *args, **kwargs) -> Any:
    return data.typ(value, data.config, *args, **kwargs)


def _type_call_path_str(value, data: type_call_data, *args, **kwargs) -> Any:
    return data.typ(value, os.path.dirname(data.config.file_path), *args, **kwargs)


def _type_call_rōblox_version(value, data: type_call_data) -> util.versions.rōblox:
    return util.versions.rōblox.from_name(value)


def _type_call_callable(value, data: type_call_data) -> Callable:
    result_typ = data.typ.__args__[-1]
    result_type_call = get_type_call(result_typ)

    call_mode_key = f'{data.key}_call_mode'
    call_mode_str = data.sibling_kwargs.get(call_mode_key)

    if isinstance(call_mode_str, str):
        call_mode = callable.call_mode_enum(call_mode_str)
    elif call_mode_str is None:
        call_mode = callable.call_mode_enum.assume
    else:
        raise Exception(
            "Config property `%s` is not a string "
        )

    def caster(result):
        return result_type_call(
            result,
            dataclasses.replace(data, typ=result_typ),
        )

    return callable.obj_type(
        rep=value,
        path=data.path,
        config=data.config,
        call_mode=call_mode,
        caster_func=caster,
    )


def _type_call_dataclass_as_dict(value, data: type_call_data) -> Callable:
    '''
    Entries which are typed as `dataclass` in-program
    should be written as Python `dict` objects in the config file.
    This snippet is responsible for casting the `dict` to  a `dataclass`.
    '''
    fields = getattr(data.typ, dataclasses._FIELDS)  # type: ignore
    casted_values = {
        field_name: get_type_call(field.type)(
            value.get(field_name, field.default),
            dataclasses.replace(data, typ=field.type),
        )
        for field_name, field in fields.items()
    }
    return data.typ(**casted_values)


def _type_call_union(value, data: type_call_data) -> Any | None:
    type_args: tuple[type] = data.typ.__args__
    if type_args[-1] == type(None):
        type_args = (type_args[-1], *type_args[:-1])
    for sub_typ in type_args:
        try:
            return get_type_call(sub_typ)(
                value,
                dataclasses.replace(data, typ=sub_typ),
            )
        except Exception:
            pass

    raise Exception(
        'Value "%s" is not of any of the following types: %s.' %
        (value, *', '.join(data.typ.__args__)),
    )


def _type_call_none_type(value, data: type_call_data) -> None:
    if value is not None:
        raise Exception(
            "Nothing that isn't `None` in `%s` can be `None`." %
            (data.path),
        )
    return None


type_calls = {
    callable.obj_type:
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
