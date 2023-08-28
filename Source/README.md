# Rōblox Filtering Disabled

Adapted from the [Rōblox Filtering Disabled](https://jetray.itch.io/roblox-filtering-disabled) project by Jetray, et al.

Users can host their own server instances of Rōblox using binaries from a selection of versions.

Players can join an existing server

Clients must connect to a server of the same version.

# Command Syntax

Anyone can host a server and must leave **two** network ports of their choice accessible:

## RCC (both TCP & UDP)

RCC is an acronym for 'Rōblox Cloud Compute', which is the server-side program we use to run the Rōblox physics engine.

Host is specified by the `--rcc_host` or `-rh` option.

Port is specified by the `--rcc_port` or `-rp` option **(defaults to 2005)**.

## Webserver (HTTP or HTTPS)

The webserver is responsible for facilitating player connections and loading in-game assets.

Host is optionally specified by the `--webserver_host` or `-wh` option, in case RCC is hosted elsewhere.

Port is specified by the `--webserver_port` or `-wp` option **(defaults to 2006)**.

# Credits:

_iknowidontexistbutwhatifwin_ for patching the v463 (early 2021) binaries.
_Jetray_ for engineering the original [Rōblox Filtering Disabled](https://jetray.itch.io/roblox-filtering-disabled) server in PHP.
**More to come...**

# Examples

## Server

```shell
py launcher/main.py -v 2018M server -rp 2005 -wp 2006 -p "C:\Users\USERNAME\Documents\Baseplate.rbxl"
```

## Player

```shell
py launcher/main.py -v 2018M player -rh localhost -rp 2005 -wp 2006
```
