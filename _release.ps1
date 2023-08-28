# Packs Rōblox executables into GitHub releases that can be downloaded.
$release_name = Get-Date -Format "yyyy-MM-ddTHH`u{a789}mmZ"
$root = "$PSScriptRoot/Roblox"

pyinstaller `
	--name "RFD" `
	--onefile Source/_main.py `
	-p "./Source/" `
	--workpath "./PyInstallerWork" `
	--distpath "./Binaries" `
	--clean `
	--icon "./Source/Icon.ico"
$bins = Get-ChildItem "./Binaries/*"

$zips = Get-ChildItem "$root/*/*" -Directory | ForEach-Object {
	return "$root/$($_.Parent.Name).$($_.Name).7z"
}

$zips | ForEach-Object {
	Remove-Item $zip* -Force
	7z a $zip $_.FullName
}

$new_zips = $zips | ForEach-Object {
	Get-ChildItem $zip*
}

gh release create "$release_name" --notes "" $new_zips $bins