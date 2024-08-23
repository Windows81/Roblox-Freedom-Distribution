$mode = (Read-Host "@
1. Build EXE
2. Build EXE and publish artefacts
3. Build EXE and ZIP, then publish artefects
")

$root = "$PSScriptRoot"
$files = New-Object System.Collections.Generic.List[System.Object]

function RetrieveInput() {
	$script:release_name = (Read-Host "Version title?")
	# Packs Rōblox executables into GitHub releases that can be downloaded.
	$script:commit_name = $args[1] ?? (Get-Date -Format "yyyy-MM-ddTHHmmZ" (curl -I -s http://1.1.1.1 | grep "Date:" | cut -d " " -f 2-))
}


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
		--specpath "$root/PyInstallerWork/Spec"
	foreach ($file in (Get-ChildItem "$root/Binaries/*")) {
		$files.Add($file.FullName)
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

function ReleaseToGitHub() {
	gh release create "$release_name" --notes "" $files -p
}

switch ($mode) {
	'1' {
		CreateBinary
	}
	'2' {
		RetrieveInput
		UpdateAndPush
		CreateBinary
		ReleaseToGitHub
	}
	'3' {
		RetrieveInput
		UpdateZippedDirVersion
		UpdateAndPush
		CreateBinary
		CreateZippedDirs
		ReleaseToGitHub
	}
	Default {}
}