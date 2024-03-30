# Packs Rōblox executables into GitHub releases that can be downloaded.
$release_name = $args[1] ?? (Get-Date -Format "yyyy-MM-ddTHH`u{a789}mmZ")
$root = "$PSScriptRoot"

$const = "$root/Source/util/const.py"
$const_txt = (Get-Content $const) -replace 'GIT_RELEASE_VERSION =.+', "GIT_RELEASE_VERSION = '''$release_name'''"
$const_txt | Set-Content $const

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

$zips = Get-ChildItem "$root/Roblox/*/*" -Directory | ForEach-Object {
	$zip = "$root/Roblox/$($_.Parent.Name).$($_.Name).7z"
	Remove-Item $zip* -Force
	7z a $zip $_.FullName
	return $zip
}

gh release create "$release_name" --notes "" $zips $bins -p