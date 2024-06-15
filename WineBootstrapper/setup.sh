#!/bin/bash

#This uses an older version with wine (the latest RFD.exe seems to not work with wine. We're working on getting the latest version to work with wine.)

# Get the latest release information from GitHub API
latest_release_info=$(curl -s https://api.github.com/repos/Windows81/Roblox-Freedom-Distribution/releases/latest)

# Extract the URL for RFD.exe from the latest release information
download_url=$(echo "$latest_release_info" | grep -oP '"browser_download_url": "\K(.*RFD.exe)(?=")')

# Define the destination directory and file path
destination_dir="/home/$USER/RobloxFreedomDistribution"
destination_file="$destination_dir/RFD.exe"

# Download the file using wget
wget "$download_url" -O "$destination_file"

echo "Downloaded RFD.exe to $destination_file"

# Define the base directory
base_dir="/home/$USER/RobloxFreedomDistribution"
settings_dir="$base_dir/settings"
maps_dir="$base_dir/maps"

# Create directories if they do not exist
mkdir -p "$base_dir"
mkdir -p "$settings_dir"
mkdir -p "$maps_dir"

# Download the files using curl
curl -L https://raw.githubusercontent.com/Windows81/Roblox-Freedom-Distribution/main/WineBootstrapper/join.sh -o "$base_dir/join.sh"
curl -L https://raw.githubusercontent.com/Windows81/Roblox-Freedom-Distribution/main/WineBootstrapper/host.sh -o "$base_dir/host.sh"
curl -L https://raw.githubusercontent.com/Windows81/Roblox-Freedom-Distribution/main/WineBootstrapper/stop-all.sh -o "$base_dir/stop-all.sh"
curl -L https://raw.githubusercontent.com/Windows81/Roblox-Freedom-Distribution/main/GameConfig.toml -o "$base_dir/GameConfig.toml"
curl -L https://raw.githubusercontent.com/Windows81/Roblox-Freedom-Distribution/main/WineBootstrapper/winebin.txt -o "$settings_dir/winebin.txt"
curl -L https://raw.githubusercontent.com/Vector4-new/RobloxFDLauncherLinux/main/maps/2007Crossroads.rbxl -o "$maps_dir/2007Crossroads.rbxl"

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
