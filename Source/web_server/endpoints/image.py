import gzip
import json
import re
from typing import Any

import util
import assets.returns as returns
from web_server._logic import web_server_handler, server_path


def handle_resolution_check(
        self: web_server_handler,
        width_parameters_name: list[str] = ['width', 'x'],
        height_parameters_name: list[str] = ['height', 'y'],
        allowed_widths: list[int] = [48, 180, 420, 60, 100, 150, 352, 200, 500],
        allowed_heights: list[int] = [48, 180, 420, 60, 100, 150, 352, 200, 500],
        must_be_square: bool = True,
        can_round_to_nearest: bool = True
) -> (int, int):
    """
        Handles resolution checking for images. Aborts the request if the resolution is invalid.
        Must be called in a flask request context.

        :param width_parameters_name: The names of valid parameters for width.
        :param height_parameters_name: The names of valid parameters for height.
        :param allowed_widths: The allowed widths.
        :param allowed_heights: The allowed heights.
        :param must_be_square: Whether or not the image must be square.
        :param can_round_to_nearest: Whether or not the image can round to the nearest resolution.

        :return: ( width, height )
    """
    width: int = 0
    height: int = 0
    for WidthParameterName in width_parameters_name:
        if WidthParameterName in self.query:
            width = int(self.query.get(WidthParameterName))
            break
    for HeightParameterName in height_parameters_name:
        if HeightParameterName in self.query:
            height = int(self.query.get(HeightParameterName))
            break

    if width is None or height is None:
        self.send_response(400)
    if (width not in allowed_widths or height not in allowed_heights) and not can_round_to_nearest:
        self.send_response(400)
    if must_be_square and width != height:
        self.send_response(400)

    if can_round_to_nearest:
        if width not in allowed_widths:
            width = min(allowed_widths, key=lambda x: abs(x - width))
        if height not in allowed_heights:
            height = min(allowed_heights, key=lambda x: abs(x - height))

    return width, height


def handle_image_resize(
        self: web_server_handler,
        image_content_hash: str,
        target_width: int,
        target_height: int,
        cropped_hash: str,
        cache_control: str = "max-age=120",
        skip_cache_cropped_image: bool = False,
) -> Any:
    """
        Handles image resizing

        :param image_content_hash: The content hash of the image.
        :param target_width: The target width.
        :param target_height: The target height.
        :param cropped_hash: The hash of the cropped image.

        :return: JSON
    """
    # if s3helper.DoesKeyExist(CroppedHash) and not SkipCacheCroppedImage:
    #     if ReturnAsJSON:
    #         return jsonify({
    #             "Final": True,
    #             "Url": f"{config.CDN_URL}/{CroppedHash}"
    #         })
    #     ImageResponse = make_response(redirect(f"{config.CDN_URL}/{CroppedHash}"))
    #     ImageResponse.headers['Cache-Control'] = CacheControl
    #     return ImageResponse
    #
    # if not s3helper.DoesKeyExist(ImageContentHash):
    #     if ReturnAsJSON:
    #         return jsonify({
    #             "Final": False,
    #             "Url": "/static/img/placeholder.png"
    #         })
    #     return redirect("/static/img/placeholder.png")
    #
    # ImageContent = BytesIO(s3helper.GetFileFromS3(ImageContentHash))
    # ImageObj = Image.open(ImageContent)
    # ImageObj = ImageObj.resize((int(TargetWidth), int(TargetHeight))).convert('RGBA')
    #
    # VirtualFile = BytesIO()
    # ImageObj.save(VirtualFile, "PNG")
    # VirtualFile.seek(0)
    # s3helper.UploadBytesToS3(VirtualFile.getvalue(), CroppedHash, contentType="image/png")
    #
    # if ReturnAsJSON:
    #     return jsonify({
    #         "Final": True,
    #         "Url": f"{config.CDN_URL}/{CroppedHash}"
    #     })
    # ImageResponse = make_response(self.send_redirect(f"{config.CDN_URL}/{CroppedHash}"))
    # ImageResponse.headers['Cache-Control'] = CacheControl
    # return ImageResponse


