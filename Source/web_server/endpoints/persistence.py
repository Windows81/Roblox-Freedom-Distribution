# Standard library imports
import itertools
import urllib.parse

import json

# Local application imports
from web_server._logic import web_server_handler, server_path



@server_path('/persistence/set')  # Usually expects POST.
def _(self: web_server_handler) -> bool:
    '''
    https://github.com/InnitGroup/syntaxsource/blob/71ca82651707ad88fb717f3cc5e106ff62ac3013/syntaxwebsite/app/routes/datastoreservice.py#L92
    '''
    form_content = str(self.read_content(), encoding='utf-8')
    form_data = dict(urllib.parse.parse_qsl(form_content))
    database = self.server.storage.persistence

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
    starting_count = 0
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
    data_type = self.query.get("type", None)
    scope = self.query.get("scope", "global")
    key = self.query['key']

    exclusive_start_key = int(self.query.get("exclusiveStartKey", 1))
    is_ascending = self.query.get("ascending") == "True"
    page_size = int(self.query.get("pageSize", 50))

    inclusive_min_str = self.query.get("inclusiveMinValue")
    inclusive_min_value = (
        int(inclusive_min_str)
        if inclusive_min_str is not None
        else None
    )

    exclusive_max_str = self.query.get("exclusiveMaxValue")
    exclusive_max_value = (
        int(exclusive_max_str)
        if exclusive_max_str is not None
        else None
    )

    if data_type != "sorted":
        self.send_json({"data": [], "message": "Invalid data type"})
        return True

    if exclusive_start_key < 1:
        self.send_json({"data": [], "message": "Invalid exclusive start key"})
        return True

    # Assuming persistence supports sorted data.
    database = self.server.storage.persistence
    sorted_data = database.query_sorted_data(
        scope=scope,
        key=key,
        ascending=is_ascending,
        min_value=inclusive_min_value,
        max_value=exclusive_max_value,
        start=exclusive_start_key,
        size=page_size
    )

    if not sorted_data:
        self.send_json({
            "data": {
                "Entries": [],
                "ExclusiveStartKey": None,
            }
        })
        return True

    entries = [
        {
            "Target": entry.name,
            "Value": entry.value,
        }
        for entry in sorted_data.items
    ]

    self.send_json({
        "data": {
            "Entries": entries,
            "ExclusiveStartKey": sorted_data.next_key,
        }
    })
    return True


@server_path('/persistence/increment')  # Usually expects POST.
def _(self: web_server_handler) -> bool:
    """
    Handles incrementing numeric values in the persistence storage.
    Supports both standard and sorted data types.
    """
    database = self.server.storage.persistence

    scope = self.query.get('scope', 'global')
    target = self.query['target']
    key = self.query['key']
    data_type = self.query['type']

    try:
        increment_value = int(self.query.get('value', 1))
    except (TypeError, ValueError):
        self.send_json({"data": [], "message": "Increment must be an integer"})
        return True

    if not all([target, key]):
        self.send_json({"data": [], "message": "Missing required parameters"})
        return True

    # Get current value
    current_value = database.get(scope, target, key)

    try:
        if current_value is None:
            new_value = increment_value
        else:
            if isinstance(current_value, str):
                current_value = int(current_value)
            new_value = current_value + increment_value
    except (TypeError, ValueError):
        self.send_json(
            {"data": [], "message": "Current value is not an integer"})
        return True

    if data_type != "sorted":
        new_value = str(new_value)

    # Stores the new value.
    database.set(scope, target, key, new_value)

    self.send_json({"data": new_value})
    return True
