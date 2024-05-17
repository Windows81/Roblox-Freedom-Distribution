#Version 1.00
echo "Make sure you have wget and wine installed!"
sleep 3
mkdir /home/$USER/RobloxFreedomDistribution
mkdir /home/$USER/RobloxFreedomDistribution/settings
wget https://raw.githubusercontent.com/Windows81/Roblox-Freedom-Distribution/main/LinuxClient/joinnew.sh -O /home/$USER/RobloxFreedomDistribution
wget https://raw.githubusercontent.com/Windows81/Roblox-Freedom-Distribution/main/LinuxClient/winebin.txt -O /home/$USER/RobloxFreedomDistribution/settings/winebin.txt
wget https://github.com/Windows81/Roblox-Freedom-Distribution/releases/download/2024-05-16T0741Z/RFD.exe -O /home/$USER/RobloxFreedomDistribution/RFD.exe
