$root = "$PSScriptRoot/.."

pyinstaller `
	--name "RFD" `
	--onefile "$root/Source/_main.py" `
	--paths "$root/Source/" `
	--workpath "$root/PyInstallerWork" `
	--distpath "$root" `
	--icon "$root/Source/Icon.ico" `
	--specpath "$root/PyInstallerWork/Spec" `
	--add-data "$root/Source/*:./Source" `
	--hidden-import requests `
	--hidden-import dracopy