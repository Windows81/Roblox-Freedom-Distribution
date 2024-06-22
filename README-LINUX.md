Here's how to play Roblox Freedom Distribution on GNU/Linux 🐧

(This guide assumes you have wget,jq & [The latest Wine version](https://wiki.winehq.org/Download) 🍷 installed)
(All of the commands in this readme file reference the default install directory.)

1.Run these commands 
```
cd
sudo rm /tmp/setup.sh
sudo rm -r /home/$USER/RobloxFreedomDistribution
wget https://raw.githubusercontent.com/Windows81/Roblox-Freedom-Distribution/main/WineBootstrapper/setup.sh -O /tmp/setup.sh
chmod +x /tmp/setup.sh
/tmp/setup.sh
```

2.Run host.sh/join.sh depending on your use case (or just search for FreedomDistribution in your start menu)

Host
```
/home/$USER/RobloxFreedomDistribution/host.sh
```

Join
```
/home/$USER/RobloxFreedomDistribution/join.sh
```


### Known issues ❗❗❗
1.RFD.exe failing to download the clients. A common fix for this is to remove your "Roblox" folder.
```
sudo rm -r /home/$USER/RobloxFreedomDistribution/Roblox
```
Using native wget/curl to download clients might fix the said issue too (not sure)

2.Freedom distribution not launching on window managers through the .desktop shortcut
If you're using a window manager do the following to fix this isse
```
nano /home/$USER/.local/share/applications/FreedomDistribution.desktop
```
Add "kitty" to the exec part it should look like this in the end
```
Exec=kitty /home/twig/RobloxFreedomDistribution/menu.sh
```


If you're having issues, please add me on discord. My discord is twig6843. (with the dot)
