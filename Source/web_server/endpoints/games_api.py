from datetime import datetime

from web_server._logic import web_server_handler, server_path
import util.versions as versions


def _format_api_datetime(value: str) -> str:
    try:
        return datetime.fromisoformat(value).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    except ValueError:
        return value

@server_path(r'/alerts/alert-info', commands={'GET'})
def _(self: web_server_handler) -> bool:
    self.send_response(200)
    self.send_header("Content-Type", "application/json")
    self.send_json({"IsVisible": True, "Text": "RFD btw.", "LinkText": "", "LinkUrl": ""})
    return True

@server_path(r'/v1/games/list', commands={'GET'})
def _(self: web_server_handler) -> bool:
    sort_token = self.query.get("sort_token") or "MostPopular"
    try:
        start_rows = int(self.query.get("startRows") or 0)
        max_rows = int(self.query.get("maxRows") or 40)
    except ValueError:
        self.send_response(400)
        self.send_header("Content-Type", "application/json")
        self.send_json({"errors": [{"code": 0, "message": "Invalid pagination arguments."}]})
        return False

    if sort_token not in ["MostPopular", "Featured", "RecentlyUpdated"]:
        self.send_response(400)
        self.send_header("Content-Type", "application/json")
        self.send_json({"errors": [{"code": 0, "message": "Invalid sort token."}]})
        return False
    if start_rows < 0:
        self.send_response(400)
        self.send_header("Content-Type", "application/json")
        self.send_json({"errors": [{"code": 0, "message": "Invalid start rows."}]})
        return False
    if max_rows > 100 or max_rows < 0:
        self.send_response(400)
        self.send_header("Content-Type", "application/json")
        self.send_json({"errors": [{"code": 0, "message": "Max rows must be between 0-40"}]})
        return False

    universe_page = self.server.storage.universe.list_for_games_api(
        sort_token=sort_token,
        start_rows=start_rows,
        max_rows=max_rows,
    )

    game_list = []
    storage = self.server.storage
    for universe_obj in universe_page.items:
        place_obj = storage.place.check_object(universe_obj.root_place_id)
        if place_obj is None or place_obj.assetObj is None:
            continue

        asset_obj = place_obj.assetObj
        creator_type = "User" if universe_obj.creator_type == 0 else "Group"
        creator_name = str(universe_obj.creator_id)
        # upvotes, downvotes = GetAssetLikesAndDislikes(PlaceObj.placeid)

        if creator_type == "User":
            username = storage.players.get_player_field_from_index(
                index=storage.players.player_field.IDEN_NUM,
                value=universe_obj.creator_id,
                field=storage.players.player_field.USERNAME,
            )
            if isinstance(username, str):
                creator_name = username

        game_list.append({
            "creatorId": universe_obj.creator_id,
            "creatorName": creator_name,
            "creatorType": creator_type,
            "creatorHasVerifiedBadge": False,
            "totalUpVotes": 0,#Upvotes,
            "totalDownVotes": 0,#Downvotes,
            "universeId": universe_obj.universe_id,
            "name": asset_obj.name,
            "placeId": place_obj.placeid,
            "playerCount": 0, #placeinfo.GetUniversePlayingCount(UniverseObj),
            "imageToken": "",
            "isSponsored": False,
            "nativeAdData": "",
            "isShowSponsoredLabel": False,
            "price": 0,
            "analyticsIdentifier": "",
            "gameDescription": asset_obj.description,
            "genre": "All",
            "minimumAge": 0
        })

    self.send_response(200)
    self.send_header("Content-Type", "application/json")
    self.send_json({
        "games": game_list,
        "suggestedKeyword": "",
        "correctedKeyword": "",
        "filteredKeyword": "",
        "hasMoreRows": universe_page.has_next,
        "nextPageExclusiveStartId": (
            start_rows + max_rows
            if universe_page.has_next else
            0
        ),
        "featuredSearchUniverseId": 0,
        "emphasis": False,
        "cutOffIndex": 0,
        "algorithm": "",
        "algorithmQueryType": "",
        "suggestionAlgorithm": "",
        "relatedGames": []
    })
    return True

