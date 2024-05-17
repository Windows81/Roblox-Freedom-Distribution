#!/bin/bash

# List of client versions
client_versions=(
    "2018M"
    "2021E"
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

# Ask user for IP address, port number, and username, winebin (doesnt ask winebin)
ip_address=$(whiptail --inputbox "Enter IP address:" 8 60 --title "IP Address" 3>&1 1>&2 2>&3)
port=$(whiptail --inputbox "Enter port number:" 8 60 --title "Port Number" 3>&1 1>&2 2>&3)
username=$(whiptail --inputbox "Enter username:" 8 60 --title "Username" 3>&1 1>&2 2>&3)
winebin=$(cat /home/$USER/RobloxFDLauncherLinux/settings/winebin.txt)

# Perform actions based on the selected client version
# Unfinished clients: 2008,2013L,2014M,2015M,2022M
    "2018M")
    # Execute actions for 2018M client version
    command=exec /home/$USER/RobloxFDLauncherLinux/join.sh 2018M "$ip" "$port" "$username"
    eval "$command" 
    ;;

    "2021E")
        # Execute actions for 2021E client version
        command="$winebin /home/$USER/RobloxFDLauncherLinux/Clients/2021E/RCCService/RobloxPlayerBeta.exe -a 'http://localhost/2021/login/negotiate.ashx' -j 'http://localhost/2021/game/placelauncher.ashx/?placeid=1818&ip=$ip_address&port=$port&id=314975379&app=http://localhost/charscript/Custom.php?hat=0;http://localhost/asset/?id=86498048;http://localhost/asset/?id=86500008;http://localhost/asset/?id=86500036;http://localhost/asset/?id=86500054;http://localhost/asset/?id=86500064;http://localhost/asset/?id=86500078;http://localhost/asset/?id=144076760;http://localhost/asset/?id=144076358;http://localhost/asset/?id=63690008;http://localhost/asset/?id=86500036;http://localhost/asset/?id=86500078;http://localhost/asset/?id=86500064;http://localhost/asset/?id=86500054;http://localhost/asset/?id=86500008;password=314975379|Pastel brown;Pastel brown;Pastel brown;Pastel brown;Pastel brown;Pastel brown&user=$username' -t 1"
        eval "$command"
        ;;
esac
