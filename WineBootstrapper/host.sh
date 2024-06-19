#!/bin/bash

winebin=$(cat settings/winebin.txt)
if ! [ -x "$(command -v "$winebin")" ]; then
    echo 'Error: the command linked in winebin.txt is invalid.' >&2
    exit 1
fi

#Add "start" after $winebin if you want the terminal window to disappear 
command="$winebin RFD.exe server"
eval "$command"
