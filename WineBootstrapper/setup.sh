#!/bin/bash
echo "Make sure you have wget and wine installed!"
sleep 3
mkdir /home/$USER/RobloxFreedomDistribution
mkdir /home/$USER/RobloxFreedomDistribution/settings
wget https://github.com/Windows81/Roblox-Freedom-Distribution/releases/download/2024-05-16T0741Z/RFD.exe -O /home/$USER/RobloxFreedomDistribution/RFD.exe
wget https://raw.githubusercontent.com/Windows81/Roblox-Freedom-Distribution/main/WineBootstrapper/joinnew.sh -O /home/$USER/RobloxFreedomDistribution/joinnew.sh
wget https://raw.githubusercontent.com/Windows81/Roblox-Freedom-Distribution/main/WineBootstrapper/hostnew.sh -O /home/$USER/RobloxFreedomDistribution/hostnew.sh
wget https://raw.githubusercontent.com/Windows81/Roblox-Freedom-Distribution/main/WineBootstrapper/GameConfig.toml -O /home/$USER/RobloxFreedomDistribution/GameConfig.toml
wget https://raw.githubusercontent.com/Windows81/Roblox-Freedom-Distribution/main/WineBootstrapper/winebin.txt -O /home/$USER/RobloxFreedomDistribution/settings/winebin.txt
mkdir /home/$USER/.wine/drive_c/robloxmaps
wget https://raw.githubusercontent.com/Vector4-new/RobloxFDLauncherLinux/main/maps/2007Crossroads.rbxl -O /home/$USER/.wine/drive_c/robloxmaps/2007Crossroads.rbxl
