# How This Module Works

The `./routers` directory contains a series of tasks. Every file except `./routers/_logic.py` is in itself a task module, but the task modules all import that `_logic.py`. Each routine runs in its own thread. Good for concurrent s\*\*t.

Each task module `T` has a `T.arg_type` and an `T.obj_type`. Both classes derive from one of a series of base types.

Each object `obj` of `T.obj_type` has a property `obj.local_args` of type `T.arg_type`.

`T.arg_type` is a Python dataclass and carries, for example, the header:

```py
@dataclasses.dataclass
class _arg_type(logic.bin_ssl_arg_type):
```

The `logic.bin_ssl_arg_type` can be replaced with any other `arg_type` class (including `arg_type` itself) in `./routines/_logic`.

**To further clarify**, here's a non-functional skeleton for any modules in `./routines` you wish to add. The `{***}` are placed where you add stuff.

```py
import launcher.routines._logic as logic
import dataclasses
{***} # Any other potential imports.


@dataclasses.dataclass
class _arg_type(logic.{***}arg_type):
    {***} # Dataclass fields.


class obj_type(logic.{***}entry):
    local_args: _arg_type

    def process(self) -> None:
        {***} # The routine code.


class arg_type(_arg_type):
    obj_type = obj_type
```
