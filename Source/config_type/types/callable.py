# pyright: reportUnknownLambdaType=false

# Standard library imports
import dataclasses
import enum
import textwrap
import time

# Typing imports
from typing import Any, Callable, Hashable


class call_mode_enum(enum.Enum):
    assume = 'assume'
    lua = 'lua'
    python = 'python'
    dicted = 'dict'


@dataclasses.dataclass
class call_cache_data[R]:
    value: R
    tick: float


class obj_type[**P, R]:

    def __init__(
        self,
        rep,
        call_mode: call_mode_enum,
        path: str, config,
        caster_func,
    ) -> None:
        super().__init__()
        self.rep = rep
        self.config = config
        self.field_path = path
        self.caster_func = caster_func
        self.call_mode = (
            self.assume_call_mode()
            if call_mode == call_mode_enum.assume else
            call_mode
        )
        self.call_cache: dict[Hashable, call_cache_data[R]] = {}
        self._func = self.gen_function()

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
        result = self._func(*args, *kwargs.values())
        return self.caster_func(result)

    def cached_call(self, dur: float, key: Hashable, *args: P.args, **kwargs: P.kwargs) -> R:
        '''
        Wrapper function which caches the result of `__call__` for `dur` seconds.
        '''
        tick = time.time()
        existing = self.call_cache.get(key)
        if existing is not None and tick < existing.tick:
            return existing.value

        value = self.__call__(*args, **kwargs)
        self.call_cache[key] = call_cache_data(
            value=value,
            tick=tick + dur,
        )
        return value

    def assume_call_mode(self) -> call_mode_enum:
        rep = self.rep
        if isinstance(rep, str):
            checked = rep.strip()
            if checked.startswith('function'):
                return call_mode_enum.lua
            elif 'def ' in checked:
                return call_mode_enum.python
            return call_mode_enum.lua
        elif isinstance(rep, dict):
            return call_mode_enum.dicted
        elif isinstance(rep, Callable):
            return call_mode_enum.python
        raise Exception(
            "Config option at path `%s` isn't valid." %
            (self.field_path),
        )

    def gen_function(self) -> Callable[..., Any] | Any:
        match self.call_mode:
            case call_mode_enum.lua:
                def call_lua(*args):
                    return self.config.data_transferer.call(
                        self.field_path, self.config, *args,
                    )
                return call_lua
            case call_mode_enum.python:
                if isinstance(self.rep, Callable):
                    return lambda _, *a: self.rep(*a)
                local_vars = {}
                modded_rep = (
                    textwrap.dedent("""\
                    def func():
                    %(func_body)s
                        return next(
                            v
                            for v in reversed(locals().values())
                            if callable(v)
                        )
                    """) % {
                        'func_body': textwrap.indent(self.rep, ' ' * 4),
                    }
                )
                exec(
                    modded_rep,  # source
                    {  # globals
                        'CONFIG_DIR': self.config.base_dir,
                    },
                    local_vars,  # locals
                )
                result = local_vars['func']()
                return result
            case call_mode_enum.dicted:
                def call_dicted(*args):
                    assert isinstance(self.rep, dict)
                    arg_strs = [str(a) for a in args]
                    candidate_keys = [
                        *arg_strs,
                        '-'.join(arg_strs),
                        '_'.join(arg_strs),
                        ','.join(arg_strs),
                        ', '.join(arg_strs),
                        'default',
                    ]
                    return next(
                        (
                            self.rep[a]
                            for a in candidate_keys
                            if a in self.rep
                        ),
                        None,
                    )
                return call_dicted
            case _:
                raise Exception(
                    "Config option `%s` doesn't seem to be in a valid format." %
                    (self.field_path), )
