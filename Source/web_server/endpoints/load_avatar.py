from web_server._logic import web_server_handler, server_path
import util.versions as versions
from config import obj_type


class avatar_data:
    def __init__(self, game_config: obj_type, user_code: str) -> None:
        self.type = game_config.server_core\
            .retrieve_avatar_type(user_code)
        self.items = game_config.server_core\
            .retrieve_avatar_items(user_code)
        self.scales = game_config.server_core\
            .retrieve_avatar_scales(user_code)
        self.colors = game_config.server_core\
            .retrieve_avatar_colors(user_code)


@server_path('/v1.1/avatar-fetch/', versions={versions.rōblox.v348})
def _(self: web_server_handler) -> bool:
    '''
    Character appearance for v348.
    '''
    database = self.server.database.players

    id_num = self.query.get('userId')
    user_code = database.get_player_field_from_index(
        database.player_field.ID_NUMBER,
        id_num,
        database.player_field.USER_CODE,
    )

    if user_code is None:
        return False

    avatar = avatar_data(self.game_config, user_code)
    self.send_json({
        "animations": {},
        "resolvedAvatarType": avatar.type.name,
        "accessoryVersionIds": avatar.items,
        "equippedGearVersionIds": [],
        "backpackGearVersionIds": [],
        "bodyColors": {
            "HeadColor": avatar.colors.head,
            "LeftArmColor": avatar.colors.left_arm,
            "LeftLegColor": avatar.colors.left_leg,
            "RightArmColor": avatar.colors.right_arm,
            "RightLegColor": avatar.colors.right_leg,
            "TorsoColor": avatar.colors.torso,
        },
        "scales": {
            "Height": avatar.scales.height,
            "Width": avatar.scales.width,
            "Head": avatar.scales.head,
            "Depth": avatar.scales.depth,
            "Proportion": avatar.scales.proportion,
            "BodyType": avatar.scales.body_type,
        },
    })
    return True


@server_path('/v1/avatar', versions={versions.rōblox.v463})
@server_path('/v1/avatar/', versions={versions.rōblox.v463})
@server_path('/v1/avatar-fetch', versions={versions.rōblox.v463})
@server_path('/v1/avatar-fetch/', versions={versions.rōblox.v463})
def _(self: web_server_handler) -> bool:
    '''
    Character appearance for v463.
    TODO: properly implement avatars.
    '''
    database = self.server.database.players

    id_num = self.query.get('userId')
    user_code = database.get_player_field_from_index(
        database.player_field.ID_NUMBER,
        id_num,
        database.player_field.USER_CODE,
    )

    if user_code is None:
        return False

    avatar = avatar_data(self.game_config, user_code)
    self.send_json({
        "resolvedAvatarType": avatar.type.name,
        "equippedGearVersionIds": [],
        "backpackGearVersionIds": [],
        "assetAndAssetTypeIds": [
            {
                "assetId": item,
                "assetTypeId": 8
            }
            for item in avatar.items
        ],
        "animationAssetIds": {
            "run": 2510238627,
            "jump": 2510236649,
            "fall": 2510233257,
            "climb": 2510230574
        },
        "bodyColors": {
            "headColorId": avatar.colors.head,
            "leftArmColorId": avatar.colors.left_arm,
            "leftLegColorId": avatar.colors.left_leg,
            "rightArmColorId": avatar.colors.right_arm,
            "rightLegColorId": avatar.colors.right_leg,
            "torsoColorId": avatar.colors.torso,
        },
        "scales": {
            "height": avatar.scales.height,
            "width": avatar.scales.width,
            "head": avatar.scales.head,
            "depth": avatar.scales.depth,
            "proportion": max(avatar.scales.proportion, 1e-2),
            "bodyType": max(avatar.scales.body_type, 1e-2),
        },
        "emotes": [
            {
                "assetId": 3696763549,
                "assetName": "Heisman Pose",
                "position": 1
            },
            {
                "assetId": 3360692915,
                "assetName": "Tilt",
                "position": 2
            },
            {
                "assetId": 3696761354,
                "assetName": "Air Guitar",
                "position": 3
            },
            {
                "assetId": 3576968026,
                "assetName": "Shrug",
                "position": 4
            },
            {
                "assetId": 3576686446,
                "assetName": "Hello",
                "position": 5
            },
            {
                "assetId": 3696759798,
                "assetName": "Superhero Reveal",
                "position": 6
            },
            {
                "assetId": 3360689775,
                "assetName": "Salute",
                "position": 7
            },
            {
                "assetId": 3360686498,
                "assetName": "Stadium",
                "position": 8
            }
        ]
    })
    return True
