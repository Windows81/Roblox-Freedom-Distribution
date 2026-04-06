from datetime import datetime
import re

import util.versions as versions
from .._logic import web_server_handler, server_path


def _format_api_datetime(value: str | None) -> str:
    if value is None:
        return "1970-01-01T00:00:00.000Z"

    try:
        return datetime.fromisoformat(value).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    except ValueError:
        pass

    try:
        parsed = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        return parsed.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    except ValueError:
        return value


def _get_badge_definitions(self: web_server_handler):
    game_config = getattr(
        self,
        "game_config",
        getattr(self.server, "game_config", None),
    )
    if game_config is None:
        return {}

    remote_data = getattr(game_config, "remote_data", None)
    if remote_data is None:
        return {}

    badge_definitions = getattr(remote_data, "badges", None)
    if badge_definitions is None:
        return {}
    return badge_definitions


def _get_badge_icon_image_id(badge_definition) -> int:
    icon = getattr(badge_definition, "icon", None)
    if icon is None:
        return 0

    icon_value = getattr(icon, "value", None)
    if isinstance(icon_value, str) and icon_value.isdigit():
        return int(icon_value)
    return 0


def _get_awarding_universe(self: web_server_handler) -> dict[str, int | str]:
    name = "Untitled"
    game_config = getattr(
        self,
        "game_config",
        getattr(self.server, "game_config", None),
    )
    if game_config is not None:
        metadata = getattr(getattr(game_config, "server_core", None), "metadata", None)
        configured_name = getattr(metadata, "title", None)
        if isinstance(configured_name, str) and configured_name:
            name = configured_name

    universe_obj = self.server.storage.universe.check(1)
    if universe_obj is None:
        return {
            "id": 0,
            "name": name,
            "rootPlaceId": 0,
        }

    root_place_id = universe_obj[0]
    place_obj = self.server.storage.place.check_object(root_place_id)
    if place_obj is not None and place_obj.assetObj is not None:
        place_name = getattr(place_obj.assetObj, "name", None)
        if isinstance(place_name, str) and place_name:
            name = place_name

    return {
        "id": 1,
        "name": name,
        "rootPlaceId": root_place_id,
    }


def _build_badge_details(
    self: web_server_handler,
    badge_id: int,
    awarded_timestamp: str,
) -> dict:
    badge_definition = _get_badge_definitions(self).get(badge_id)
    badge_name = getattr(badge_definition, "name", f"Badge {badge_id}")
    icon_image_id = _get_badge_icon_image_id(badge_definition)
    awarded_count, past_day_awarded_count = self.server.storage.badges.get_badge_statistics(badge_id)
    api_timestamp = _format_api_datetime(awarded_timestamp)

    return {
        "id": badge_id,
        "name": badge_name,
        "description": "",
        "displayName": badge_name,
        "displayDescription": "",
        "enabled": True,
        "iconImageId": icon_image_id,
        "displayIconImageId": icon_image_id,
        "created": api_timestamp,
        "updated": api_timestamp,
        "statistics": {
            "pastDayAwardedCount": past_day_awarded_count,
            "awardedCount": awarded_count,
            "winRatePercentage": 0.0,
        },
        "awardingUniverse": _get_awarding_universe(self),
    }


def send_user_badges_v1(
    self: web_server_handler,
    user_id_num: int,
) -> bool:
    try:
        limit = int(self.query.get("limit", "10"))
    except ValueError:
        limit = 10
    if limit > 100 or limit < 1:
        limit = 10

    cursor = self.query.get("cursor")
    try:
        offset = int(cursor) if cursor else 0
    except ValueError:
        self.send_json({
            "errors": [
                {
                    "code": 0,
                    "message": "Invalid cursor.",
                }
            ]
        }, 400)
        return True

    badge_items = self.server.storage.badges.list_for_user(
        user_id_num=user_id_num,
        limit=limit,
        offset=offset,
        descending=self.query.get("sortOrder", "Asc") == "Desc",
    )

    self.send_json({
        "previousPageCursor": (
            str(offset - limit)
            if offset >= limit else
            None
        ),
        "nextPageCursor": (
            str(offset + limit)
            if len(badge_items) >= limit else
            None
        ),
        "data": [
            _build_badge_details(self, badge_item.badge_id, badge_item.timestamp)
            for badge_item in badge_items
        ],
    })
    return True


@server_path(r'/v1/users/(\d+)/badges', regex=True, commands={'GET'})
def _(self: web_server_handler, match: re.Match[str]) -> bool:
    return send_user_badges_v1(self, int(match.group(1)))

@server_path(r'/v1/users/(\d+)/roblox-badges', regex=True)
def _(self: web_server_handler, match: re.Match[str]) -> bool:
    self.send_json({
        "previousPageCursor": None,
        "nextPageCursor": None,
        "data": []
    }, 200)
    return True

@server_path(r'/v1/users/(\d+)/badges/awarded-dates', regex=True, commands={'GET'}, versions={versions.rōblox.v463})
def _(self: web_server_handler, match: re.Match[str]) -> bool:
    '''
    TODO: properly award badges.
    https://github.com/MightyPart/openblox/blob/bde5bd486153cfb47990a8e00f63ce4b6bfa8e34/src/apis/classic/badges/badges.types.ts#L61
    '''

    user_id_num = int(match.group(1))
    badge_ids = self.query_lists.get('badgeIds', [])
    database = self.server.storage.badges

    results = []
    for badge_id in badge_ids:
        date_str = database.check(user_id_num, int(badge_id))
        if date_str is None:
            continue
        results.append({
            'badgeId': int(badge_id),
            'awardedDate': date_str,
        })

    self.send_json({'data': results})
    return True
