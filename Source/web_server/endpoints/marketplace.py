# Standard library imports
import urllib.parse
import json
import re
from datetime import datetime

from urllib3 import request

# Local application imports
from web_server._logic import web_server_handler, server_path
import util.const
from enums.AssetType import AssetType


def purchase_gamepass(self: web_server_handler, user_id_num: int, gamepass_id: int):
    gamepass = self.game_config.remote_data.gamepasses.get(gamepass_id)

    if gamepass is None:
        return False  # Gamepass does not exist

    storage = self.server.storage
    if storage.gamepasses.check(user_id_num, gamepass_id):
        return False  # You already own this!

    funds = storage.funds.check(user_id_num)
    if funds is None:
        return False  # Couldn't load funds

    if funds < gamepass.price:
        return False  # Too poor!

    storage.gamepasses.update(user_id_num, gamepass_id)
    storage.funds.add(user_id_num, -1 * gamepass.price)
    return True


def purchase_devproduct(self: web_server_handler, user_id_num: int, devproduct_id: int) -> str | None:
    devproduct = self.game_config.remote_data.devproducts.get(devproduct_id)

    if devproduct is None:
        return  # Gamepass does not exist

    storage = self.server.storage
    funds = storage.funds.check(user_id_num)
    if funds is None:
        return  # Couldn't load funds

    if funds < devproduct.price:
        return  # Too poor!

    storage.devproducts.update(user_id_num, devproduct_id)
    storage.funds.add(user_id_num, -1 * devproduct.price)
    return f"{devproduct_id}-{user_id_num}"


def _format_api_datetime(value: str | None) -> str | None:
    if value is None:
        return None
    try:
        return datetime.fromisoformat(value).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    except ValueError:
        return value


def _get_creator_name(self: web_server_handler, creator_type: int, creator_id: int) -> str:
    if creator_type == 0:
        username = self.server.storage.players.get_player_field_from_index(
            index=self.server.storage.players.player_field.IDEN_NUM,
            value=creator_id,
            field=self.server.storage.players.player_field.USERNAME,
        )
        if isinstance(username, str):
            return username
    return str(creator_id)


def _parse_catalog_items_request(self: web_server_handler) -> list[dict]:
    if 'items' in self.query:
        parsed = json.loads(self.query['items'])
        if isinstance(parsed, dict):
            return list(parsed.get('items', []))
        if isinstance(parsed, list):
            return parsed

    if 'itemIds' in self.query:
        return [
            {
                "id": int(item_id),
                "itemType": "Asset",
            }
            for item_id in self.query['itemIds'].split(',')
            if item_id.strip()
        ]

    content_length = int(self.headers.get('content-length', 0))
    if content_length <= 0:
        return []

    parsed = json.loads(self.read_content())
    if isinstance(parsed, dict):
        return list(parsed.get('items', []))
    if isinstance(parsed, list):
        return parsed
    return []


@server_path('/Game/GamePass/GamePassHandler.ashx', commands={'GET'})
def _(self: web_server_handler) -> bool:
    '''
    TODO: handle social requests.
    '''
    match self.query['Action']:
        case 'HasPass':
            def check() -> bool:
                gamepass_id = int(self.query['PassID'])
                user_id = int(self.query['UserID'])
                return self.server.storage.gamepasses.check(user_id, gamepass_id) is not None

            self.send_data(bytes(
                '<Value Type="boolean">' +
                ("true" if check() else "false") +
                '</Value>',
                encoding='utf-8',
            ))
            return True
        case _:
            pass

    self.send_json({})
    return True


@server_path(r'/v1/purchases/products/(\d+)', regex=True)
def _(self: web_server_handler, match: re.Match[str]) -> bool:
    '''
    https://github.com/SushiDesigner/Meteor-back/blob/dc561b5af196ca9c375530d30d593fc8d7f0486c/routes/marketplace.js#L157
    '''
    gamepass_id = int(match[1])

    # TODO: actually make gamepass sales secure.
    user_id_num = json.loads(self.headers['Roblox-Session-Id'])['UserId']

    if purchase_gamepass(self, user_id_num, gamepass_id):
        self.send_json({
            "purchased": True,
            "reason": "Success",
            "productId": gamepass_id,
            "currency": 1,
            "price": 0,
            "assetId": gamepass_id,
            "assetName": "",
            "assetType": "Gamepass",
            "assetTypeDisplayName": "Gamepass",
            "assetIsWearable": False,
            "sellerName": "",
            "transactionVerb": "bought",
            "isMultiPrivateSale": False,
        })
    else:
        self.send_json({
            "purchased": False,
            "reason": "InsufficientFunds",
            "productId": gamepass_id,
            "statusCode": 500,
            "title": "Not Enough Robux",
            "errorMsg": "You do not have enough Robux to purchase this item.",
            "showDivId": "InsufficientFundsView",
        })
    return True


