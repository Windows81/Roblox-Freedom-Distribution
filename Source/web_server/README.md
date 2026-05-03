# Web Server (`web_server/`)

#### Note: This README file has been generated using Deepseek v4. Certain explanations might be wrong. Will correct over time.

The web server module provides an HTTP(S) server that emulates Rōblox web APIs, allowing the RFD client and RCC (Rōblox Cloud Compute) to function without connecting to Rōblox's official servers.

## Architecture

```
web_server/
├── __init__.py          # Package entry; exposes make_server()
├── _logic.py            # Core server, handler, and routing infrastructure
├── endpoints/
│   ├── __init__.py      # Imports all endpoints; serves root "/"
│   ├── assets.py        # Asset and thumbnail delivery
│   ├── avatar.py        # Character appearance data
│   ├── badges.py        # Badge awarding and checking
│   ├── data_transfer.py # RCC ↔ server data exchange
│   ├── funds.py         # Player currency balance
│   ├── groups.py        # Group rank retrieval
│   ├── join_data.py     # Player join/registration flow
│   ├── marketplace.py   # Gamepass and developer product purchases
│   ├── persistence.py   # DataStore (set, get, increment, sorted)
│   ├── player_info.py   # Player lookup by name/ID
│   ├── save_place.py    # game:SavePlace() support
│   ├── setup_player.py  # Player configuration and settings endpoints
│   ├── setup_rcc.py     # RCC configuration (MD5 hashes, versions, policies)
│   ├── studio.py        # Studio login and user endpoints
│   └── text_filter.py   # Chat filtering/moderation
└── README.md
```

## Core (`_logic.py`)

The foundation of the web server. Key components:

- **`server_path()` decorator** — Registers handler functions into the global `SERVER_FUNCS` routing table. Supports static path matching, regex path matching, version-specific routes, and HTTP method filtering (GET, POST, etc.).
- **`web_server`** — Extends `http.server.ThreadingHTTPServer`. Accepts `port`, `is_ipv6`, `game_config`, `server_mode`, and `log_filter`. Holds references to game storage, data transferer, and logger.
- **`web_server_ssl`** — Extends `web_server` with TLS support. Generates a self-signed certificate via the `trustme` library.
- **`web_server_handler`** — Extends `BaseHTTPRequestHandler`. Handles GET, POST, HEAD, PATCH, and DELETE. Parses the Host header, query string, and request body. Routes requests by matching against `SERVER_FUNCS` using static path lookup then regex fallback. Provides helpers: `send_json()`, `send_data()`, `send_redirect()`.

## Endpoints

### `__init__.py`
Serves the root `/` path with server version and Rōblox version info: `"Rōblox Freedom Distribution webserver <version> [<rōblox_version>]"`.

### `assets.py`
- `/asset`, `/Asset`, `/v1/asset`, etc. — Fetches assets and thumbnails from the asset cache. Returns the asset data, a redirect, or a 404. Blocks access to the place file (`PLACE_IDEN_CONST`) unless the request is privileged (from localhost).
- `/ownership/hasasset` — Always returns `true` (collective ownership — no catalogue API planned).
- `/Game/Tools/ThumbnailAsset.ashx`, `/Thumbs/Asset.ashx` — Fetches asset thumbnails via cache.

### `avatar.py`
Returns player character appearance data. Two version-specific implementations:
- **v347**: `/v1.1/avatar-fetch/` — Animations, accessory versions, body colors, scales.
- **v463**: `/v1/avatar`, `/v1/avatar-fetch` — Asset+type IDs, animation asset IDs, body colors, scales, emotes.
- `/v1.1/game-start-info` — Returns universe avatar configuration (scales, collision type, body type).

### `badges.py`
- `/Game/Badge/HasBadge.ashx` (v347) — Checks if a user owns a badge.
- `/assets/award-badge` — Awards a badge to a player.
- `/v1/users/{id}/badges/awarded-dates` (v463) — Returns awarded badge dates.

### `data_transfer.py`
- `/rfd/data-transfer` — Privileged-only (localhost) endpoint. Accepts a JSON dict via POST, inserts it into the data transfer buffer, and returns accumulated output. Used for RCC ↔ server communication.

### `funds.py`
- `/currency/balance` — Returns the player's robux and ticket balance.

### `groups.py`
- `/Game/LuaWebService/HandleSocialRequest.ashx` (v347) — Handles `GetGroupRank` method, returning the player's rank in a group.
- `/v2/users/{id}/groups/roles` (v463) — Returns all groups and roles for a player.

### `join_data.py`
Handles the player join and registration flow:
- `gen_player()` / `init_player()` — Creates or retrieves a player entry in the database. Initializes default funds on first join.
- `perform_and_send_join()` — Constructs the join-data JSON (server connection, user info, session ID, etc.) and sends it.
- `/game/join.ashx` (v347, v463) — Main join endpoint. Returns version-specific join data with appropriate `--rbxsig` prefix.
- `/game/PlaceLauncher.ashx` — Returns join script URL and authentication ticket.
- `/login/negotiate.ashx` — Always returns `true` (authentication passthrough).
- `/universes/validate-place-join` — Always returns `true`.

