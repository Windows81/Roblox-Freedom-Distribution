pyinstaller `
	--name "rfd" `
	--onefile Source/_main.py `
	-p "./Source/" `
	--add-data "./Source/ssl/*;." `
	--workpath "./PyInstallerWork" `
	--distpath "." `
	--clean `
	--icon "./Icon.ico"