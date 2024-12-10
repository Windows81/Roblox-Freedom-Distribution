# Prompt user to select build mode
$mode = (Read-Host @"
1. Build EXE
2. Build EXE and publish artefacts
3. Build EXE and ZIP, then publish artefacts
"@)

# Defines root directory.
$root = "$PSScriptRoot"
# Initialize list of files to include in release
$files = New-Object System.Collections.Generic.List[System.Object]

# Retrieves user input for version title and commit message.
function RetrieveInput() {
	$script:release_name = (Read-Host "Version title?")
	# Packs Rōblox executables into GitHub releases that can be downloaded.
	$script:commit_name = $args[1] ?? (Get-Date -Format "yyyy-MM-ddTHHmmZ" `
		(curl -I -s http://1.1.1.1 | grep "Date:" | cut -d " " -f 2-))
}

# Adds changes to git repository and push.
function UpdateAndPush() {
	git add .
	git commit -m $script:commit_name
	git push
}

# Builds RFD.exe using PyInstaller.
function CreateBinary() {
	pyinstaller `
		--name "RFD" `
		--onefile "$root/Source/_main.py" `
		--paths "$root/Source/" `
		--workpath "$root/PyInstallerWork" `
		--distpath "$root" `
		--icon "$root/Source/Icon.ico" `
		--specpath "$root/PyInstallerWork/Spec" `
		--add-data "$root/Source/*:./Source" `
		--hidden-import requests # Allows functions in config to use the `requests` library (1 MiB addition).

	$files.Add("$root/RFD.exe")
}

# Updates version number in const.py file.
function UpdateZippedReleaseVersion($labels) {
	$const_file = "$root/Source/util/const.py"
	$const_txt = (Get-Content $const_file) | ForEach-Object {
		$r = $_
		foreach ($label in $labels) {
			$r = $r -replace "$label =.+", "$label = '''$script:release_name'''"
		}
		return $r
	}
	$const_txt | Set-Content $const_file
}

# Creates zipped directories for Roblox files.
function CreateZippedDirs() {
	foreach ($dir in (Get-ChildItem "$root/Roblox/*/*" -Directory)) {
		$zip = "$root/Roblox/$($dir.Parent.Name).$($dir.Name).7z"
		Remove-Item $zip -Force -Confirm
		if (-not (Test-Path $zip)) {
			# The `-xr` switches are for excluding specific file names (https://documentation.help/7-Zip-18.0/exclude.htm).
			7z a $zip "$($dir.FullName)/*" `
				"-xr!AppSettings.xml" `
				"-xr!RFDStarterScript.lua" `
				"-xr!cacert.pem" `
				"-xr!dxgi.dll" "-xr!Reshade.ini" "-xr!ReShade.log" "-xr!ReShade_RobloxPlayerBeta.log" # ReShade stuff
		}
		$files.Add($zip)
	}
}

# Creates a GitHub release with specified files.
function ReleaseToGitHub() {
	gh release create "$release_name" --notes "" $files
}

# Executes selected build mode.
switch ($mode) {
	'1' {
		CreateBinary
	}
	'2' {
		RetrieveInput
		UpdateZippedReleaseVersion @("GIT_RELEASE_VERSION")
		UpdateAndPush
		CreateBinary
		ReleaseToGitHub
	}
	'3' {
		RetrieveInput
		UpdateZippedReleaseVersion @("GIT_RELEASE_VERSION", "ZIPPED_RELEASE_VERSION")
		UpdateAndPush
		CreateBinary
		CreateZippedDirs
		ReleaseToGitHub
	}
	Default {}
}