### `marketplace.py`
Full marketplace implementation:
- `purchase_gamepass()` / `purchase_devproduct()` — Deducts funds and records ownership.
- `/Game/GamePass/GamePassHandler.ashx` — Checks gamepass ownership.
- `/v1/purchases/products/{id}` — Purchases a gamepass.
- `/v2/developer-products/{id}/purchase` — Purchases a developer product.
- `/marketplace/purchase`, `/marketplace/submitpurchase` — Alternate purchase endpoints.
- `/marketplace/game-pass-product-info` — Returns gamepass details.
- `/marketplace/productinfo`, `/productDetails` — Returns product/developer product details.
- `/gametransactions/getpendingtransactions` — Returns pending transaction receipts.
- `/marketplace/validatepurchase` — Validates purchase receipts.

### `persistence.py`
DataStore API implementation:
- `/persistence/set` — Stores a key-value pair with scope, target, and type.
- `/persistence/getv2` — Retrieves multiple key-value pairs in bulk.
- `/persistence/getSortedValues` — Retrieves sorted paginated data with min/max filtering.
- `/persistence/increment` — Atomically increments numeric values.

### `player_info.py`
- `/users/{id}` — Returns username for a given user ID.
- `/users/get-by-username` — Returns user ID for a given username.
- `/v1/users/{id}/friends` (v463) — Returns empty friend list (dummy).
- `/points/get-point-balance` — Returns zero point balance.

### `save_place.py`
- `/v1/places/{id}/symbolic-links` — Returns empty package list (packages not used in RFD).
- `/ide/publish/UploadExistingAsset` — Saves the place file from Studio's `game:SavePlace()`. Creates a `.bak` backup before overwriting. Only works for local place files, not online URIs. Privileged-only.

### `setup_player.py`
Miscellaneous player/client configuration endpoints:
- `/rfd/default-user-code` — Returns the default user code string.
- `/rfd/is-player-allowed` — Checks if a user is allowed to join.
- `/rfd/rōblox-version` — Returns the configured Rōblox version name.
- `/game/validate-machine` — Always returns success.
- `/Setting/QuietGet/StudioAppSettings/`, `ClientAppSettings/` — Returns empty settings (all defaults).
- `/avatar-thumbnail/json`, `/avatar-thumbnail/image` — Returns empty/does nothing.
- `/asset-thumbnail/json` — Returns game icon thumbnail URL.
- `/Thumbs/GameIcon.ashx` — Serves the game icon from cache.
- `/v1/settings/application` — Returns empty application settings.
- `/v1/player-policies-client` — Returns player policy flags (ads allowed, trading allowed, etc.).
- `/users/{id}/canmanage/{id}` — Checks if a user has admin rights (via `server_core`).
- `/v1/user/{id}/is-admin-developer-console-enabled` — Checks admin console access.

### `setup_rcc.py`
RCC (Rōblox Cloud Compute) configuration endpoints:
- `/api.GetAllowedMD5Hashes/` — Returns a hardcoded list of allowed MD5 hashes.
- `/api.GetAllowedSecurityVersions/` — Returns allowed security versions (v347: `0.348.0pcplayer`, v463: `0.463.0pcplayer`).
- `/game/load-place-info` — Returns place metadata (creator, version, game ID).
- `/v1.1/Counters/BatchIncrement`, `/v1.0/SequenceStatistics/BatchAddToSequencesV2` — No-op, returns empty JSON.
- `/universal-app-configuration/v1/behaviors/app-patch/content` — Returns canary/rollout config.
- `/universal-app-configuration/v1/behaviors/app-policy/content` — Returns app feature flags (chat, game details, catalog, etc.).
- `/v1/autolocalization/games/{id}/autolocalizationtable` — Returns localization disabled.

### `studio.py`
Rōblox Studio-specific endpoints:
- `/studio/e.png` — Returns empty bytes (tracking pixel).
- `/login/RequestAuth.ashx` — Redirects to negotiate endpoint.
- `/v2/login` — Mock login. Accepts any password without `1`; rejects passwords containing `1` (debugging aid).
- `/Users/1630228`, `/game/GetCurrentUser.ashx` — Returns hardcoded user ID `1630228`. Includes a 2-second sleep for Studio 2021E compatibility.
- `/users/account-info` — Returns user roles, ID, and robux balance.
- `/device/initialize` — Returns zero device identifiers.
- `/v1/users/authenticated` — Returns hardcoded "RŌBLOX" user.
- `/my/settings/json` — Returns empty settings.

### `text_filter.py`
- `/game/players/{id}/`, `/127.0.0.1/game/players/{id}/` — Returns `"ChatFilter": "blacklist"`.
- `/moderation/v2/filtertext` — Passes text through the server core's text filter and returns filtered output.