@server_path(r'/v1/games/sorts', commands={'GET'})
def _(self: web_server_handler) -> bool:
    self.send_response(200)
    self.send_header("Content-Type", "application/json")
    self.send_json({
        "sorts" : [
            {
                "token": "MostPopular",
                "name": "most_popular",
                "displayName": "Popular",
                "gameSetTypeId": 1,
                "gameSetTargetId": 90,
                "timeOptionsAvailable": False,
                "genreOptionsAvailable": False,
                "numberOfRows": 2,
                "numberOfGames": 0,
                "isDefaultSort": True,
                "contextUniverseId": None,
                "contextCountryRegionId": 1,
                "tokenExpiryInSeconds": 3600
            },
            {
                "token": "Featured",
                "name": "featured",
                "displayName": "Featured",
                "gameSetTypeId": 2,
                "gameSetTargetId": 91,
                "timeOptionsAvailable": False,
                "genreOptionsAvailable": False,
                "numberOfRows": 1,
                "numberOfGames": 0,
                "isDefaultSort": True,
                "contextUniverseId": None,
                "contextCountryRegionId": 1,
                "tokenExpiryInSeconds": 3600
            },
            {
                "token": "RecentlyUpdated",
                "name": "recently_updated",
                "displayName": "Recently Updated",
                "gameSetTypeId": 3,
                "gameSetTargetId": 93,
                "timeOptionsAvailable": False,
                "genreOptionsAvailable": False,
                "numberOfRows": 1,
                "numberOfGames": 0,
                "isDefaultSort": True,
                "contextUniverseId": None,
                "contextCountryRegionId": 1,
                "tokenExpiryInSeconds": 3600
            },
        ],
        "timeFilters": [
            {
                "token": "Now",
                "name": "Now",
                "tokenExpiryInSeconds": 3600
            },
            {
                "token": "PastDay",
                "name": "PastDay",
                "tokenExpiryInSeconds": 3600
            },
            {
                "token": "PastWeek",
                "name": "PastWeek",
                "tokenExpiryInSeconds": 3600
            },
            {
                "token": "PastMonth",
                "name": "PastMonth",
                "tokenExpiryInSeconds": 3600
            },
            {
                "token": "AllTime",
                "name": "AllTime",
                "tokenExpiryInSeconds": 3600
            }
        ],
        "genreFilters": [
            {
            "token": "T638364961735517991_1_89de",
            "name": "All",
            "tokenExpiryInSeconds": 3600
            },
            {
            "token": "T638364961735518009_19_3d2",
            "name": "Building",
            "tokenExpiryInSeconds": 3600
            },
            {
            "token": "T638364961735518045_11_3de6",
            "name": "Horror",
            "tokenExpiryInSeconds": 3600
            },
            {
            "token": "T638364961735518062_7_558c",
            "name": "Town and City",
            "tokenExpiryInSeconds": 3600
            },
            {
            "token": "T638364961735518076_17_c371",
            "name": "Military",
            "tokenExpiryInSeconds": 3600
            },
            {
            "token": "T638364961735518094_15_2056",
            "name": "Comedy",
            "tokenExpiryInSeconds": 3600
            },
            {
            "token": "T638364961735518107_8_6d4f",
            "name": "Medieval",
            "tokenExpiryInSeconds": 3600
            },
            {
            "token": "T638364961735518120_13_c168",
            "name": "Adventure",
            "tokenExpiryInSeconds": 3600
            },
            {
            "token": "T638364961735518134_9_e6aa",
            "name": "Sci-Fi",
            "tokenExpiryInSeconds": 3600
            },
            {
            "token": "T638364961735518156_12_13fb",
            "name": "Naval",
            "tokenExpiryInSeconds": 3600
            },
            {
            "token": "T638364961735518169_20_46a",
            "name": "FPS",
            "tokenExpiryInSeconds": 3600
            },
            {
            "token": "T638364961735518183_21_4bbf",
            "name": "RPG",
            "tokenExpiryInSeconds": 3600
            },
            {
            "token": "T638364961735518192_14_efc6",
            "name": "Sports",
            "tokenExpiryInSeconds": 3600
            },
            {
            "token": "T638364961735518205_10_fa83",
            "name": "Fighting",
            "tokenExpiryInSeconds": 3600
            },
            {
            "token": "T638364961735518223_16_5d38",
            "name": "Western",
            "tokenExpiryInSeconds": 3600
            }
        ],
        "gameFilters": [
            {
            "token": "T638364961735518263_Any_56d2",
            "name": "Any",
            "tokenExpiryInSeconds": 3600
            },
            {
            "token": "T638364961735518277_Classic_a1f4",
            "name": "Classic",
            "tokenExpiryInSeconds": 3600
            }
        ],
        "pageContext": {
            "pageId": "f5b1510e-3810-42ab-8135-8ffa5ef221ba",
            "isSeeAllPage": None
        },
        "gameSortStyle": None
    })
    return True