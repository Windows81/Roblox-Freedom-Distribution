#!/bin/bash

winebin=$(cat /home/"$USER"/RobloxFreedomDistribution/settings/winebin.txt)
if ! [ -x "$(command -v "$winebin")" ]; then
    echo 'Error: the command linked in winebin.txt is invalid.' >&2
    exit 1
fi

# Asks user for IP address, port number, and user code.
ip_address=$(whiptail --inputbox "Enter IP address:" 8 60 --title "IP Address" 3>&1 1>&2 2>&3)
port=$(whiptail --inputbox "Enter primary port number:" 8 60 --title "Primary Port Number" 3>&1 1>&2 2>&3)
secondary_port=$(whiptail --inputbox "Enter secondary port number:" 8 60 --title "Secondary Port Number" 3>&1 1>&2 2>&3)
username=$(whiptail --inputbox "Enter user code:" 8 60 --title "Username" 3>&1 1>&2 2>&3)

command="$winebin /home/\"$USER\"/RobloxFreedomDistribution/RFD.exe player -rh $ip_address -rp $port -wp $secondary_port -u $username"
eval "$command"