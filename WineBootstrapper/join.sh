#!/bin/bash

winebin=$(cat settings/winebin.txt)
if ! [ -x "$(command -v "$winebin")" ]; then
    echo 'Error: the command linked in winebin.txt is invalid.' >&2
    exit 1
fi

# Asks user for IP address, port number, and user code.
ip_address=$(whiptail --inputbox "Enter IP address:" 8 60 --title "IP Address" 3>&1 1>&2 2>&3)
port=$(whiptail --inputbox "Enter RCC port number:" 8 60 --title "RCC Port Number" 3>&1 1>&2 2>&3)
secondary_port=$(whiptail --inputbox "Enter webserver port number:" 8 60 --title "Webserver Port Number" 3>&1 1>&2 2>&3)
username=$(whiptail --inputbox "Enter user code:" 8 60 --title "User Code" 3>&1 1>&2 2>&3)

command="$winebin start RFD.exe player -rh $ip_address -rp $port -wp $secondary_port -u $username"
eval "$command"
