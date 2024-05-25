#!/bin/bash

winebin=$(cat /home/"$USER"/RobloxFreedomDistribution/settings/winebin.txt)
if ! [ -x "$(command -v "$winebin")" ]; then
    echo 'Error: the command linked in winebin.txt is invalid.' >&2
    exit 1
fi

command="$winebin /home/\"$USER\"/RobloxFreedomDistribution/RFD.exe server"
eval "$command"