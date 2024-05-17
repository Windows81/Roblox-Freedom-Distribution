#Version 1.00
echo "Make sure you have wget,git and wine installed!"
mkdir /home/$USER/RobloxFreedomDistribution
mkdir /home/$USER/RobloxFreedomDistribution/settings
wget https://raw.githubusercontent.com/Windows81/Roblox-Freedom-Distribution/main/LinuxClient/winebin.txt -O /home/$USER/RobloxFreedomDistribution/settings/winebin.txt
wget https://github.com/Windows81/Roblox-Freedom-Distribution/releases/download/2024-05-16T0741Z/RFD.exe -O /home/$USER/RobloxFreedomDistribution/RFD.exe