@server_path(r'/v2/developer-products/(\d+)/purchase', regex=True)
def _(self: web_server_handler, match: re.Match[str]) -> bool:
    '''
    https://github.com/Username10101023/RobloxLabsTemp/blob/cc3fcd0df84e515af76cffa05afeab1367711630/StaticPages/ApiSites/Roblox.Economy.Api/docs/json/v2.json#L275
    '''
    devproduct_id = int(match[1])

    # TODO: actually make gamepass sales secure.
    user_id_num = json.loads(self.headers['Roblox-Session-Id'])['UserId']

    receipt = purchase_devproduct(self, user_id_num, devproduct_id)
    if receipt is not None:
        self.send_json({
            "purchased": True,
            "success": True,
            "transactionStatus": "Success",
            "productId": user_id_num,
            "price": 0,
            "receipt": receipt,
        })
    else:
        self.send_json({
            "purchased": False,
            "success": False,
            "transactionStatus": "ApplicationError",
            "productId": user_id_num,
        })
    return True


@server_path('/marketplace/purchase', commands={'POST'})
def _(self: web_server_handler) -> bool:
    form_content = str(self.read_content(), encoding='utf-8')
    form_data = dict(urllib.parse.parse_qsl(form_content))
    gamepass_id = int(form_data['productId'])

    # TODO: actually make gamepass sales secure.
    user_id_num = json.loads(self.headers['Roblox-Session-Id'])['UserId']

    if purchase_gamepass(self, user_id_num, gamepass_id):
        self.send_json({"success": True, "status": "Purchased"})
    else:
        self.send_json({"status": "error", "error": "Unable to purchase"})
    return True


@server_path('/marketplace/game-pass-product-info', commands={'GET'})
def _(self: web_server_handler) -> bool:
    '''
    https://github.com/InnitGroup/syntaxsource/blob/71ca82651707ad88fb717f3cc5e106ff62ac3013/syntaxwebsite/app/routes/marketplace.py#L21
    '''
    gamepass_id = int(self.query['gamePassId'])
    gamepasses = self.game_config.remote_data.gamepasses
    gamepass = gamepasses.get(gamepass_id)
    if gamepass is None:
        self.send_error(404)
        return True

    self.send_json({
        "AssetId": gamepass.id_num,
        "ProductId": gamepass.id_num,
        "Name": gamepass.name,
        "Description": gamepass.name,
        "AssetTypeId": "GamePass",
        "Creator": {
            "Id": 1,
            "Name": "",
            "CreatorType": "Group",
        },
        "IconImageAssetId": 0,
        "Created": 0,
        "Updated": 0,
        "PriceInRobux": gamepass.price,
        "PriceInTickets": 0,
        "Sales": 0,
        "IsNew": False,
        "IsForSale": True,
        "IsPublicDomain": False,
        "IsLimited": False,
        "IsLimitedUnique": False,
        "Remaining": False,
        "MinimumMembershipLevel": 0,
        "ContentRatingTypeId": 0,
    })
    return True


@server_path(r'/v1/users/(\d+)/items/gamepass/(\d+)', regex=True, commands={'GET'})
def _(self: web_server_handler, match: re.Match[str]) -> bool:
    '''
    https://github.com/SushiDesigner/Meteor-back/blob/dc561b5af196ca9c375530d30d593fc8d7f0486c/routes/marketplace.js#L129
    '''
    user_iden = int(match.group(1))
    gamepass_iden = int(match.group(2))
    gamepasses = self.game_config.remote_data.gamepasses

    gamepass_data = []
    has_gamepass = self.server.storage.gamepasses.check(
        user_iden,
        gamepass_iden,
    )

    if has_gamepass is not None:
        gamepass = gamepasses.get(gamepass_iden)
        assert gamepass is not None
        gamepass_data = [
            {
                "type": "Gamepass",
                "id": gamepass_iden,
                "name": gamepass.name,
                "instanceId": None,
            }
        ]

    self.send_json({
        "previousPageCursor": None,
        "nextPageCursor": None,
        "data": gamepass_data,
    })
    return True


