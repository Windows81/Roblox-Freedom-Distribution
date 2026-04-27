# 0.66.2

- feat: support for modern _CSGPHS8_ physics meshes
- fix: default remote resource `rbxmtl-studs.dds` not loading
- fix: properly repaired `--clear_temp_cache` command flag
- build: `zstandard` and `dracopy` now come installed in future releases

# 0.66.{0,1}

- feat!: changed method signatures of `server_core.check_user_allowed` and `server_core.retrieve_default_user_code`
- feat: add GameConfig option `server_core.retrieve_membership_type(id_num, user_code)`
- feat: add `/Game/Badge/HasBadge.ashx` and `/assets/award-badge` endpoints
- feat: support for modern _CSGMDL5_ unions
- fix: disable SSL certificate verification to work around PyInstaller incompatiblity #160
- fix: route `/Asset` and `/Asset/` to existing `/v1/asset`
- fix: persistence `target` not existing on route `/persistence/set`
- fix: repaired `--clear_temp_cache` command flag
- fix: `/marketplace/productinfo` to support all-lowercase `assetid` query param
- fix: route `/Login/Negotiate.ashx` to already-existing `/login/negotiate.ashx`
- build: update link to `sqlite-worker` dependency
- test: add unit test for CSGMDL2's hashing algorithm
- test: add unit test to convert CSGMDL5 to CSGMDL2 format

# 0.65.0

- [feat!](https://github.com/Windows81/Roblox-Freedom-Distribution/discussions/139): moved `./Roblox/v348` to `./Roblox/v347`
- [feat!](https://github.com/Windows81/Roblox-Freedom-Distribution/discussions/130): to address DataStore2 behaviour, ordered data stores no longer collide with unordered data stores of the same name
