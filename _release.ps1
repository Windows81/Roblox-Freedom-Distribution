$confirmation = (Read-Host "Save zipped files? (y?)") -eq "y"

# Packs Rōblox executables into GitHub releases that can be downloaded.
$release_name = $args[1] ?? (Get-Date -Format "yyyy-MM-ddTHHmmZ" (curl -I -s http://1.1.1.1 | grep "Date:" | cut -d " " -f 2-))
$root = "$PSScriptRoot"

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
		--icon "$root/Source/Icon.ico"
	$bins = Get-ChildItem "$root/Binaries/*"
	return $bins
}

function UpdateZippedDirVersion() {
	$const_file = "$root/Source/util/const.py"
	$const_txt = (Get-Content $const_file) -replace 'GIT_RELEASE_VERSION =.+', "GIT_RELEASE_VERSION = '''$release_name'''"
	$const_txt | Set-Content $const_file
}

function CreateZippedDirs() {
	$zips = New-Object System.Collections.Generic.List[System.Object]
	Get-ChildItem "$root/Roblox/*/*" -Directory | ForEach-Object {
		$zip = "$root/Roblox/$($_.Parent.Name).$($_.Name).7z"
		Remove-Item $zip -Force -Confirm
		if (-not (Test-Path $zip)) { 7z a $zip "$($_.FullName)/*" }
		$zips.Add($zip)
	}
	return $zips
}

if (-not $confirmation) {
	UpdateAndPush
	$bins = CreateBinary
	gh release create "$release_name" --notes "" $bins -p
	return
}

UpdateZippedDirVersion
UpdateAndPush
$bins = CreateBinary
$zips = CreateZippedDirs
gh release create "$release_name" --notes "" $bins $zips -p