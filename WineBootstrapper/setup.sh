#!/bin/bash

winebin=$(cat /home/"$USER"/RobloxFreedomDistribution/settings/winebin.txt)
if ! [ -x "$(command -v "$winebin")" ]; then
    echo 'Error: the command linked in winebin.txt is invalid.' >&2
    exit 1
fi

mkdir /home/"$USER"/RobloxFreedomDistribution
mkdir /home/"$USER"/RobloxFreedomDistribution/settings
wget https://github.com/Windows81/Roblox-Freedom-Distribution/releases/download/2024-06-06T0437Z/RFD.exe -O /home/"$USER"/RobloxFreedomDistribution/RFD.exe
wget https://raw.githubusercontent.com/Windows81/Roblox-Freedom-Distribution/main/WineBootstrapper/join.sh -O /home/"$USER"/RobloxFreedomDistribution/join.sh
wget https://raw.githubusercontent.com/Windows81/Roblox-Freedom-Distribution/main/WineBootstrapper/host.sh -O /home/"$USER"/RobloxFreedomDistribution/host.sh
wget https://raw.githubusercontent.com/Windows81/Roblox-Freedom-Distribution/main/WineBootstrapper/stop-all.sh -O /home/"$USER"/RobloxFreedomDistribution/stop-all.sh
wget https://raw.githubusercontent.com/Windows81/Roblox-Freedom-Distribution/main/WineBootstrapper/GameConfig.toml -O /home/"$USER"/RobloxFreedomDistribution/GameConfig.toml
wget https://raw.githubusercontent.com/Windows81/Roblox-Freedom-Distribution/main/WineBootstrapper/winebin.txt -O /home/"$USER"/RobloxFreedomDistribution/settings/winebin.txt
mkdir /home/"$USER"/.wine/drive_c/robloxmaps
wget https://raw.githubusercontent.com/Vector4-new/RobloxFDLauncherLinux/main/maps/2007Crossroads.rbxl -O /home/"$USER"/.wine/drive_c/robloxmaps/2007Crossroads.rbxl

chmod +x /home/"$USER"/RobloxFreedomDistribution/join.sh
chmod +x /home/"$USER"/RobloxFreedomDistribution/host.sh
chmod +x /home/"$USER"/RobloxFreedomDistribution/stop-all.sh
