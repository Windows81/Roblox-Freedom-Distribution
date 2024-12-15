To launch Freedom Distribution, your command line will look something like this:

```
wine RFD.exe player -h 127.0.0.1 -p 2005
```

If you're going to use a wine manager like heroic/lutris/bottles

1.Initialize a wineprefix

2.Apply the [cover art](https://github.com/Windows81/Roblox-Freedom-Distribution/blob/main/Cover.png?raw=true)

3.Put [RFD.exe](https://github.com/Windows81/Roblox-Freedom-Distribution/releases/latest/download/RFD.exe) (the config & map files also go here if you're going to host) to `drive_c/windows/system32`

4.Pick `drive_c\windows\system32\cmd.exe` as the game executable

5. Put these as game launch options `/C start RFD.exe`

6.Press play and then it should work

(This is a dirty workaround to make sure Freedom distribution launches its own cmd window)
