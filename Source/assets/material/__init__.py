from . import const
import urllib3


def transform_to_id_num(asset_id: str) -> int:
    asset_sub = asset_id[len(const.ID_PREFIX):]

    result = const.MATERIAL_DICT_2022.get(asset_sub, 153465633)
    return result


def load_asset(asset_id: str) -> bytes | None:
    asset_sub = asset_id[len(const.ID_PREFIX):]
    # TODO: make material URL scheme more flexible.
    url = (
        'https://github.com/Windows81/Roblox-Materials/raw/main/textures/Extrapolated2022/' +
        '/'.join(asset_sub.split('-'))
    )

    http = urllib3.PoolManager()
    response = http.request('GET', url)
    if response.status == 200:
        return response.data
