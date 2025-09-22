# Standard library imports
import urllib.parse
import json
import re

# Local application imports
from web_server._logic import web_server_handler, server_path
import util.const


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


def purchase_dev_product(self: web_server_handler, user_id_num: int, dev_product_id: int) -> str | None:
    dev_product = self.game_config.remote_data.dev_products.get(dev_product_id)

    if dev_product is None:
        return  # Gamepass does not exist

    storage = self.server.storage
    funds = storage.funds.check(user_id_num)
    if funds is None:
        return  # Couldn't load funds

    if funds < dev_product.price:
        return  # Too poor!

    storage.dev_products.update(user_id_num, dev_product_id)
    storage.funds.add(user_id_num, -1 * dev_product.price)
    return f"{dev_product_id}-{user_id_num}"


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
    dev_product_id = int(match[1])

    # TODO: actually make gamepass sales secure.
    user_id_num = json.loads(self.headers['Roblox-Session-Id'])['UserId']

    receipt = purchase_dev_product(self, user_id_num, dev_product_id)
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
        "PriceInRobux": 0,
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
    for (user_id_num, dev_product_id, receipt) in self.server.storage.dev_products.receipts():
        receipt_dict.append({
            "playerId": user_id_num,
            "placeId": util.const.PLACE_IDEN_CONST,
            "receipt": receipt,
            "actionArgs": [
                {
                    "Key": "productId",
                    "Value": dev_product_id,
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
    dev_product_id = int(form_data['productId'])

    # TODO: actually make gamepass sales secure.
    user_id_num = json.loads(self.headers['Roblox-Session-Id'])['UserId']

    receipt = purchase_dev_product(self, user_id_num, dev_product_id)
    if receipt is not None:
        self.send_json({
            "success": True,
            "status": "Bought",
            "receipt": receipt,
        })
    else:
        self.send_json({
            "purchased": False,
            "reason": "InsufficientFunds",
            "productId": dev_product_id,
            "statusCode": 500,
            "title": "Not Enough Robux",
            "errorMsg": "You do not have enough Robux to purchase this item.",
            "showDivId": "InsufficientFundsView",
        })
    return True


@server_path('/marketplace/validatepurchase', commands={'GET'})
def _(self: web_server_handler) -> bool:
    receipt = self.query['receipt'].split('-')
    dev_product_id = int(receipt[0])
    user_id_num = int(receipt[1])
    self.send_json({
        'playerId': user_id_num,
        'placeId': 1,
        'isValid': True,
        'productId': dev_product_id,
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
    dev_product_id = int(self.query['productId'])
    dev_products = self.game_config.remote_data.dev_products
    dev_product = dev_products.get(dev_product_id)
    if dev_product is None:
        self.send_error(404)
        return True

    self.send_json({
        "TargetId": 1,
        "ProductType": "Developer Product",
        "AssetId": 0,
        "ProductId": dev_product.id_num,
        "Name": dev_product.name,
        "Description": dev_product.name,
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
        "PriceInRobux": dev_product.price,
        "PremiumPriceInRobux": dev_product.price,
        "PriceInTickets": dev_product.price,
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
