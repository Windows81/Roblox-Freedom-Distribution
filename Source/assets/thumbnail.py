from . import const, extractor
import json
import functools
import game_config
from config_type.types import wrappers


@functools.cache
def _get_icon_map() -> dict[int, 'wrappers.uri_obj']:
    config = game_config.get_cached_config()
    result = {}
    for gp in config.remote_data.gamepasses.values():
        if gp.icon is not None:
            result[gp.id_num] = gp.icon
    for dp in config.remote_data.devproducts.values():
        if dp.icon is not None:
            result[dp.id_num] = dp.icon
    return result


def transform_to_id_num(asset_id: str) -> int:
    asset_sub = asset_id[len(const.THUMB_PREFIX):-4]

    try:
        return int(asset_sub)
    except:
        return 0


def check(asset_id: str):
    return asset_id.startswith(const.THUMB_PREFIX)


def load_asset(asset_id: str) -> bytes | None:
    id = transform_to_id_num(asset_id)
    if id == 0:
        return None

    icon = _get_icon_map().get(id)
    if icon is not None:
        return icon.extract()

    raw = extractor.download_item(
        "https://thumbnails.roblox.com/v1/assets?assetids=%s&size=700x700&format=Png&isCircular=false" %
        (id,)
    )
    if raw is None:
        return None

    parsed = json.loads(raw)

    if "data" in parsed and len(parsed["data"]) != 1:
        return None

    return extractor.download_item(parsed["data"][0]['imageUrl'])