def send_thumbnail_content(
        self: web_server_handler,
        content_hash: str | None,
) -> bool:
    if content_hash is None:
        self.send_error(404)
        return True

    asset = self.game_config.asset_cache.get_asset(
        content_hash,
        bypass_blocklist=self.is_privileged,
    )
    if isinstance(asset, returns.ret_data):
        self.send_data(asset.data)
        return True
    if isinstance(asset, returns.ret_none):
        self.send_error(404)
        return True
    if isinstance(asset, returns.ret_relocate):
        self.send_redirect(asset.url)
        return True
    return False


@server_path(r'/Thumbs/GameIcon.ashx')
@server_path(r'/Thumbs/PlaceIcon.ashx')
def _(self: web_server_handler) -> bool:
    asset_cache = self.game_config.asset_cache
    thumbnail_data = asset_cache.get_asset(util.const.THUMBNAIL_ID_CONST)
    if isinstance(thumbnail_data, returns.ret_data):
        self.send_data(thumbnail_data.data)
    return True

@server_path(r'/v1/games/icons', commands={'GET'})
def _(self: web_server_handler) -> bool:
    self.send_response(200)
    self.send_header("Content-Type", "application/json")
    self.send_json({
        "data": [{
            "targetId": 67,
            "state": "Completed",
            "imageUrl": f"{self.hostname}/Thumbs/PlaceIcon.ashx?assetId=496&x=420&y=420",
            "version": "TN3"
        }]
    })
    return True

@server_path(r'/Game/Tools/ThumbnailAsset.ashx', commands={'GET'})
def _(self: web_server_handler) -> bool:
    asset_cache = self.game_config.asset_cache

    expected_format: str = self.query['fmt']
    asset_id: int = self.query['aid']

    if asset_id is None:
        self.send_redirect("/static/img/placeholder.png")
        return True
    if expected_format.lower() != "png":
        self.send_redirect("/static/img/placeholder.png")
        return True

    asset = asset_cache.get_asset(
        asset_id,
        bypass_blocklist=self.is_privileged,
    )
    if asset is None:
        self.send_redirect("/static/img/placeholder.png")
        return True

    if isinstance(asset, returns.ret_data):
        self.send_data(asset.data)
        return True
    elif isinstance(asset, returns.ret_none):
        self.send_error(404)
        return True
    elif isinstance(asset, returns.ret_relocate):
        self.send_redirect(asset.url)
        return True
    return False

