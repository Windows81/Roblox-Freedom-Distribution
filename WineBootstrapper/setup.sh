#!/bin/bash

echo "Make sure you have wine,wget & jq installed!"
sleep 3
echo "If you want to install Roblox Freedom Distribution to another drive please change the "base_dir" variable in the script to your preferred location"
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

# Fetch the latest release information from GitHub API and parse the URL using jq
download_url=$(wget -qO- https://api.github.com/repos/Windows81/Roblox-Freedom-Distribution/releases/latest | jq -r '.assets[] | select(.name == "RFD.exe") | .browser_download_url')

# Check if download_url is not empty
if [ -z "$download_url" ]; then
  echo "Error: Could not find the download URL for RFD.exe"
  exit 1
fi

# Download the file using wget
wget "$download_url" -O "$destination_file"

echo "Downloaded RFD.exe to $destination_file"


# Download the files using wget
wget -O "$base_dir/join.sh" https://raw.githubusercontent.com/Windows81/Roblox-Freedom-Distribution/main/WineBootstrapper/join.sh
wget -O "$base_dir/host.sh" https://raw.githubusercontent.com/Windows81/Roblox-Freedom-Distribution/main/WineBootstrapper/host.sh
wget -O "$base_dir/menu.sh" https://raw.githubusercontent.com/Windows81/Roblox-Freedom-Distribution/main/WineBootstrapper/menu.sh
wget -O "$base_dir/stop-all.sh" https://raw.githubusercontent.com/Windows81/Roblox-Freedom-Distribution/main/WineBootstrapper/stop-all.sh
wget -O "$base_dir/GameConfig.toml" https://raw.githubusercontent.com/Windows81/Roblox-Freedom-Distribution/main/GameConfig.toml
wget -O "$settings_dir/winebin.txt" https://raw.githubusercontent.com/Windows81/Roblox-Freedom-Distribution/main/WineBootstrapper/winebin.txt
wget -O "$maps_dir/2007Crossroads.rbxl" https://raw.githubusercontent.com/Vector4-new/RobloxFDLauncherLinux/main/maps/2007Crossroads.rbxl


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
chmod +x $base_dir/menu.sh
chmod +x $base_dir/stop-all.sh

#Desktop file stuff
wget -O "/home/$USER/.local/share/icons/hicolor/256x256/apps/freedom.png" https://github.com/Windows81/Roblox-Freedom-Distribution/blob/main/freedom.png?raw=true 


#Create .desktop Entry
rm ~/.local/share/applications/FreedomDistribution.desktop
echo "[Desktop Entry]" >> ~/.local/share/applications/FreedomDistribution.desktop
echo "Name=FreedomDistribution" >> ~/.local/share/applications/FreedomDistribution.desktop
echo "Comment=A fork of the Rōblox Filtering Disabled project which allows people to host their own instances of Rōblox for other people to play." >> ~/.local/share/applications/FreedomDistribution.desktop
echo "Icon=/home/$USER/.local/share/icons/hicolor/256x256/apps/freedom.png" >> ~/.local/share/applications/FreedomDistribution.desktop
echo "Exec=$base_dir/menu.sh" >> ~/.local/share/applications/FreedomDistribution.desktop
echo "Terminal=True" >> ~/.local/share/applications/FreedomDistribution.desktop
echo "Type=Application" >> ~/.local/share/applications/FreedomDistribution.desktop
echo "Categories=Game;" >> ~/.local/share/applications/FreedomDistribution.desktop
echo "StartupNotify=true" >> ~/.local/share/applications/FreedomDistribution.desktop
echo "Path=$base_dir" >> ~/.local/share/applications/FreedomDistribution.desktop
cp ~/.local/share/applications/FreedomDistribution.desktop ~/Desktop/FreedomDistribution.desktop

echo "Roblox freedom distribution is now installed!"
sleep 5
