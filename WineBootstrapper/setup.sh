#!/bin/bash

#This uses an older version with wine (the latest RFD.exe seems to not work with wine. We're working on getting the latest version to work with wine.)

mkdir /home/$USER/RobloxFreedomDistribution
mkdir /home/$USER/RobloxFreedomDistribution/settings
wget https://github.com/Windows81/Roblox-Freedom-Distribution/releases/download/2024-05-16T0741Z/RFD.exe -O /home/$USER/RobloxFreedomDistribution/RFD.exe
wget https://raw.githubusercontent.com/Windows81/Roblox-Freedom-Distribution/main/WineBootstrapper/join.sh -O /home/"$USER"/RobloxFreedomDistribution/join.sh
wget https://raw.githubusercontent.com/Windows81/Roblox-Freedom-Distribution/main/WineBootstrapper/host.sh -O /home/"$USER"/RobloxFreedomDistribution/host.sh
wget https://raw.githubusercontent.com/Windows81/Roblox-Freedom-Distribution/main/WineBootstrapper/stop-all.sh -O /home/"$USER"/RobloxFreedomDistribution/stop-all.sh
wget https://raw.githubusercontent.com/Windows81/Roblox-Freedom-Distribution/main/WineBootstrapper/GameConfig.toml -O /home/"$USER"/RobloxFreedomDistribution/GameConfig.toml
wget https://raw.githubusercontent.com/Windows81/Roblox-Freedom-Distribution/main/WineBootstrapper/winebin.txt -O /home/"$USER"/RobloxFreedomDistribution/settings/winebin.txt
mkdir /home/$USER/.wine/drive_c/robloxmaps
wget https://raw.githubusercontent.com/Vector4-new/RobloxFDLauncherLinux/main/maps/2007Crossroads.rbxl -O /home/"$USER"/.wine/drive_c/robloxmaps/2007Crossroads.rbxl

chmod +x /home/$USER/RobloxFreedomDistribution/join.sh
chmod +x /home/$USER/RobloxFreedomDistribution/host.sh
chmod +x /home/$USER/RobloxFreedomDistribution/stop-all.sh
echo "Roblox freedom distribution is now installed!"
sleep 5