@server_path(r'/v1/batch', commands={'POST'})
def _(self: web_server_handler) -> bool:
    if self.headers['Content-Encoding'] == 'gzip':
        try:
            data = gzip.decompress(self.rfile.read())
        except Exception as e:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.send_json({"success": False, "message": "Invalid gzip data"})
            return True
        try:
            json_data = json.loads(data)
        except Exception as e:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.send_json({"success": False, "message": "Invalid JSON data"})
            return True
    else:
        json_data = self.rfile.read()
    if json_data is None:
        self.send_response(400)
        self.send_header("Content-Type", "application/json")
        self.send_json({"success": False, "message": "Missing JSON data"})
        return True

    # [{'requestId': 'type=GameIcon&id=1&w=128&h=128&filters=', 'targetId': 1, 'type': 'GameIcon', 'size': '128x128', 'isCircular': False}]

    if len(json_data) > 15:
        self.send_response(400)
        self.send_header("Content-Type", "application/json")
        self.send_json({"success": False, "message": "Too many requests"})
        return True
    if len(json_data) == 0:
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_json({"data": []})
        return True

    processed_requests = []
    for request_obj in json_data:
        if "requestId" not in request_obj or "targetId" not in request_obj or "type" not in request_obj or "size" not in request_obj:
            continue
        if request_obj["type"] not in ["Avatar", "AvatarHeadShot", "GameIcon", "GameThumbnail", "Asset", "GroupIcon"]:
            continue

        if "x" not in request_obj["size"]:
            continue
        split_size = request_obj["size"].split("x")
        if len(split_size) != 2:
            continue
        try:
            target_width = int(split_size[0])
            target_height = int(split_size[1])
        except:
            continue

        allowed_sizes = [48, 180, 420, 60, 100, 150, 352, 396, 480, 512, 576, 700, 768, 640, 36, 1280, 720]
        target_width = min(allowed_sizes, key=lambda x: abs(x - target_width))
        target_height = min(allowed_sizes, key=lambda x: abs(x - target_height))

        request_type = request_obj["type"]

        # if request_type == "Avatar":
        #     thumbnail_obj: UserThumbnail = UserThumbnail.query.filter_by(userid=request_obj["targetId"]).first()
        #     if thumbnail_obj is None:
        #         continue
        #     content_hash = thumbnail_obj.full_contenthash
        # elif request_type == "AvatarHeadShot":
        #     thumbnail_obj: UserThumbnail = UserThumbnail.query.filter_by(userid=request_obj["targetId"]).first()
        #     if thumbnail_obj is None:
        #         continue
        #     content_hash = thumbnail_obj.headshot_contenthash
        # elif request_type == "GameIcon":
        #     place_icon_obj: PlaceIcon = PlaceIcon.query.filter_by(placeid=request_obj["targetId"]).first()
        #     if place_icon_obj is None:
        #         continue
        #     content_hash = place_icon_obj.contenthash
        # elif request_type == "GameThumbnail" or request_type == "Asset":
        #     thumbnail_obj: AssetThumbnail = AssetThumbnail.query.filter_by(asset_id=request_obj["targetId"]).order_by(
        #         AssetThumbnail.asset_version_id.desc()).first()
        #     if thumbnail_obj is None:
        #         continue
        #     if thumbnail_obj.moderation_status != 0:
        #         continue
        #     content_hash = thumbnail_obj.content_hash
        # elif request_type == "GroupIcon":
        #     thumbnail_obj: GroupIcon = GroupIcon.query.filter_by(group_id=request_obj["targetId"]).first()
        #     if thumbnail_obj is None:
        #         continue
        #     if thumbnail_obj.moderation_status != 0:
        #         continue
        #     content_hash = thumbnail_obj.content_hash
        # else:
        #     continue
        # cropped_hash = hashlib.sha512(f"{content_hash}-{target_width}-{target_height}-v3".encode('utf-8')).hexdigest()
        # if not s3helper.DoesKeyExist(cropped_hash):
        #     if not s3helper.DoesKeyExist(content_hash):
        #         continue
        #     ImageContent = BytesIO(s3helper.GetFileFromS3(content_hash))
        #     ImageObj = Image.open(ImageContent)
        #     ImageObj = ImageObj.resize((int(target_width), int(target_height))).convert('RGBA')
        #
        #     VirtualFile = BytesIO()
        #     ImageObj.save(VirtualFile, "PNG")
        #     VirtualFile.seek(0)
        #     s3helper.UploadBytesToS3(VirtualFile.getvalue(), cropped_hash, contentType="image/png")
        processed_requests.append({
            "requestId": request_obj["requestId"],
            "targetId": request_obj["targetId"],
            "state": "Completed",
            "imageUrl": f"{self.hostname}/Thumbs/PlaceIcon.ashx?assetId=496&x=420&y=420", # f"{config.CDN_URL}/{CroppedHash}",
            "version": None
        })

    self.send_response(200)
    self.send_header("Content-Type", "application/json")
    self.send_json({"data": processed_requests})
    return True

@server_path(r'/Thumbs/Head.ashx', commands={'GET'})
@server_path(r'/headshot-thumbnail/image', commands={'GET'})
def _(self: web_server_handler) -> bool:
    user_id = self.query.get('userId')
    if user_id is None:
        self.send_error(400)
        return True

    try:
        user_id_num = int(user_id)
    except ValueError:
        self.send_error(400)
        return True

    thumbnail_obj = self.server.storage.userthumbnail.check(user_id_num)
    if thumbnail_obj is None:
        self.send_error(404)
        return True

    return send_thumbnail_content(self, thumbnail_obj[1])


