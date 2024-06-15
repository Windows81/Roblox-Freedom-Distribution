#!/bin/bash

echo "Make sure you have wine,wget & jq installed!"
sleep 5

# Define the base directoriest
base_dir="/home/$USER/RobloxFreedomDistribution"
destination_file="$base_dir/RFD.exe"
settings_dir="$base_dir/settings"
maps_dir="$base_dir/maps"

# Create directories if they do not exist
mkdir -p "$base_dir"
mkdir -p "$settings_dir"
mkdir -p "$maps_dir"

# Get the latest release information from GitHub API
latest_release_info=$(curl -s https://api.github.com/repos/Windows81/Roblox-Freedom-Distribution/releases/latest)

# Extract the URL for RFD.exe from the latest release information
download_url=$(echo "$latest_release_info" | grep -oP '"browser_download_url": "\K(.*RFD.exe)(?=")')

# Download the file using wget
wget "$base_dir" -O "$destination_file"

echo "Downloaded RFD.exe to $destination_file"

# Download the files using wget
wget -O "$base_dir/join.sh" https://raw.githubusercontent.com/Windows81/Roblox-Freedom-Distribution/main/WineBootstrapper/join.sh
wget -O "$base_dir/host.sh" https://raw.githubusercontent.com/Windows81/Roblox-Freedom-Distribution/main/WineBootstrapper/host.sh
wget -O "$base_dir/stop-all.sh" https://raw.githubusercontent.com/Windows81/Roblox-Freedom-Distribution/main/WineBootstrapper/stop-all.sh
wget -O "$base_dir/GameConfig.toml" https://raw.githubusercontent.com/Windows81/Roblox-Freedom-Distribution/main/GameConfig.toml
wget -O "$settings_dir/winebin.txt" https://raw.githubusercontent.com/Windows81/Roblox-Freedom-Distribution/main/WineBootstrapper/winebin.txt
wget -O "$maps_dir/2007Crossroads.rbxl" https://raw.githubusercontent.com/Vector4-new/RobloxFDLauncherLinux/main/maps/2007Crossroads.rbxl

echo "Files downloaded successfully."

echo "Files downloaded successfully."

#Set the Graphics Renderer API to OpenGL (2021)
#mkdir /home/$USER/RobloxFreedomDistribution/Roblox
#mkdir /home/$USER/RobloxFreedomDistribution/Roblox/v463
#mkdir /home/$USER/RobloxFreedomDistribution/Roblox/v463/ClientSettings
#wget https://raw.githubusercontent.com/Twig6943/RobloxGraphicsSwitcherForLinux/main/RFD/2021E/OpenGL/ClientAppSettings.json -O $base_dir/Roblox/v463/Player/ClientSettings/ClientAppSettings.json

#Desktop file integration

#Chmod the scripts
chmod +x $base_dir/join.sh
chmod +x $base_dir/host.sh
chmod +x $base_dir/stop-all.sh
echo "Roblox freedom distribution is now installed!"
sleep 5
