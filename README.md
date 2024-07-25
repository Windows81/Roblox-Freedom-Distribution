<h1 align="center"><img src="./Logo.png" height="20px"/> Rōblox: Freedom Distribution <img src="./Logo.png" height="20px"/></h1>

_Want to host your own Rōblox LAN parties? Looking for a way to deploy your Rōblox experiences, new and old, on your own machine?_

Rōblox Freedom Distribution is one such solution. It's a 'revival' launcher built on existing research for self-hosting Rōblox servers.

Using RFD, users can host their own server instances from compiled Rōblox binaries from 2018-07-25 or 2021-01-25.

Players can join existing servers.

Clients only need to keep track of which hosts and ports to connect to. That's because clients will automatically connect to a server of the same version.

**If you worked with Python (3.10–3.12) before, [_initial_ setup](#installation) is supposed to take less than a minute. Why _initial_? Freedom Distribution automatically downloads additional data (at most 90 MiB) for you.**

Initial adaptation from the [Rōblox Filtering Disabled](https://jetray.itch.io/roblox-filtering-disabled) project by Jetray, et al.

All the code is free-as-in-freedom software and is licensed under the GNU GPL v3.

_This README is optimised for viewing on [GitHub](https://github.com/Windows81/Roblox-Freedom-Distribution)._

## Copyright Acknowledgement

My use of Rōblox's binaries are unlikely to fall into fair use. Be wary of any potential copyright takedowns.

In the event of a DMCA takedown, don't rely on forks of this repo on GitHub. Consider using other means. Also consult this [document](./LEGAL.md) if you want to know why I believe I'm protected under fair-use law.

## Installation

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
./RFD.exe player -rh 172.88.194.43 -rp 2005 -wp 2006
```

#### For GNU/Linux

Consult [`./WineBootstrapper/README.md`](./WineBootstrapper/README.md)

### From [Source](https://github.com/Windows81/Roblox-Freedom-Distribution/archive/refs/heads/main.zip)

This is good for if you already have Python installed on your machine. Do you want to help contribute to RFD? Use this.

To install _from source_, run:

```
git clone --depth 1 https://github.com/Windows81/Roblox-Freedom-Distribution rfd
cd rfd
pip install -r ./Source/requirements.txt
```

To launch RFD, your command line will look something like this:

```
py Source/_main.py player -rh 172.88.194.43 -rp 2005 -wp 2006
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

## Network Ports in Use

Anyone can host a server and must leave **two** network ports of their choice accessible.

### RCC (UDP)

RCC is an acronym for 'Rōblox Cloud Compute', which is the `exe` program we use to run the Rōblox servers. It leaves one (maybe two) relevant port open.

Host is specified by the `--rcc_host` or `-rh` option.

Port is specified by the `--rcc_port` or `-rp` option **(defaults to 2005)**.

### Webserver (HTTPS)

The webserver is responsible for facilitating player connections and loading in-game assets.

Host is optionally specified by the `--webserver_host` or `-wh` option, in case RCC is hosted elsewhere.

Port is specified by the `--webserver_port` or `-wp` option **(defaults to 2006)**.

## Studio?

You can modify `rbxl` file in current-day Studio as of July 2024. For compatibility with older clients, _RFD comes with its own [serialiser suite](./Source/assets/serialisers/)_. Objects transformed include:

1. Fonts which existed in their respective versions,
1. And meshes encoded with versions 4 or 5 _back_ to version 3.

However, **union operations done in current-day Studio (CSG v3) are not supported**.

In that case...

[Rōblox Filtering Disabled](https://beepboopbap.itch.io/filtering-disabled) has a working Studio build from 2022.

[Sodikm](https://archive.org/details/full-sodikm_202308) has a functional Studio build from 2018.

You can also use [this 2018M build](https://github.com/Windows81/Roblox-Freedom-Distribution/releases/download/2023-08-31T09%EA%9E%8910Z/v348.Studio.7z) whilst running the Rōblox Filtering Disabled webserver.

If you need any help, please shoot me an issue on GitHub or a message to an account with some form of 'VisualPlugin' elsewhere.

## Credits

_iknowidontexistbutwhatifwin_ for making initial patches to the v463 (early 2021) binaries.

_Jetray_ and others for engineering the original [Rōblox Filtering Disabled](https://jetray.itch.io/roblox-filtering-disabled) server in PHP.

_Twig6843_ for [`./WineBootstrapper`](./WineBootstrapper/).

**More to come...**

## Examples

Where `...` is [your command-line prefix](#installation),

### Server

```shell
... server -rp 2005 -wp 2006 --config ./GameConfig.toml
```

### Player

```shell
... player -rh 172.88.194.43 -rp 2005 -wp 2006
```

---

<p align="center"><img src="./Logo.png" height="60px"/></p>