@server_path('/gametransactions/getpendingtransactions/', commands={'GET'})
def _(self: web_server_handler) -> bool:
    '''
    Something to do with developer products.
    https://github.com/InnitGroup/syntaxsource/blob/71ca82651707ad88fb717f3cc5e106ff62ac3013/syntaxwebsite/app/routes/gametransactions.py#L26
    '''
    receipt_dict = []
    for (user_id_num, devproduct_id, receipt) in self.server.storage.devproducts.receipts():
        receipt_dict.append({
            "playerId": user_id_num,
            "placeId": util.const.PLACE_IDEN_CONST,
            "receipt": receipt,
            "actionArgs": [
                {
                    "Key": "productId",
                    "Value": devproduct_id,
                },
                {
                    "Key": "currencyTypeId",
                    "Value": 1,
                },
                {
                    "Key": "unitPrice",
                    "Value": 0,
                }
            ]
        })

    self.send_json(receipt_dict)
    return True


@server_path('/marketplace/submitpurchase', commands={'POST'})
def _(self: web_server_handler) -> bool:
    '''
    https://github.com/alainbacu27/RbxJs2016/blob/7b55c6c1b5f820b60e796ceadaacf2b808df26c2/controllers/api.js#L93
    '''
    form_content = str(self.read_content(), encoding='utf-8')
    form_data = dict(urllib.parse.parse_qsl(form_content))
    devproduct_id = int(form_data['productId'])

    # TODO: actually make gamepass sales secure.
    user_id_num = json.loads(self.headers['Roblox-Session-Id'])['UserId']

    receipt = purchase_devproduct(self, user_id_num, devproduct_id)
    if receipt is not None:
        self.send_json({
            "success": True,
            "status": "Bought",
            "receipt": receipt,
        })
    else:
        self.send_json({
            "success": False,
            "status": "Error",
        })
    return True


@server_path('/marketplace/validatepurchase', commands={'GET'})
def _(self: web_server_handler) -> bool:
    receipt = self.query['receipt'].split('-')
    devproduct_id = int(receipt[0])
    user_id_num = int(receipt[1])
    self.send_json({
        'playerId': user_id_num,
        'placeId': 1,
        'isValid': True,
        'productId': devproduct_id,
    })
    return True


@server_path('/marketplace/productinfo')
def _(self: web_server_handler) -> bool:
    asset_id = int(self.query['assetId'])

    gamepasses = self.game_config.remote_data.gamepasses
    metadata = self.game_config.server_core.metadata
    if asset_id in gamepasses:
        gamepass_data = gamepasses[asset_id]
        self.send_json({
            "PriceInRobux": gamepass_data.price,
            "MinimumMembershipLevel": 0,
            "TargetId": gamepass_data.id_num,
            "AssetId": gamepass_data.id_num,
            "ProductId": gamepass_data.id_num,
            "Name": gamepass_data.name,
            "Description": "",
            "AssetTypeId": "GamePass",
            "IsForSale": True,
            "IsPublicDomain": False,
            'Creator': {
                'Id': 1,
                'Name': metadata.creator_name,
                'CreatorType': 'User',
                'CreatorTargetId': 1
            },
        })
        return True

    # Returns an error if the thing trying to be accessed isn't the place we're in.
    if asset_id != util.const.PLACE_IDEN_CONST:
        self.send_error(404)
        return True

    self.send_json({
        'AssetId': util.const.PLACE_IDEN_CONST,
        'ProductId': 13831621,
        'Name': metadata.title,
        'Description': metadata.description,
        'AssetTypeId': 19,
        'Creator': {
            'Id': 1,
            'Name': metadata.creator_name,
            'CreatorType': 'User',
            'CreatorTargetId': 1
        },
        'IconImageAssetId': 0,
        'Created': 0,
        'Updated': 0,
        'PriceInRobux': 0,
        'PriceInTickets': 0,
        'Sales': 0,
        'IsNew': False,
        'IsForSale': True,
        'IsPublicDomain': False,
        'IsLimited': False,
        'IsLimitedUnique': False,
        'Remaining': None,
        'MinimumMembershipLevel': 0,
        'ContentRatingTypeId': 0,
    })
    return True


