# Rōblox: Freedom Distribution

A Rōblox 'revival' framework built with Python; tested on Python 3.10 and 3.12.

Adapted from the [Rōblox Filtering Disabled](https://jetray.itch.io/roblox-filtering-disabled) project by Jetray, et al.

Users can host their own server instances of Rōblox using binaries from a variety of versions throughout their history.

Players can join existing servers.

Clients will automatically connect to a server of the same version.

Everything here is free-as-in-freedom software.

My use of Rōblox's binaries are unlikely to fall into fair use. Be wary of any potential copyright takedowns.

## Installation

To install _from source_, run:

```
git clone https://github.com/Windows81/Roblox-Freedom-Distribution rfd
cd rfd
pip install -r ./Source/requirements.txt
```

---

To install _as a binary_, run:

```
git clone https://github.com/Windows81/Roblox-Freedom-Distribution rfd
cd rfd
pip install -r ./Source/requirements.txt
```

## Command Syntax

### `server`

Game-specific options are specified in the `--config_path` argument, which defaults to `./GameConfig.toml`. **Please review each option in the config file before starting your server up.**

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

| Option              | Type  | Default |
| ------------------- | ----- | ------- |
| `--rcc_host`, `-rh` | `str` | None    |
| `--rcc_port`, `-rp` | `int` | 2005    |
| `--web_host`, `-wh` | `str` | N/A     |
| `--web_port`, `-wp` | `int` | 2006    |
| `--user_code`, `-u` | `str` | N/A     |

### Misc.

Command syntaxes for `studio` and `download` also exists, but haven't been adequately documented yet.

## Protocols in Use

Anyone can host a server and must leave **two** network ports of their choice accessible.

### RCC (UDP + TCP)

RCC is an acronym for 'Rōblox Cloud Compute', which is the server-side program we use to run the Rōblox physics engine.

Host is specified by the `--rcc_host` or `-rh` option.

Port is specified by the `--rcc_port` or `-rp` option **(defaults to 2005)**.

### Webserver (HTTPS)

The webserver is responsible for facilitating player connections and loading in-game assets.

Host is optionally specified by the `--webserver_host` or `-wh` option, in case RCC is hosted elsewhere.

Port is specified by the `--webserver_port` or `-wp` option **(defaults to 2006)**.

## Studio?

Rōblox Filtering Disabled have a working Studio build from 2022.

You can also use [this 2018M build](https://github.com/Windows81/Roblox-Freedom-Distribution/releases/download/2023-08-31T09%EA%9E%8910Z/v348.Studio.7z) whilst running the Rōblox Filtering Disabled webserver.

If you need any help, please shoot me an issue on GitHub or a message to an account with some form of 'VisualPlugin' elsewhere.

## Credits

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
py Source/_main.py player -rh "2603:8000:1:3a97:81ec:e544:bb42:6975" -rp 2005 -wp 2006
```
