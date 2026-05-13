# 0.66.2

- feat(beta): support for modern _CSGPHS8_ physics meshes
- fix: default remote resource `rbxmtl-studs.dds` not loading
- fix: properly repaired `--clear_temp_cache` command flag
- build: `zstandard` and `dracopy` now come installed in this and future releases
- test: add `--clear_temp_cache` by default to most VSCode debug options

# 0.66.{0,1}

- **[fix](https://github.com/Windows81/Roblox-Freedom-Distribution/issues/138): repaired v347 by replacing player's `ClientAppSettings.json`**
- feat!(config): changed method signatures of `server_core.check_user_allowed` and `server_core.retrieve_default_user_code`
- feat(config): add GameConfig option `server_core.retrieve_membership_type(id_num, user_code)`
- feat(webserver): add `/Game/Badge/HasBadge.ashx` and `/assets/award-badge` endpoints
- feat(serialiser): support for modern _CSGMDL5_ unions
- [fix](https://github.com/Windows81/Roblox-Freedom-Distribution/pull/160): disable SSL certificate verification to work around PyInstaller incompatiblity
- [fix](https://github.com/Windows81/Roblox-Freedom-Distribution/issues/151)(persistence): marketplace purchase fail
- fix(webserver): route `/Asset` and `/Asset/` to existing `/v1/asset`
- fix(webserver): persistence `target` not existing on route `/persistence/set`
- fix(webserver): `/marketplace/productinfo` to support all-lowercase `assetid` query param
- fix(webserver): route `/Login/Negotiate.ashx` to already-existing `/login/negotiate.ashx`
- fix(launcher): repaired `--clear_temp_cache` command flag
- build: update link to `sqlite-worker` dependency
- test: add unit test for CSGMDL2's hashing algorithm
- test: add unit test to convert CSGMDL5 to CSGMDL2 format

# 0.65.4

- fix: modify heuristics to activate mesh parser
- docs(guides, beta): add information about interaction with `MessagingService`

# 0.65.3

- docs: show additional important use case for `asset_redirects` parameter
- docs(guides): additional background information for `PatchTLSVerification` and `AdvancedTrustCheck2021E` guides
- docs(guides): add `RCCServiceFFlagsFetchPatch` guide for Rōblox 227; _not_ relevant to core RFD

# 0.65.2

- fix(serialiser): broaden regex pattern for Rōblox asset links
- fix(launcher, server): assign `-p` alias for both web and RCC connection

# 0.65.0

- [feat!](https://github.com/Windows81/Roblox-Freedom-Distribution/discussions/139): moved `./Roblox/v348` to `./Roblox/v347`
- [feat!](https://github.com/Windows81/Roblox-Freedom-Distribution/discussions/130): to address DataStore2 behaviour, ordered data stores no longer collide with unordered data stores of the same name
- feat(launcher): assign `-p` alias for both web and RCC connection
- feat(launcher): support for multiple RFD instances across consecutive TCP/UDP ports
- build: update `pyinstaller` to 6.18.0

# 0.64.4

- docs(guides): additional background information for `PatchTLSVerification` guide
- feat!(launcher): changed flag name `--clear_cache` to `--clear_temp_cache`
