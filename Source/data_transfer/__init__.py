from config.types import callable
import functools


@functools.cache
def list_functions(game_config) -> dict:
    return {
        key: ann
        for key, ann in game_config.flatten().items()
        if isinstance(ann.val, callable.obj_type)
        and ann.val.call_mode == callable.call_mode_enum.lua
    }


@functools.cache
def get_rcc_snippet(game_config) -> str:
    return "_G.RFD = {%s}" % (
        '\n'.join(
            f'["{ann.path}"] = ({ann.rep});'
            for ann in list_functions(game_config).values()
        )
    )
