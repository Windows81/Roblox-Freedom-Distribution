pushd "%~dp0"
set ip=localhost
set port=2005
set "app=rbxassetid://6445262286;rbxassetid://2510230574;rbxassetid://2510233257;rbxassetid://2510236649;rbxassetid://2510238627;rbxassetid://6969309778;rbxassetid://2846257298;rbxassetid://6340101;rbxassetid://34247191;rbxassetid://48474294;rbxassetid://107458429;rbxassetid://121390054;rbxassetid://154386348;rbxassetid://183808364;rbxassetid://190245296;rbxassetid://192483960;rbxassetid://201733574;rbxassetid://261826995;rbxassetid://9120251003;rbxassetid://9481782649;rbxassetid://9482991343;rbxassetid://5731052645;rbxassetid://10726856854;password=1630228^|Cyan;Cyan;Cyan;Cyan;Cyan;Cyan"
set j=http://localhost/game/placelauncher.ashx?year=2018^&placeid=1818^&ip=%ip%^&port=%port%^&id=1630228^&app=%app%^&user=VisualPlugin
Versions\2018M\Player\RobloxPlayerBeta.exe -a "http://localhost/login/negotiate.ashx" -j "%j%" -t "1"
popd