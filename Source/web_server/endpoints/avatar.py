from web_server._logic import web_server_handler, server_path
from config_type.types import structs, wrappers
import util.versions as versions
from game_config import obj_type


def get_avatar(id_num: int, game_config: obj_type) -> structs.avatar_data:
    user_code = get_user_code(id_num, game_config)
    return game_config.server_core.retrieve_avatar(id_num, user_code)


def get_user_code(id_num: int, game_config: obj_type) -> str | None:
    database = game_config.storage.players
    user_code = database.get_player_field_from_index(
        database.player_field.ID_NUMBER,
        id_num,
        database.player_field.USER_CODE,
    )
    if user_code is None:
        return None
    return user_code[0]


@server_path('/v1.1/avatar-fetch/', versions={versions.rōblox.v348})
def _(self: web_server_handler) -> bool:
    '''
    Character appearance for v348.
    '''
    id_num = int(self.query['userId'])
    avatar = get_avatar(id_num, self.game_config)

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
    '''
    id_num = int(self.query['userId'])
    avatar = get_avatar(id_num, self.game_config)

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


@server_path('/v1.1/game-start-info', versions={versions.rōblox.v463})
def _(self: web_server_handler) -> bool:
    '''
    https://github.com/Heliodex/Meteorite/blob/76d53e75dace3195c1068e0de66c137376a88bcf/Back/server.mjs#L3718
    '''
    self.send_json({
        "gameAvatarType": "PlayerChoice",
        "allowCustomAnimations": "True",
        "universeAvatarCollisionType": "OuterBox",
        "universeAvatarBodyType": "Standard",
        "jointPositioningType": "ArtistIntent",
        "universeAvatarMinScales": {
            "height": -1e17,
            "width": -1e17,
            "head": -1e17,
            "depth": -1e17,
            "proportion": -1e17,
            "bodyType": -1e17,
        },
        "universeAvatarMaxScales": {
            "height": +1e17,
            "width": +1e17,
            "head": +1e17,
            "depth": +1e17,
            "proportion": +1e17,
            "bodyType": +1e17,
        },
        "universeAvatarAssetOverrides": [],
        "moderationStatus": None,
    })
    return True
