#!/bin/bash

# List of client versions
client_versions=(
    "Host"
)

# Construct the options string for whiptail
options=()
for version in "${client_versions[@]}"; do
    options+=("$version" "")
done

# Display list of client versions and allow the user to select one
selected_version=$(whiptail --title "Press enter" --menu "Press enter:" 20 60 15 "${options[@]}" 3>&1 1>&2 2>&3)

# Check if the user canceled the selection
if [ $? -ne 0 ]; then
    echo "Selection canceled."
    exit 1
fi

# Ask user for IP address, port number, and username
winebin=$(cat /home/$USER/RobloxFreedomDistribution/settings/winebin.txt)

# Perform actions based on the selected client version
case $selected_version in
    "Host")
        # Execute actions for Host
        command="$winebin /home/$USER/RobloxFreedomDistribution/RFD.exe server"
        eval "$command"
    ;;
esac
