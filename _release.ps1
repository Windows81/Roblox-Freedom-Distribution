# Packs Rōblox executables into GitHub releases that can be downloaded.
$release_name = $args[1] ?? (Get-Date -Format "yyyy-MM-ddTHHmmZ")
$root = "$PSScriptRoot"

# Not needed, script automatically pulls.
# $const = "$root/Source/util/const.py"
# $const_txt = (Get-Content $const) -replace 'GIT_RELEASE_VERSION =.+', "GIT_RELEASE_VERSION = '''$release_name'''"
# $const_txt | Set-Content $const

git add .
git commit -m $release_name
git push

pyinstaller `
	--name "RFD" `
	--onefile "$root/Source/_main.py" `
	-p "$root/Source/" `
	--workpath "$root/PyInstallerWork" `
	--distpath "$root/Binaries" `
	--icon "$root/Source/Icon.ico"
$bins = Get-ChildItem "$root/Binaries/*"

$zips = New-Object System.Collections.Generic.List[System.Object]
Get-ChildItem "$root/Roblox/*/*" -Directory | ForEach-Object {
	$zip = "$root/Roblox/$($_.Parent.Name).$($_.Name).7z"
	Remove-Item $zip -Force -Confirm
	if (-not (Test-Path $zip)) { 7z a $zip "$($_.FullName)/*" }
	$zips.Add($zip)
}

gh release create "$release_name" --notes "" $bins $zips -p