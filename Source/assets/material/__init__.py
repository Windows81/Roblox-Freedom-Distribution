from .. import grabber
from . import const


def transform_to_id_num(asset_id: str):
    asset_sub = asset_id[len(const.ID_PREFIX):]

    # TODO: don't make it 7.
    return const.MATERIAL_DICT_2022.get(asset_sub, 7)
