from web_server._logic import web_server_handler, server_path
import urllib.parse
import itertools
import json


@server_path('/persistence/set')  # Usually expects POST.
def _(self: web_server_handler) -> bool:
    '''
    https://github.com/InnitGroup/syntaxsource/blob/71ca82651707ad88fb717f3cc5e106ff62ac3013/syntaxwebsite/app/routes/datastoreservice.py#L92
    '''
    form_content = str(self.read_content(), encoding='utf-8')
    form_data = dict(urllib.parse.parse_qsl(form_content))
    database = self.server.storage.persistence

    # TODO: implement sorted data stores.
    data_type = self.query.get('type')

    scope = self.query.get('scope', 'global')
    target = self.query['target']
    key = self.query['key']

    value_str = form_data.get('value', 'null')
    value = json.loads(value_str)

    database.set(scope, target, key, value)
    self.send_json({"data": value})
    return True


@server_path('/persistence/getv2')  # Usually expects POST.
@server_path('/persistence/getV2')  # Usually expects POST.
def _(self: web_server_handler) -> bool:
    '''
    https://github.com/InnitGroup/syntaxsource/blob/71ca82651707ad88fb717f3cc5e106ff62ac3013/syntaxwebsite/app/routes/datastoreservice.py#L162
    '''
    form_content = str(self.read_content(), encoding='utf-8')
    form_data = dict(urllib.parse.parse_qsl(form_content))
    database = self.server.storage.persistence

    return_data = []
    for starting_count in itertools.count(0):
        prefix = "qkeys[%d]" % starting_count
        scope = form_data.get(
            f"{prefix}.scope",
            'global',
        )

        target = form_data.get(
            f"{prefix}.target",
            None,
        )
        if target is None:
            break

        key = form_data.get(
            f"{prefix}.key",
            None,
        )
        if key is None:
            break

        value = database.get(scope, target, key)
        return_data.append({
            "Value": json.dumps(value),
            "Scope": scope,
            "Key": key,
            "Target": target,
        })

    # TODO: implement sorted data stores.
    data_type = self.query.get('type')

    if starting_count == 0:
        self.send_json({"data": [], "message": "No data being requested"})
        return True

    self.send_json({"data": return_data})
    return True


@server_path('/persistence/getSortedValues')  # Expecting POST.
def _(self: web_server_handler) -> bool:
    """
    Handles retrieval of sorted data from the persistence storage with pagination.
    """
    # Parse query parameters
    place_iden = int(self.query.get("placeId", 0))
    data_type = self.query.get("type", None)
    scope = self.query.get("scope", "global")
    page_size = int(self.query.get("pageSize", 50))
    exclusive_start_key = int(self.query.get("exclusiveStartKey", 1))
    key = self.query.get("key", '')
    ascending = self.query.get("ascending") == "True"

    inclusive_min_str = self.query.get("inclusiveMinValue")
    if inclusive_min_str is not None:
        inclusive_min_value = int(inclusive_min_str)
    else:
        inclusive_min_value = None

    exclusive_max_str = self.query.get("exclusiveMaxValue")
    if exclusive_max_str is not None:
        exclusive_max_value = int(exclusive_max_str)
    else:
        exclusive_max_value = None

    # Validate inputs
    if place_iden is None:
        self.send_json({"data": [], "message": "Place ID is required"})
        return True

    if page_size <= 0 or page_size > 100:
        self.send_json(
            {"data": [], "message": "Page size must be between 1 and 100"})
        return True

    if data_type != "sorted":
        self.send_json({"data": [], "message": "Invalid data type"})
        return True

    if exclusive_start_key < 1:
        self.send_json({"data": [], "message": "Invalid exclusive start key"})
        return True

    # Simulated database query (replace with actual implementation)
    # Assuming persistence supports sorted data
    database = self.server.storage.persistence
    sorted_data = database.query_sorted_data(
        place_id=place_iden,
        scope=scope,
        key=key,
        ascending=ascending,
        min_value=inclusive_min_value,
        max_value=exclusive_max_value,
        start=exclusive_start_key,
        size=page_size
    )

    if not sorted_data:
        self.send_json({"data": {"Entries": [], "ExclusiveStartKey": None}})
        return True

    # Prepare response
    entries = [{"Target": entry["name"], "Value": entry["value"]}
               for entry in sorted_data["items"]]
    next_key = sorted_data["next_key"] if sorted_data["has_next"] else None

    self.send_json({"data": {
        "Entries": entries,
        "ExclusiveStartKey": next_key
    }})
    return True
