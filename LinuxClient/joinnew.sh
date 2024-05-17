
#!/bin/bash

# List of client versions
client_versions=(
    "2008M"
    "2013L"
    "2014M"
    "2015M"
    "2016L"
    "2017M"
    "2018E"
    "2018M"
    "2018L"
    "2019M"
    "2020L"
    "2021E"
    "2022M"
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
case $selected_version in
    "2008M")
    command=exec /home/$USER/RobloxFDLauncherLinux/join.sh 2008M "$ip" "$port" "$username"
    eval "$command"
    ;;
    "2013L")
    # Execute actions for 2013L client version
    command=exec /home/$USER/RobloxFDLauncherLinux/join.sh 2013L "$ip" "$port" "$username"
    eval "$command"
    ;;
    "2014M")
    # Execute actions for 2014M client version
    command=exec /home/$USER/RobloxFDLauncherLinux/join.sh 2014M "$ip" "$port" "$username"
    eval "$command"
    ;;
    "2015M")
    # Execute actions for 2015M client version
    command=exec /home/$USER/RobloxFDLauncherLinux/join.sh 2015M "$ip" "$port" "$username"
    eval "$command"
    ;;
    "2016L")
    # Execute actions for 2016L client version
    command=exec /home/$USER/RobloxFDLauncherLinux/join.sh 2016L "$ip" "$port" "$username"
    eval "$command"
    ;;
    "2017M")
    # Execute actions for 2017M client version
    command=exec /home/$USER/RobloxFDLauncherLinux/join.sh 2017M "$ip" "$port" "$username"
    eval "$command"
    ;;
    "2018E")
    # Execute actions for 2018E client version
    command=exec /home/$USER/RobloxFDLauncherLinux/join.sh 2018E "$ip" "$port" "$username"
    eval "$command" 
    ;;
    "2018M")
    # Execute actions for 2018M client version
    command=exec /home/$USER/RobloxFDLauncherLinux/join.sh 2018M "$ip" "$port" "$username"
    eval "$command" 
    ;;
    "2018L")
    # Execute actions for 2018L client version
    command=exec /home/$USER/RobloxFDLauncherLinux/join.sh 2018L "$ip" "$port" "$username"
    eval "$command" 
    ;;
    "2019M")
    # Execute actions for 2019M client version
    command="$winebin /home/$USER/RobloxFDLauncherLinux/Clients/2019M/RobloxPlayerBeta.exe -a 'http://localhost/2021/Login/Negotiate.ashx' -j 'http://localhost/2021/game/placelauncher.ashx?placeid=1818&ip=$ip&user=$username&port=$port&id=923746287&app=http://localhost/charscript/Custom.php?hat=0%3Bhttp://localhost/asset/?id=86498048%3Bhttp://localhost/asset/?id=86500008%3Bhttp://localhost/asset/?id=86500036%3Bhttp://localhost/asset/?id=86500054%3Bhttp://localhost/asset/?id=86500064%3Bhttp://localhost/asset/?id=86500078%3Bhttp://localhost/asset/?id=144076760%3Bhttp://localhost/asset/?id=144076358%3Bhttp://localhost/asset/?id=63690008%3Bhttp://localhost/asset/?id=86500036%3Bhttp://localhost/asset/?id=86500078%3Bhttp://localhost/asset/?id=86500064%3Bhttp://localhost/asset/?id=86500054%3Bhttp://localhost/asset/?id=86500008&password=923746287|Pastel%20brown%3BPastel%20brown%3BPastel%20brown%3BPastel%20brown%3BPastel%20brown%3BPastel%20brown' -t 1"
    eval "$command"
    ;;
    "2020L")
        # Execute actions for 2020L client version
                command="$winebin /home/$USER/RobloxFDLauncherLinux/Clients/2020L/RobloxPlayerBeta.exe -a 'http://localhost/2021/login/negotiate.ashx' -j 'http://localhost/2021/game/placelauncher.ashx/?placeid=1818&ip=$ip_address&port=$port&id=314975379&app=http://localhost/charscript/Custom.php?hat=0;http://localhost/asset/?id=86498048;http://localhost/asset/?id=86500008;http://localhost/asset/?id=86500036;http://localhost/asset/?id=86500054;http://localhost/asset/?id=86500064;http://localhost/asset/?id=86500078;http://localhost/asset/?id=144076760;http://localhost/asset/?id=144076358;http://localhost/asset/?id=63690008;http://localhost/asset/?id=86500036;http://localhost/asset/?id=86500078;http://localhost/asset/?id=86500064;http://localhost/asset/?id=86500054;http://localhost/asset/?id=86500008;password=314975379|Pastel brown;Pastel brown;Pastel brown;Pastel brown;Pastel brown;Pastel brown&user=$username' -t 1"
        eval "$command" 
            ;;
    "2021E")
        # Execute actions for 2021E client version
        command="$winebin /home/$USER/RobloxFDLauncherLinux/Clients/2021E/RCCService/RobloxPlayerBeta.exe -a 'http://localhost/2021/login/negotiate.ashx' -j 'http://localhost/2021/game/placelauncher.ashx/?placeid=1818&ip=$ip_address&port=$port&id=314975379&app=http://localhost/charscript/Custom.php?hat=0;http://localhost/asset/?id=86498048;http://localhost/asset/?id=86500008;http://localhost/asset/?id=86500036;http://localhost/asset/?id=86500054;http://localhost/asset/?id=86500064;http://localhost/asset/?id=86500078;http://localhost/asset/?id=144076760;http://localhost/asset/?id=144076358;http://localhost/asset/?id=63690008;http://localhost/asset/?id=86500036;http://localhost/asset/?id=86500078;http://localhost/asset/?id=86500064;http://localhost/asset/?id=86500054;http://localhost/asset/?id=86500008;password=314975379|Pastel brown;Pastel brown;Pastel brown;Pastel brown;Pastel brown;Pastel brown&user=$username' -t 1"
        eval "$command"
        ;;
    "2022M")
        # Execute actions for 2022M client version
        command="$winebin /home/$USER/RobloxFDLauncherLinux/Clients/2022M/RobloxStudioBeta.exe -task StartClient -server \"$ip\" -port $port"
        eval "$command"
        ;;    
esac
