$release_name = (Read-Host "Version title?")
$confirmation = (Read-Host "Save zipped files? (y?)") -eq "y"

# Packs Rōblox executables into GitHub releases that can be downloaded.
$commit_name = $args[1] ?? (Get-Date -Format "yyyy-MM-ddTHHmmZ" (curl -I -s http://1.1.1.1 | grep "Date:" | cut -d " " -f 2-))
$root = "$PSScriptRoot"
$files = New-Object System.Collections.Generic.List[System.Object]

function UpdateAndPush() {
	git add .
	git commit -m $commit_name
	git push
}

function CreateBinary() {
	pyinstaller `
		--name "RFD" `
		--onefile "$root/Source/_main.py" `
		-p "$root/Source/" `
		--workpath "$root/PyInstallerWork" `
		--distpath "$root/Binaries" `
		--icon "$root/Source/Icon.ico" `
		--specpath "$root/PyInstallerWork/Spec" `
		--exclude-module "tqdm.std" `
		--exclude-module "tqdm.gui"
	foreach ($file in (Get-ChildItem "$root/Binaries/*")) {
		$files.Add($file)
	}
}

function UpdateZippedDirVersion() {
	$const_file = "$root/Source/util/const.py"
	$const_txt = (Get-Content $const_file) -replace 'GIT_RELEASE_VERSION =.+', "GIT_RELEASE_VERSION = '''$release_name'''"
	$const_txt | Set-Content $const_file
}

function CreateZippedDirs() {
	foreach ($dir in (Get-ChildItem "$root/Roblox/*/*" -Directory)) {
		$zip = "$root/Roblox/$($dir.Parent.Name).$($dir.Name).7z"
		Remove-Item $zip -Force -Confirm
		if (-not (Test-Path $zip)) {
			# The `-xr` switches are for excluding specific file names (https://documentation.help/7-Zip-18.0/exclude.htm).
			7z a $zip "$($dir.FullName)/*" `
				"-xr!AppSettings.xml" `
				"-xr!RFDStarterScript.lua" `
				"-xr!dxgi.dll" "-xr!Reshade.ini" "-xr!ReShade.log" "-xr!ReShade_RobloxPlayerBeta.log" # ReShade stuff
		}
		$files.Add($zip)
	}
}

if (-not $confirmation) {
	UpdateAndPush
	CreateBinary
	gh release create "$release_name" --notes "" $files -p
	return
}

UpdateZippedDirVersion
UpdateAndPush
CreateBinary
CreateZippedDirs

gh release create "$release_name" --notes "" $files -p