from typing import Callable, Union, Any
from ._logic import type_call_data
from . import wrappers, callable
import util.versions
import dataclasses
import functools


@functools.cache
def get_type_call(object_type: type) -> Callable:
    if dataclasses.is_dataclass(object_type):
        return type_calls[dataclasses.dataclass]

    if isinstance(object_type, type(str | None)):
        return type_calls[Union]  # pyright: ignore[reportDeprecated]

    for k in object_type.mro():
        if k not in type_calls:
            continue
        return type_calls[k]
    else:
        return _type_call_default


def _type_call_default(value, call_data: type_call_data, *args, **kwargs) -> Any:
    return call_data.typ(value, *args, **kwargs)


def _type_call_dicter(value: list[Any] | dict[Any, Any], call_data: type_call_data) -> Any:
    item_type: type = call_data.typ.item_type
    key_name: str = call_data.typ.key_name
    type_call = get_type_call(item_type)
    new_data = dataclasses.replace(call_data, typ=item_type)

    if isinstance(value, list):
        value_list = value
    else:
        value_list = [
            {key_name: key} | item
            for key, item in value.items()
        ]

    item_list = [
        type_call(item, new_data)
        for item in value_list
    ]
    return call_data.typ(item_list)


def _type_call_with_config(value, call_data: type_call_data, *args, **kwargs) -> Any:
    return call_data.typ(value, call_data.config, *args, **kwargs)


def _type_call_path_str(value, call_data: type_call_data, *args, **kwargs) -> Any:
    return call_data.typ(value, call_data.config.base_dir, *args, **kwargs)


def _type_call_rōblox_version(value, call_data: type_call_data) -> util.versions.rōblox:
    return util.versions.rōblox.from_name(value)


def _type_call_callable(value, call_data: type_call_data) -> Callable:
    result_typ = call_data.typ.__args__[-1]
    result_type_call = get_type_call(result_typ)

    call_mode_key = f'{call_data.key}_call_mode'
    call_mode_str = call_data.sibling_kwargs.get(call_mode_key)

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
            dataclasses.replace(call_data, typ=result_typ),
        )

    return callable.obj_type(
        rep=value,
        path=call_data.path,
        config=call_data.config,
        call_mode=call_mode,
        caster_func=caster,
    )


def _type_call_dataclass_as_dict(value, call_data: type_call_data) -> Callable:
    '''
    Entries which are typed as `dataclass` in-program
    should be written as Python `dict` objects in the config file.
    This snippet is responsible for casting the `dict` to  a `dataclass`.
    '''
    fields = getattr(
        call_data.typ,
        dataclasses._FIELDS,  # type: ignore[reportAttributeAccessIssue]
    )
    casted_values = {
        field_name: get_type_call(field.type)(
            value.get(field_name, field.default),
            dataclasses.replace(call_data, typ=field.type),
        )
        for field_name, field in fields.items()
    }
    return call_data.typ(**casted_values)


def _type_call_union(value, call_data: type_call_data) -> Any | None:
    type_args: tuple[type] = call_data.typ.__args__
    if isinstance(None, type_args[-1]):
        type_args = (type_args[-1], *type_args[:-1])
    for sub_typ in type_args:
        try:
            return get_type_call(sub_typ)(
                value,
                dataclasses.replace(call_data, typ=sub_typ),
            )
        except Exception:
            pass

    raise Exception(
        'Value "%s" is not of any of the following types: %s.' %
        (value, *', '.join(call_data.typ.__args__)),
    )


def _type_call_none_type(value, call_data: type_call_data) -> None:
    if value is not None:
        raise Exception(
            "Nothing that isn't `None` in `%s` can be `None`." %
            (call_data.path),
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
    Union:  # pyright: ignore[reportDeprecated]
        _type_call_union,
    type(None):
        _type_call_none_type,
}
