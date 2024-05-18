#!/bin/bash
echo "Make sure you have wget and wine installed!"
sleep 3
mkdir /home/$USER/RobloxFreedomDistribution
pushd /home/$USER/RobloxFreedomDistribution
mkdir settings
wget https://raw.githubusercontent.com/Windows81/Roblox-Freedom-Distribution/main/LinuxClient/joinnew.sh -O joinnew.sh
wget https://raw.githubusercontent.com/Windows81/Roblox-Freedom-Distribution/main/LinuxClient/hostnew.sh -O hostnew.sh
wget https://raw.githubusercontent.com/Windows81/Roblox-Freedom-Distribution/main/LinuxClient/winebin.txt -O settings/winebin.txt
wget https://github.com/Windows81/Roblox-Freedom-Distribution/releases/download/latest/RFD.exe -O RFD.exe