@server_path(r'/v1/users/avatar-headshot', commands={'GET'})
def _(self: web_server_handler) -> bool:
    user_ids_csv = self.query.get('userIds')
    if user_ids_csv is None:
        self.send_json({"errors": [{"code": 4, "message": "The requested Ids are invalid, of an invalid type or missing."}]}, 400)
        return False

    user_ids = user_ids_csv.split(',')
    if len(user_ids) > 100:
        self.send_json({"errors": [{"code": 1, "message": "There are too many requested Ids."}]}, 400)
        return False

    requested_size = self.query.get('size') or "48x48"

    if "x" not in requested_size:
        self.send_json({"errors": [{"code": 3, "message": "The requested size is invalid. Please see documentation for valid thumbnail size parameter name and format."}]},400)
        return False

    splitted_size = requested_size.split("x")
    if len(splitted_size) != 2:
        self.send_json({"errors": [{"code": 3,"message": "The requested size is invalid. Please see documentation for valid thumbnail size parameter name and format."}]},400)
        return False

    try:
        thumbnail_width = int(splitted_size[0])
        thumbnail_height = int(splitted_size[1])

        allowed_sizes = [48,180,420,60,100,150,352,396,480,512,576,700,768,640,36,1280,720]
        thumbnail_width = min(allowed_sizes, key=lambda x: abs(x - thumbnail_width))
        thumbnail_height = min(allowed_sizes, key=lambda x: abs(x - thumbnail_height))
    except:
        self.send_json({"errors": [{ "code": 3, "message": "The requested size is invalid. Please see documentation for valid thumbnail size parameter name and format."}]}, 400)
        return False

    processed_requests = []
    storage = self.server.storage
    for user_id in user_ids:
        try:
            user_id = int(user_id)
        except:
            continue

        thumbnail_obj = storage.userthumbnail.check(user_id)
        if thumbnail_obj is None:
            continue
        headshot_contenthash = thumbnail_obj[1]
        if headshot_contenthash is None:
            continue
        # if not s3helper.DoesKeyExist(cropped_hash):
        #     if not s3helper.DoesKeyExist(content_hash):
        #         continue
        #     image_content = BytesIO(s3helper.GetFileFromS3(content_hash))
        #     image_obj = Image.open(image_content)
        #     image_obj = image_obj.resize((int(thumbnail_width), int(thumbnail_height))).convert('RGBA')
        #
        #     virtual_file = BytesIO()
        #     image_obj.save(virtual_file, "PNG")
        #     virtual_file.seek(0)
        #     s3helper.UploadBytesToS3(virtual_file.getvalue(), cropped_hash, contentType="image/png")
        processed_requests.append({
            "targetId": user_id,
            "state": "Completed",
            "imageUrl": f"{self.hostname}/headshot-thumbnail/image?userId={user_id}&x={thumbnail_width}&y={thumbnail_height}",
            "version": "1"
        })

    self.send_json({"data": processed_requests}, 200)
    return True

# Placeholder data
# TODO: Implement API logic
@server_path(r'/v1/users/avatar-3d', regex=True, commands={'GET'})
@util.auth.authenticated_required_api
def _(self: web_server_handler, match: re.Match[str]) -> bool:
    self.send_json({"targetId":1,"state":"Completed","imageUrl":"https://t3.rbxcdn.com/30DAY-Avatar-310966282D3529E36976BF6B07B1DC90-Obj","version":"TN3"}, 200)
    return True

# Placeholder data
# TODO: Implement API logic
@server_path(r'/v1/users/avatar', regex=True, commands={'GET'})
@util.auth.authenticated_required_api
def _(self: web_server_handler, match: re.Match[str]) -> bool:
    self.send_json({"data":[{"targetId":1,"state":"Completed","imageUrl":"https://tr.rbxcdn.com/30DAY-Avatar-310966282D3529E36976BF6B07B1DC90-Png/420/420/Avatar/Png/noFilter","version":"TN3"}]}, 200)
    return True
