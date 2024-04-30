from typing_extensions import Self, Callable
import collections.abc
import util.resource
import util.versions
import functools
import tomli


class path(str):
    def __new__(cls, val: str) -> Self:
        return str.__new__(cls, util.resource.retr_full_path(util.resource.dir_type.CONFIG, val))


class allocateable:
    TYPE_CALLS = {
        util.versions.rōblox: util.versions.rōblox.from_name,
        collections.abc.Callable: lambda v:
            exec(v, {}, t := {}) == None and
            functools.cache(t.get('RESULT')),
    }

    @classmethod
    @functools.cache
    def get_type_call(cls, typ: type) -> Callable:
        for k in [
            typ,
            getattr(typ, '__origin__', None),
        ]:
            if k not in cls.TYPE_CALLS:
                continue
            return cls.TYPE_CALLS[k]
        return typ

    def __init__(self, **kwargs) -> None:
        for k, typ in self.__class__.__annotations__.items():
            setattr(
                self, k,
                allocateable.get_type_call(typ)(
                    kwargs[k],
                )
            )
        for k, typ in self.__class__.__dict__.items():
            if isinstance(typ, type) and issubclass(typ, allocateable):
                setattr(
                    self, k,
                    self.get_type_call(typ)(
                        **kwargs[k],
                    )
                )


class _configtype(allocateable):
    def __init__(self, path: str = util.resource.DEFAULT_CONFIG_PATH) -> None:
        with open(util.resource.retr_config_full_path(path), 'rb') as f:
            self.data_dict: dict = tomli.load(f)
        super().__init__(**self.data_dict)
