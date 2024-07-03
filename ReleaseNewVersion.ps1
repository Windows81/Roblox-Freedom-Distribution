$confirmation = (Read-Host "Save zipped files? (y?)") -eq "y"

# Packs Rōblox executables into GitHub releases that can be downloaded.
$release_name = $args[1] ?? (Get-Date -Format "yyyy-MM-ddTHHmmZ" (curl -I -s http://1.1.1.1 | grep "Date:" | cut -d " " -f 2-))
$root = "$PSScriptRoot"
$files = New-Object System.Collections.Generic.List[System.Object]

function UpdateAndPush() {
	git add .
	git commit -m $release_name
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
	foreach ($_ in (Get-ChildItem "$root/Binaries/*")) {
		$files.Add($_)
	}
}

function UpdateZippedDirVersion() {
	$const_file = "$root/Source/util/const.py"
	$const_txt = (Get-Content $const_file) -replace 'GIT_RELEASE_VERSION =.+', "GIT_RELEASE_VERSION = '''$release_name'''"
	$const_txt | Set-Content $const_file
}

function CreateZippedDirs() {
	foreach ($_ in (Get-ChildItem "$root/Roblox/*/*" -Directory)) {
		$zip = "$root/Roblox/$($_.Parent.Name).$($_.Name).7z"
		Remove-Item $zip -Force -Confirm
		if (-not (Test-Path $zip)) { 7z a $zip "$($_.FullName)/*" }
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