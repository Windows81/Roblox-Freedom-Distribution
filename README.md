# Rōblox: Freedom Distribution

Adapted from the [Rōblox Filtering Disabled](https://jetray.itch.io/roblox-filtering-disabled) project by Jetray, et al.

Users can host their own server instances of Rōblox using binaries from a variety of versions throughout their history.

Players can join an existing server.

Clients will automatically connect to a server of the same version.

## Command Syntax

### `server`

| Option                 | Type         | Default             |
| ---------------------- | ------------ | ------------------- |
| `--config_path`, `-cp` | `int`        | `./GameConfig.toml` |
| `--rcc_port`, `-rp`    | `int`        | 2005                |
| `--web_port`, `-wp`    | `int`        | 2006                |
| `--run_client`, `-rc`  | `store_true` | N/A                 |
| `--skip_rcc`           | `store_true` | N/A                 |
| `--skip_rcc_popen`     | `store_true` | N/A                 |
| `--skip_web`           | `store_true` | N/A                 |

### `player`

| Option              | Type  | Default          |
| ------------------- | ----- | ---------------- |
| `--rcc_host`, `-rh` | `str` | None, nargs=`?`, |
| `--rcc_port`, `-rp` | `int` | 2005, nargs=`?`, |
| `--web_host`, `-wh` | `str` | N/A, nargs=`?`,  |
| `--web_port`, `-wp` | `int` | 2006, nargs=`?`, |
| `--user_code`, `-u` | `str` | N/A              |

### Misc.

Command syntaxes for `studio` and `download` also exists, but haven't been adequately documented yet.

## Protocols in Use:

Anyone can host a server and must leave **two** network ports of their choice accessible.

### RCC (UDP + TCP)

RCC is an acronym for 'Rōblox Cloud Compute', which is the server-side program we use to run the Rōblox physics engine.

Host is specified by the `--rcc_host` or `-rh` option.

Port is specified by the `--rcc_port` or `-rp` option **(defaults to 2005)**.

### Webserver (HTTPS)

The webserver is responsible for facilitating player connections and loading in-game assets.

Host is optionally specified by the `--webserver_host` or `-wh` option, in case RCC is hosted elsewhere.

Port is specified by the `--webserver_port` or `-wp` option **(defaults to 2006)**.

## Credits:

_iknowidontexistbutwhatifwin_ for patching the v463 (early 2021) binaries.

_Jetray_ for engineering the original [Rōblox Filtering Disabled](https://jetray.itch.io/roblox-filtering-disabled) server in PHP.

**More to come...**

## Examples

### Server

```shell
py Source/_main.py server -rp 2005 -wp 2006
```

### Player

```shell
py Source/_main.py player -rh localhost -rp 2005 -wp 2006
```