@server_path('/productDetails')
@server_path('/marketplace/productDetails')
def _(self: web_server_handler) -> bool:
    '''
    Something to do with developer products.
    https://github.com/essentialsasset/RBLX15/blob/d7c5a76e6c1526e86156410a0b4f024a689920a1/shesnotkewlfgdjkhasdfjhsdf/marketplace/productDetails.php#L4
    '''
    devproduct_id = int(self.query['productId'])
    devproducts = self.game_config.remote_data.devproducts
    devproduct = devproducts.get(devproduct_id)
    if devproduct is None:
        self.send_error(404)
        return True

    self.send_json({
        "TargetId": 1,
        "ProductType": "Developer Product",
        "AssetId": 0,
        "ProductId": devproduct.id_num,
        "Name": devproduct.name,
        "Description": devproduct.name,
        "AssetTypeId": 0,
        "Creator": {
            "Id": 0,
            "Name": None,
            "CreatorType": None,
            "CreatorTargetId": 0
        },
        "IconImageAssetId": 0,
        "Created": "2000-01-01T00:00:00Z",
        "Updated": "2000-01-01T00:00:00Z",
        "PriceInRobux": devproduct.price,
        "PremiumPriceInRobux": devproduct.price,
        "PriceInTickets": devproduct.price,
        "IsNew": False,
        "IsForSale": True,
        "IsPublicDomain": False,
        "IsLimited": False,
        "IsLimitedUnique": False,
        "Remaining": None,
        "Sales": None,
        "MinimumMembershipLevel": 0,
    })
    return True


@server_path('/v1/catalog/items/details')
def _(self: web_server_handler) -> bool:
    try:
        request_items = _parse_catalog_items_request(self)
    except (ValueError, json.JSONDecodeError):
        self.send_response(400)
        self.send_header("Content-type", "application/json")
        self.send_json({
            "errors": [
                {
                    "code": 0,
                    "message": "Invalid catalog items request.",
                }
            ]
        })
        return False

    data = []
    for request_item in request_items:
        if isinstance(request_item, int):
            item_id = request_item
            item_type = "Asset"
        elif isinstance(request_item, dict):
            item_id = request_item.get("id")
            item_type = request_item.get("itemType", "Asset")
        else:
            continue

        if item_id is None:
            continue

        try:
            item_id = int(item_id)
        except (TypeError, ValueError):
            continue

        if item_type not in ("Asset", "asset", 0, None):
            continue

        asset_obj = self.server.storage.asset.resolve_object(item_id)
        if asset_obj is None:
            continue

        supports_head_shapes = asset_obj.asset_type in {
            AssetType.Head,
            AssetType.Face,
        }
        creator_name = _get_creator_name(
            self,
            asset_obj.creator_type,
            asset_obj.creator_id,
        )
        price_status = (
            "Off Sale"
            if not asset_obj.is_for_sale else
            ("Free" if asset_obj.price_robux <= 0 else "On Sale")
        )

        data.append({
            "bundledItems": [],
            "taxonomy": [],
            "itemCreatedUtc": _format_api_datetime(asset_obj.created_at),
            "id": asset_obj.id,
            "itemType": 0,
            "assetType": asset_obj.asset_type.value,
            "bundleType": 0,
            "isRecolorable": False,
            "name": asset_obj.name,
            "description": asset_obj.description,
            "productId": asset_obj.id,
            "itemStatus": (
                []
                if asset_obj.moderation_status == 0 else
                [asset_obj.moderation_status]
            ),
            "itemRestrictions": [],
            "creatorHasVerifiedBadge": False,
            "creatorType": asset_obj.creator_type,
            "creatorTargetId": asset_obj.creator_id,
            "creatorName": creator_name,
            "price": asset_obj.price_robux,
            "lowestPrice": asset_obj.price_robux,
            "lowestResalePrice": (
                asset_obj.price_robux
                if asset_obj.is_limited or asset_obj.is_limited_unique else
                0
            ),
            "priceStatus": price_status,
            "unitsAvailableForConsumption": max(
                0,
                asset_obj.serial_count - asset_obj.sale_count,
            ),
            "favoriteCount": 0,
            "offSaleDeadline": _format_api_datetime(asset_obj.offsale_at),
            "collectibleItemId": (
                str(asset_obj.id)
                if asset_obj.is_limited_unique else
                None
            ),
            "totalQuantity": asset_obj.serial_count,
            "saleLocationType": 0,
            "hasResellers": asset_obj.is_limited or asset_obj.is_limited_unique,
            "isOffSale": not asset_obj.is_for_sale,
            "quantityLimitPerUser": 0,
            "supportsHeadShapes": supports_head_shapes,
            "timedOptions": [],
        })

    self.send_response(200)
    self.send_header("Content-type", "application/json")
    self.send_json({"data": data})
    return True