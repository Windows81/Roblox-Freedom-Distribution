Here's how to play Roblox Freedom Distribution on GNU/Linux 🐧

(This guide assumes you have wget & [Wine](https://wiki.winehq.org/Download) 🍷 installed)

1.Run these commands
```
wget https://raw.githubusercontent.com/Windows81/Roblox-Freedom-Distribution/main/WineBootstrapper/setup.sh -O /tmp/setup.sh
chmod +x /tmp/setup.sh
/tmp/setup.sh
```

2.Run host.sh/join.sh depending on your use case
Host
```
/home/$USER/RobloxFreedomDistribution/host.sh
```

Join
```
/home/$USER/RobloxFreedomDistribution/join.sh
```

A common fix if you're having issues is to delete the "Roblox" folder
```
sudo rm -r /home/$USER/RobloxFreedomDistribution/Roblox
```
Using native wget/curl to download clients might fix issues too (not sure)

If you're having issues, please add me on discord. My discord is twig6843. (with the dot)
