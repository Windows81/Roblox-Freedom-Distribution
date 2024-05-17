#This isnt finished
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

# Perform actions based on the selected client version
case $selected_version in
    "2022M")
        # Execute actions for 2022M client version
        command="exec /home/$USER/RobloxFDLauncherLinux/ManuelHostScripts/2022M_HostScript.sh"
        eval "$command"
        ;;
    *)

        # Ask user for IP address, port number, and username, winebin
        map=$(whiptail --inputbox "Enter mapname without file extension:" 8 60 --title "Map file name" 3>&1 1>&2 2>&3)
        port=$(whiptail --inputbox "Enter port number:" 8 60 --title "Port Number" 3>&1 1>&2 2>&3)
        

        # Perform actions based on the selected client version
        case $selected_version in
            "2008M")
                command="exec /home/$USER/RobloxFDLauncherLinux/host.sh 2008M \"/home/$USER/RobloxFDLauncherLinux/maps/$map.rbxl\" $port"
                eval "$command"
                ;;
            "2013L")
                # Execute actions for 2013L client version
                command="exec /home/$USER/RobloxFDLauncherLinux/host.sh 2013L \"/home/$USER/RobloxFDLauncherLinux/maps/$map.rbxl\" $port"
                eval "$command"
                ;;
            "2014M")
                # Execute actions for 2014M client version
                command="exec /home/$USER/RobloxFDLauncherLinux/host.sh 2014M \"/home/$USER/RobloxFDLauncherLinux/maps/$map.rbxl\" $port"
                eval "$command"
                ;;
            "2015M")
                # Execute actions for 2015M client version
                command="exec /home/$USER/RobloxFDLauncherLinux/host.sh 2015M \"/home/$USER/RobloxFDLauncherLinux/maps/$map.rbxl\" $port"
                eval "$command"
                ;;
            "2016L")
                # Execute actions for 2016L client version
                command="exec /home/$USER/RobloxFDLauncherLinux/host.sh 2016L \"/home/$USER/RobloxFDLauncherLinux/maps/$map.rbxl\" $port"
                eval "$command"
                ;;
            "2017M")
                # Execute actions for 2017M client version
                command="exec /home/$USER/RobloxFDLauncherLinux/host.sh 2017M \"/home/$USER/RobloxFDLauncherLinux/maps/$map.rbxl\" $port"
                eval "$command"
                ;;
            "2018E")
                # Execute actions for 2018E client version
                command="exec /home/$USER/RobloxFDLauncherLinux/host.sh 2018E \"/home/$USER/RobloxFDLauncherLinux/maps/$map.rbxl\" $port"
                eval "$command" 
                ;;
            "2018M")
                # Execute actions for 2018M client version
                command="exec /home/$USER/RobloxFDLauncherLinux/host.sh 2018M \"/home/$USER/RobloxFDLauncherLinux/maps/$map.rbxl\" $port"
                eval "$command" 
                ;;
            "2018L")
                # Execute actions for 2018L client version
                command="exec /home/$USER/RobloxFDLauncherLinux/host.sh 2018L \"/home/$USER/RobloxFDLauncherLinux/maps/$map.rbxl\" $port"
                eval "$command" 
                ;;
            "2019M")
                # Execute actions for 2019M client version
                command="exec /home/$USER/RobloxFDLauncherLinux/host.sh 2019M \"/home/$USER/RobloxFDLauncherLinux/maps/$map.rbxl\" $port"
                eval "$command"
                ;;
            "2020L")
                # Execute actions for 2020L client version
                command="exec /home/$USER/RobloxFDLauncherLinux/host.sh 2020L \"/home/$USER/RobloxFDLauncherLinux/maps/$map.rbxl\" $port"
                eval "$command" 
                ;;
            "2021E")
                # Execute actions for 2021E client version
                command="exec /home/$USER/RobloxFDLauncherLinux/host.sh 2021E \"/home/$USER/RobloxFDLauncherLinux/maps/$map.rbxl\" $port"
                eval "$command"
                ;;
        esac
        ;;
esac
