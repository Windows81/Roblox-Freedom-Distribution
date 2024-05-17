#!/bin/bash

# List of client versions
client_versions=(
    "Join"
)

# Construct the options string for whiptail
options=()
for version in "${client_versions[@]}"; do
    options+=("$version" "")
done

# Display list of client versions and allow the user to select one
selected_version=$(whiptail --title "Client Version Selection" --menu "Choose a client version:" 20 60 15 "${options[@]}" 3>&1 1>&2 2>&3)

# Check if the user canceled the selection
if [ $? -ne 0 ]; then
    echo "Selection canceled."
    exit 1
fi

# Ask user for IP address, port number, and username
ip_address=$(whiptail --inputbox "Enter IP address:" 8 60 --title "IP Address" 3>&1 1>&2 2>&3)
port=$(whiptail --inputbox "Enter primary port number:" 8 60 --title "Primary Port Number" 3>&1 1>&2 2>&3)
secondary_port=$(whiptail --inputbox "Enter secondary port number:" 8 60 --title "Secondary Port Number" 3>&1 1>&2 2>&3)
username=$(whiptail --inputbox "Enter username:" 8 60 --title "Username" 3>&1 1>&2 2>&3)
winebin=$(cat /home/$USER/RobloxFreedomDistribution/settings/winebin.txt)

# Perform actions based on the selected client version
case $selected_version in
    "Join")
    # Execute actions for Join
    command="$winebin /home/$USER/RobloxFreedomDistribution/RFD.exe player -rh $ip_address -rp $port -wp $secondary_port -u $username"
    eval "$command"
    ;;
esac
