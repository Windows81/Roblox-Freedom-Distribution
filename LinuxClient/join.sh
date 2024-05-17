#!/usr/bin/env bash

# usage: join.sh <client> <ip> <port> <username>
# appearance can be changed using the customize script
winebin=$(cat /home/$USER/RobloxFDLauncherLinux/settings/winebin.txt)

if [[ $# -ne 4 ]]; then
    echo "usage: $0 <client> <ip> <port> <username>"
    echo "appearance can be changed using the 'customize.sh' script"

    exit
fi

pushd $(dirname $0) > /dev/null

if [[ ! -d "shared" || ! -d "Clients" ]]; then
    echo "Clients don't exist!"
    echo "Install it by going aeplexi.itch.io/roblox-filtering-disabled, download FilteringDisabled.7z, and extract the 'shared' and 'Clients' folders here"
    popd > /dev/null
    exit
fi

curl -sf localhost > /dev/null

if [[ $? -eq 7 ]]; then
    echo "The webserver hasn't been started!"
    echo "Start it by going to the webserver directory and running 'start.sh'"
    popd > /dev/null
    exit
fi

if [ $3 -gt 1023 ] 2> /dev/null; then
    :
else
    echo "Port '$3' is either not an integer over 1023 or an invalid integer"
    popd > /dev/null
    exit
fi

CLIENT=${1^^}
IP=$2
PORT=$3
USERNAME=$4
USERID=$(cat settings/server/serverPassword.txt)

function Join2022M() {
    # doesn't work
    
    STUDIO_SCRIPT=$(cat templates/StudioClient.lua)
    STUDIO_SCRIPT=${STUDIO_SCRIPT//%USERNAME%/$USERNAME}
    STUDIO_SCRIPT=${STUDIO_SCRIPT//%APPEARANCE%/${APPEARANCE:0:-1}}
    STUDIO_SCRIPT=${STUDIO_SCRIPT//%BODYCOLOURS%/${BODY_COLOURS:0:-1}}

    cd Clients/2022M
    ((nohup $winebin RobloxStudioBeta.exe -task StartClient -server "$IP" -port $PORT &> /dev/null) &) &> /dev/null
}

function Join2015L() {
    cd shared

    ((nohup $winebin ${CLIENT:0:-1}Player.exe -a "http://localhost/Login/Negotiate.ashx" -j "http://localhost/game/placelaunchrrr.php/?placeid=1818&ip=$IP&port=$PORT&id=$USERID&app=$FULL_APPEARANCE&user=$USERNAME" -t "1" &> /dev/null) &) &> /dev/null
}

function Join2017M() {
    cd shared

    ((nohup $winebin 2017Player.exe -a "http://localhost/Login/Negotiate.ashx" -j "http://localhost/game/join.php/?placeid=1818&ip=$IP&port=$PORT&id=$USERID&app=$FULL_APPEARANCE&user=$USERNAME" -t "1" &> /dev/null) &) &> /dev/null
}

function Join2021E() {
    FULL_APPEARANCE=${FULL_APPEARANCE//1111111/""}

    cd Clients/$CLIENT/RCCService

    ((nohup $winebin RobloxPlayerBeta.exe -a "http://localhost/2021/Login/Negotiate.ashx" -j "http://localhost/2021/game/placelauncher.ashx?placeid=1818&ip=$IP&user=$USERNAME&port=$PORT&id=$USERID&app=$FULL_APPEARANCE" -t "1" &> /dev/null) &) &> /dev/null
}

function Join2019M2020L() {
    FULL_APPEARANCE=${FULL_APPEARANCE//1111111/""}

    cd Clients/$CLIENT

    ((nohup $winebin RobloxPlayerBeta.exe -a "http://localhost/2021/Login/Negotiate.ashx" -j "http://localhost/2021/game/placelauncher.ashx?placeid=1818&ip=$IP&user=$USERNAME&port=$PORT&id=$USERID&app=$FULL_APPEARANCE" -t "1" &> /dev/null) &) &> /dev/null
}

function Join2014M() {
    # works, kinda. cores don't load and camera is kinda messed up, but may be a VM artifact
    FULL_APPEARANCE=${FULL_APPEARANCE//localhost/localhost\/www.civdefn.tk}

    cd Clients/$CLIENT

    ((nohup $winebin RobloxPlayerBeta.exe -a "http://localhost/www.civdefn.tk/" -j "http://localhost/www.civdefn.tk/game/join.php?port=$PORT&app=$FULL_APPEARANCE&ip=$IP&username=$USERNAME&id=$USERID&mode=1" -t "1") &) &> /dev/null
}

function Join2008M() {
    JOINSCRIPT=$(cat templates/2008Mjoin.txt)
    JOINSCRIPT=${JOINSCRIPT//%port%/$PORT}
    JOINSCRIPT=${JOINSCRIPT//%ip%/\"$IP\"}
    JOINSCRIPT=${JOINSCRIPT//%name%/\"$USERNAME\"}
    JOINSCRIPT=${JOINSCRIPT//%id%/$USERID}
    JOINSCRIPT="charapp = [[${APPEARANCE:0:-1}|${BODY_COLOURS:0:-1}]] $JOINSCRIPT"
    echo "$JOINSCRIPT" > Clients/2008M/Player/content/join.txt

    cd Clients/2008M/Player

    ((nohup $winebin Roblox.exe -script "dofile('rbxasset://join.txt')" &> /dev/null) &) &> /dev/null
}

function Join2018() {
    FULL_APPEARANCE=${FULL_APPEARANCE//1111111/""}

    cd Clients/$CLIENT/Player

    ((nohup $winebin RobloxPlayerBeta.exe -a "http://localhost/Login/Negotiate.ashx" -j "http://localhost/game/placelauncher.ashx?&year=2018&placeid=1818&ip=$IP&port=$PORT&id=$USERID&app=$FULL_APPEARANCE&user=$USERNAME" -t "1" &> /dev/null) &) &> /dev/null
}

APPEARANCE=$(awk ' { printf "%s;", $0 } ' settings/client/appearance.txt)
BODY_COLOURS=$(awk ' { printf "%s;", $0 } ' settings/client/bodyColours.txt)
FULL_APPEARANCE="$APPEARANCE""password=$(cat settings/server/serverPassword.txt)|${BODY_COLOURS:0:-1}"

case ${1^^} in
    "2022M") Join2022M ;;
    "2016L"|"2015M") Join2015L ;;
    "2017M") Join2017M ;;
    "2021E") Join2021E ;;
    "2019M"|"2020L") Join2019M2020L ;;
    "2014M"|"2013L") Join2014M ;;
    "2008M") Join2008M ;;
    "2018E"|"2018M"|"2018L") Join2018 ;;
    *) echo "Unrecognized client '$1'." ;;
esac

popd > /dev/null
