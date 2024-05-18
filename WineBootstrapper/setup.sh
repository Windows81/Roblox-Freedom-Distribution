#!/bin/bash
echo "Make sure you have wget and wine installed!"
sleep 3
mkdir /home/$USER/RobloxFreedomDistribution
mkdir /home/$USER/RobloxFreedomDistribution/settings
wget https://github.com/Windows81/Roblox-Freedom-Distribution/releases/download/latest/RFD.exe -O /home/$USER/RobloxFreedomDistribution/RFD.exe
wget https://raw.githubusercontent.com/Windows81/Roblox-Freedom-Distribution/main/LinuxClient/joinnew.sh -O /home/$USER/RobloxFreedomDistribution/joinnew.sh
wget https://raw.githubusercontent.com/Windows81/Roblox-Freedom-Distribution/main/LinuxClient/hostnew.sh -O /home/$USER/RobloxFreedomDistribution/hostnew.sh
wget https://raw.githubusercontent.com/Windows81/Roblox-Freedom-Distribution/main/GameConfig.toml -O /home/$USER/RobloxFreedomDistribution/GameConfig.toml
wget https://raw.githubusercontent.com/Windows81/Roblox-Freedom-Distribution/main/LinuxClient/winebin.txt -O /home/$USER/RobloxFreedomDistribution/settings/winebin.txt
mkdir /home/$USER/.wine/drive_c/robloxmaps
wget https://raw.githubusercontent.com/Vector4-new/RobloxFDLauncherLinux/main/maps/2007Crossroads.rbxl -O /home/$USER/.wine/drive_c/robloxmaps/2007Crossroads.rbxl
