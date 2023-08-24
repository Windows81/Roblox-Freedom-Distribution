pyinstaller `
	--name "rfd" `
	--onefile Source/_main.py `
	-p "./Source/" `
	--add-data "./Source/ssl/roblox.key;." `
	--add-data "./Source/ssl/cert.cert;." `
	--workpath "./PyInstallerWork" `
	--distpath "." `
	--clean `
	--icon "./Icon.ico"