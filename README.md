<h1 align="center"><img src="./Logo.png" height="20px"/> Rōblox: Freedom Distribution <img src="./Logo.png" height="20px"/></h1>

_Want to host your own Rōblox LAN parties? Looking for a way to deploy your Rōblox experiences, new and old, on your own machine?_

Rōblox Freedom Distribution is one such solution. It's a 'revival' launcher built on existing research for self-hosting Rōblox servers.

Using RFD, users can host their own server instances from compiled Rōblox binaries from 2018-07-25 or 2021-01-25.

Players can join existing servers.

Clients only need to keep track of which hosts and ports to connect to. That's because clients will automatically connect to a server of the same version.

**If you worked with Python 3.12+ before, [_initial_ setup](#installation) is supposed to take less than a minute. Why _initial_? Freedom Distribution automatically downloads additional data (at most 90 MiB) for you.**

Initial adaptation from the [Rōblox Filtering Disabled](https://jetray.itch.io/roblox-filtering-disabled) project by Jetray, et al.

All the code is free-as-in-freedom software and is licensed under the GNU GPL v3.

_This README is optimised for viewing on [GitHub](https://github.com/Windows81/Roblox-Freedom-Distribution)._

## Copyright Acknowledgement

My use of Rōblox's binaries are prone to copyright-infringement issues. Be wary of any potential copyright takedowns.

In the event of a DMCA takedown, don't rely on forks of this repo on GitHub. Consider using other means. Also consult this [document](./LEGAL.md) if you want to know why I believe I'm protected under fair-use law.

## Installation

RFD is natively supported on Windows and somewhat works on GNU/Linux systems with `wine`. No plans for native MacOS support so far.

### As an [Executable](https://github.com/Windows81/Roblox-Freedom-Distribution/releases/latest/download/RFD.exe)

This is good for if you want to deploy quickly on any machine _with_ connection to the internet.

#### For Windows

To install _as an executable_, run:

```
mkdir rfd
cd rfd
curl https://github.com/Windows81/Roblox-Freedom-Distribution/releases/latest/download/RFD.exe --output RFD.exe
```

To launch RFD, your command line will look something like this:

```
./RFD.exe player -h 127.0.0.1 -p 2005
```

#### For GNU/Linux

Might not run as well as on Windows.

[Guide 📕](https://github.com/Windows81/Roblox-Freedom-Distribution/blob/main/Guides/Linux/README.MD)

### From [Source](https://github.com/Windows81/Roblox-Freedom-Distribution/archive/refs/heads/main.zip)

This is good for if you already have Python installed on your machine. Do you want to help contribute to RFD? Use this.

You need Python 3.12+ on your system.

To install _from source_, run:

```
git clone --depth 1 https://github.com/Windows81/Roblox-Freedom-Distribution rfd
cd rfd
pip install -r ./Source/requirements.txt
```

To launch RFD, your command line will look something like this:

```
py Source/_main.py player -h 127.0.0.1 -p 2005
```

## Command Syntax

### `server`

Game-specific options are specified in the `--config_path` argument, which defaults to `./GameConfig.toml`.

[**Please review each option in the config file before starting your server up.**](#gameconfigtoml-structure)

| Option                    | Type         | Default             |
| ------------------------- | ------------ | ------------------- |
| `--config_path`, `-cp`    | `int`        | `./GameConfig.toml` |
| `--rcc_port`, `-rp`, `-p` | `int`        | 2005                |
| `--web_port`, `-wp`       | `int`        | 2005                |
| `--run_client`, `-rc`     | `store_true` | N/A                 |
| `--skip_rcc`              | `store_true` | N/A                 |
| `--skip_rcc_popen`        | `store_true` | N/A                 |
| `--skip_web`              | `store_true` | N/A                 |
| `--place_path`, `-pl`     | `str`        | N/A                 |

_This option allows you to specify the path to a Roblox place file (.rbxl) that should be loaded when the server starts._

[**Please review the Roblox documentation for information on how to create and use place files.**](https://developer.roblox.com/en-us/articles/Place-Files)

### `player`

| Option                    | Type  | Default |
| ------------------------- | ----- | ------- |
| `--rcc_host`, `-rh`, `-h` | `str` | None    |
| `--rcc_port`, `-rp`, `-p` | `int` | 2005    |
| `--web_host`, `-wh`       | `str` | N/A     |
| `--web_port`, `-wp`       | `int` | 2005    |
| `--user_code`, `-u`       | `str` | N/A     |

Command syntaxes for `studio` and `download` now include detailed documentation.

## `download`

The `download` command allows you to download specific versions of Rōblox components. Here are the available options:

| Option              | Type   | Default               |
| ------------------- | ------ | --------------------- |
| `--rbx_version, -v` | `str`  | N/A                   |
| `--bin_subtype, -b` | `list` | `Client` and `Server` |

## Network Ports in Use

**To keep it simple: just open port 2005 on both TCP and UDP.**

Anyone can host a server and must leave _both a TCP and UDP network port_ of their choice accessible.

It's possible to connect to a webserver and an RCC server from different hosts. However, I wouldn't recommend it.

### RCC (UDP)

RCC is an acronym for 'Rōblox Cloud Compute', which is the `exe` program we use to run the Rōblox servers. The UDP-based protocol it communicated with built under [RakNet](http://www.raknet.com/).

Host is specified by the `-h` option (also by `--rcc_host` or `-rh`).

Port is specified by the `-p` option (also by `--rcc_port` or `-rp`).

### Webserver (self-signed HTTPS)

The webserver is responsible for facilitating player connections and loading in-game assets.

Host is optionally specified by the `--webserver_host` or `-wh` option, in case RCC is hosted elsewhere.

Port is specified by the `--webserver_port` or `-wp` option.

## Asset Packs

Assets are automatically cached server-side in directory `./AssetCache`. To manually add assets, place the raw data in a file named with the iden number or string _without_ any extension.

The following are examples of asset idens resolving to cache files:

| Asset Iden                    | File Name          | Format |
| ----------------------------- | ------------------ | ------ |
| `rbxassetid://1818`           | `./00000001818`    | `%11d` |
| `rbxassetid://5950704`        | `./00005950704`    | `%11d` |
| `rbxassetid://97646706196482` | `./97646706196482` | `%11d` |
| `rbxassetid://custom-asset`   | `./custom-asset`   | `%s`   |

## Studio?

You can modify `rbxl` file in current-day Studio as of September 2024. For compatibility with older clients, _RFD comes with its own [serialiser suite](./Source/assets/serialisers/)_. Objects transformed include:

1. Fonts which existed in their respective versions,
1. And meshes encoded with versions 4 or 5 _back_ to version 2 (courtesy [rbxmesh](https://github.com/PrintedScript/RBXMesh/blob/main/RBXMesh.py)).

Some modern programs do weird things to client-sided scripts. They use `Script` classs objects, but with a [`RunContext`](https://robloxapi.github.io/ref/class/BaseScript.html#member-RunContext) property set to [`"Client"`](https://robloxapi.github.io/ref/enum/RunContext.html#member-Client). You will also need to _manually_ convert these objects to `LocalScripts`.

And, **union operations done in current-day Studio (CSG v3) are not supported**. This is because CSG v2 support was completely removed in late 2022.

In that case...

[Sodikm](https://archive.org/details/full-sodikm_202308) has a functional Studio build from 2018.

[Rōblox Filtering Disabled](https://beepboopbap.itch.io/filtering-disabled) has a working Studio build from 2022.

You can also use [this 2018M build](https://github.com/Windows81/Roblox-Freedom-Distribution/releases/download/2023-08-31T09%EA%9E%8910Z/v348.Studio.7z) whilst running the Rōblox Filtering Disabled webserver.

If you need any help, please shoot me an issue on GitHub or a message to an account with some form of 'VisualPlugin' elsewhere.

## Examples

Where `...` is [your command-line prefix](#installation),

### Server

```shell
... server -p 2005 --config ./GameConfig.toml
```

```shell
... server -p 2005 --place ./Place.rbxl
```

### Player

```shell
... player -rh 172.88.194.43 -p 2005
```

## `GameConfig.toml` Structure

This specification is current as of 0.53. Some options might be different in future versions.

### Special Types

#### Functions

Function-type options are very flexible in RFD. _Way_ too flexible if you're asking me.

Look out for `{OPTION}_call_mode`, where `{OPTION}` is the name of the option you're modifying. If `{OPTION}_call_mode` is not specified, RFD tries to assume on its own.

Following is a hypothetical option called `skibidi_plugin`. The examples all do the same thing.

##### Lua Mode

```toml
skibidi_plugin_call_mode = "lua"
skibidi_plugin = '''
function(toil_int, daf_qbool)
    if toil_int == 666 then
        return {
            evil = 666,
        }
    elseif daf_qbool == true then
        return {
            owo = 7,
        }
    elseif toil_int == 420 and daf_qbool == false then
        return {
            uwu = 3,
        }
    end
    return {
        camera_man = 1,
        ohio = 2,
    }
end
'''
```

##### Python Mode

```toml
skibidi_plugin_call_mode = "python"
skibidi_plugin = '''
def f(toil_int: int, daf_qbool: bool):
    if toil_int == 666:
        return {
            "evil": 666,
        }
    elif daf_qbool == True:
        return {
            "owo": 7,
        }
    elif toil_int == 420 and daf_qbool == False:
        return {
            "uwu": 3,
        }
    return {
        "camera_man": 1,
        "ohio": 2,
    }
'''
```

Nobody cares what name you give the function. RFD should be smart enough to figure out what you're using.

In Python mode, RFD assigns global constants for your convenience.

| Variable     | Description                      |
| ------------ | -------------------------------- |
| `CONFIG_DIR` | the config file's directory path |

##### Dict Mode

```toml
skibidi_plugin_call_mode = "dict"
skibidi_plugin.666 = {
    "evil": 666,
}
skibidi_plugin.True = {
    "owo": 7,
}
skibidi_plugin.420-False = {
    "uwu": 3,
}
skibidi_plugin.default = {
    "camera_man": 1,
    "ohio": 2,
}
```

Dict keys are access in the following order of precedence:

1. Each of the individual stringified arguments in positional order,
1. The joined string of all arguments with string separators `_`, `,`, then `, `,
1. Then the static key `default`.

### Options

#### `metadata.config_version_wildcard`

Resolves to a wildcard; defaults to `"*"`.

Matches against the `GIT_RELEASE_VERSION` internal constant. Useful for protecting changes in config structure between RFD versions.

#### `server_core.startup_script`

Resolves to type `str`.

Runs at the CoreScript security level whenever a new _server_ is started.

```toml
startup_script = 'game.workspace.FilteringEnabled = false'
```

#### `server_core.metadata.title`

Resolves to type `str`.

Shows up on the loading screen when a player joins the server.

#### `server_core.metadata.description`

Resolves to type `str`.

Shows up on the loading screen when a player joins the server.

#### `server_core.metadata.creator_name`

Resolves to type `str`.

Shows up on the loading screen when a player joins the server.

#### `server_core.metadata.icon_uri`

Resolves to internal type `uri_obj`.

Can resolve to either a relative or absolute local path -- or extracted from a remote URL.

#### `server_core.place_file.rbxl_uri`

Resolves to internal type `uri_obj`. Files must be encoded in the binary `rbxl` format and not in the human-readable `rbxlx` format.

Can resolve to either a relative or absolute local path -- or extracted from a remote URL.

```toml
rbxl_uri = 'c:\Users\USERNAME\Documents\Baseplate.rbxl'
```

```toml
rbxl_uri = 'https://archive.org/download/robloxBR1/RBR1/RBR1.rbxl'
```

#### `server_core.place_file.enable_saveplace`

Resolves to type `bool`; defaults to false.

When `game:SavePlace()` is called and `enable_saveplace` is true, the file at [`rbxl_uri`](#game_setupplace_filerbxl_uri) is overwritten. It won't work if `rbxl_uri` points to a remote resource.

#### `game_setup.roblox_version`

The following are valid version strings.

| `"v348"`  | `"v463"`  |
| --------- | --------- |
| `"2018M"` | `"2021E"` |
| `"2018"`  | `"2021"`  |

All entries on the same column are aliases for the same version.

#### `game_setup.asset_cache.dir_path`

Resolves to type `path_str`. Relative paths are traced from the directory where the config file is placed.

#### `game_setup.asset_cache.clear_on_start`

Resolves to type `bool`; defaults to false.

If true, deletes cache from assets which should redirect so that the config file remains correct.

#### `game_setup.persistence.clear_on_start`

Resolves to type `bool`; defaults to false.

If true, clears [the `sqlite` database](#game_setuppersistencesqlite_path) before starting a new server.

#### `game_setup.persistence.sqlite_path`

Resolves to type `path_str`. Relative paths are traced from the directory where the config file is placed.

#### `server_core.chat_style`

Corresponds to Rōblox [`Enum.ChatStyle`](https://create.roblox.com/docs/reference/engine/enums/ChatStyle). Can either be `"Classic"`, `"Bubble"`, or `"ClassicAndBubble"`.

#### `server_core.retrieve_default_user_code`

Resolves to [function](#functions) type `(float) -> str`.

If the client doesn't include a [`-u` user code](#player) whilst connecting to the server, this function is called. Should be a randomly-generated value.

```toml
retrieve_default_user_code_call_mode = "lua"
retrieve_default_user_code = '''
function(tick) -- float -> str
    return string.format('Player%d', tick)
end
```

#### `server_core.check_user_allowed`

Resolves to [function](#functions) type `(int, str) -> bool`.

```toml
check_user_allowed_call_mode = "lua"
check_user_allowed = '''
function(user_id_num, user_code) -- string -> bool
    return true
end
'''
```

#### `server_core.check_user_has_admin`

Resolves to [function](#functions) type `(int, str) -> bool`.

```toml
check_user_has_admin_call_mode = "lua"
check_user_has_admin = '''
function(user_id_num, user_code) -- string -> bool
    return true
end
'''
```

#### `server_core.retrieve_username`

Resolves to [function](#functions) type `(int, str) -> str`.

Only gets called the first time a new user joins. Otherwise, RFD checks for a cached value in [the `sqlite` database](#game_setuppersistencesqlite_path).

```toml
retrieve_username_call_mode = "lua"
retrieve_username = '''
function(user_id_num, user_code)
    return user_code
end
'''
```

#### `server_core.retrieve_user_id`

Resolves to [function](#functions) type `(str) -> int`.

Only gets called the first time a new user joins. Otherwise, RFD checks for a cached value in [the `sqlite` database](#game_setuppersistencesqlite_path).

```toml
retrieve_user_id_call_mode = "lua"
retrieve_user_id = '''
function(user_code)
    return math.random(1, 16777216)
end
'''
```

#### `server_core.retrieve_avatar_type`

Resolves to [function](#functions) type `(int, str) -> Enum.HumanoidRigType`.

Where Rōblox [`Enum.HumanoidRigType`](https://create.roblox.com/docs/reference/engine/enums/HumanoidRigType) can either be `"R6"` or `"R15"`.

```toml
retrieve_avatar_type_call_mode = "lua"
retrieve_avatar_type = '''
function(user_id_num, user_code)
    return 'R15'
end
'''
```

#### `server_core.retrieve_avatar_items`

Resolves to [function](#functions) type `(int, str) -> [int]`.

The returned list contains asset idens from the Rōblox catalogue.

```toml
retrieve_avatar_items_call_mode = "lua"
retrieve_avatar_items = '''
function(user_id_num, user_code)
    return {
        10726856854,
        9482991343,
        9481782649,
        9120251003,
        4381817635,
        6969309778,
        5731052645,
        2846257298,
        121390054,
        261826995,
        154386348,
        201733574,
        48474294,
        6340101,
        192483960,
        190245296,
        183808364,
        34247191,
    }
end
'''
```

#### `server_core.retrieve_avatar_scales`

Resolves to [function](#functions) type `(int, str) -> util.types.structs.avatar_scales`.

```toml
retrieve_avatar_scales_call_mode = "lua"
retrieve_avatar_scales = '''
function(user_id_num, user_code)
    return {
        height = 1,
        width = 0.8,
        head = 1,
        depth = 0.8,
        proportion = 0,
        body_type = 0,
    }
end
'''
```

#### `server_core.retrieve_avatar_colors`

Resolves to [function](#functions) type `(int, str) -> util.types.structs.avatar_colors`.

```toml
retrieve_avatar_colors_call_mode = "lua"
retrieve_avatar_colors = '''
function(user_id_num, user_code)
    return {
        head = 315,
        left_arm = 315,
        left_leg = 315,
        right_arm = 315,
        right_leg = 315,
        torso = 315,
    }
end
'''
```

#### `server_core.retrieve_groups`

Resolves to [function](#functions) type `(int, str) -> dict[str, int]`.

Key is the group iden number written as a string; value is the rank value from 0 to 255.

```toml
retrieve_groups_call_mode = "lua"
retrieve_groups = '''
function(user_id_num, user_code)
    return {
        ['1200769'] = 255;
        ['2868472'] = 255;
        ['4199740'] = 255;
        ['4265462'] = 255;
        ['4265456'] = 255;
        ['4265443'] = 255;
        ['4265449'] = 255;
    }
end
'''
```

#### `server_core.retrieve_account_age`

Resolves to [function](#functions) type `(int, str) -> int`.

```toml
retrieve_account_age_call_mode = "lua"
retrieve_account_age = '''
function(user_id_num, user_code) -- str -> int
    return 6969
end
'''
```

#### `server_core.retrieve_default_funds`

Resolves to [function](#functions) type `(int, str) -> int`.

Established the amount of funds that a player receives when they join a server for the first time. These funds can only be spent on [server-defined gamepasses](#remote_datagamepasses).

```toml
retrieve_default_funds_call_mode = "lua"
retrieve_default_funds = '''
function(user_id_num, user_code)
    return 6969
end
'''
```

#### `server_core.filter_text`

Resolves to [function](#functions) type `(str, int, str) -> str`.

```toml
filter_text_call_mode = "lua"
filter_text = '''
function(text, user_id_num, user_code)
    return text:gsub('oo','òó'):gsub('OO','ÒÓ'):gsub('ee','èé'):gsub('EE','ÈÉ'):gsub('Roblox','Rōblox'):gsub('ROBLOX','RŌBLOX')
end
'''
```

#### `remote_data.gamepasses`

Resolves to a data dictionary.

```toml
[[remote_data.gamepasses]]
id_num = 163231044
name = 'EnforcersPowers'
price = 100
```

#### `remote_data.asset_redirects`

Resolves to [function](#functions) type `(int | str) -> asset_redirect`.

When an RFD server receives a request to load an asset by id, it does so from Roblox.com by default.

However, entries in [`asset_redirects`](#remote_dataasset_redirects) override that default.

Through the `uri` field, assets can load either from a local or remote resource.

The following examples notate the structure into the [dict mode](#dict-mode) syntax:

```toml
[remote_data.asset_redirects.13] # asset iden 13
uri = 'c:\Users\USERNAME\Pictures\Image.jpg'
```

```toml
[remote_data.asset_redirects.14] # asset iden 14
raw_data = 'https://archive.org/download/youtube-WmNfDXTnKMw/WmNfDXTnKMw.webm'
```

You can include a `cmd_line` field if you want the loaded asset to literally come from the `stdout` of a program.

```toml
[remote_data.asset_redirects.15] # asset iden 15
cmd_line = 'curl https://archive.org/download/youtube-WmNfDXTnKMw/WmNfDXTnKMw.webm -L --output -'
```

A `raw_data` field works here too. That literally encapsuates the binary data that will be sent as an asset.

```toml
[remote_data.asset_redirects.16] # asset iden 15
raw_data = '\0'
```

This should also work. It redirects asset iden strings starting wtih `time_music_` to static files on the internet.

```toml
remote_data.asset_redirects = "python"
remote_data.asset_redirects = '''
def f(asset_iden):
    PREFIX = "time_music_"
    if asset_iden.startswith(PREFIX):
        h = int(asset_iden[len(PREFIX):])
        return {
            "uri": "https://github.com/Windows81/Time-Is-Musical/blob/main/hour_%02d.wav" % (h % 24)
        }
    return None
'''
```

#### `remote_data.badges`

Resolves to a data dictionary.

```toml
[[remote_data.badges]]
id_num = 757
name = 'Awardable Badge'
price = 1
```

---

<p align="center"><img src="./Logo.png" height="60px"/></p>
