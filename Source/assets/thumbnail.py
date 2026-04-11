from . import const, extractor
import json

def transform_to_id_num(asset_id: str) -> int:
    asset_sub = asset_id[len(const.THUMB_PREFIX):-4] # strip .png

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

    # technically we could also download the decal and parse its contents
    # to extract the thumbnail, but that might be overkill
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