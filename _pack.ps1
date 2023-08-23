# Packs Rōblox executables into GitHub releases that can be downloaded.

$release_name = Get-Date -Format "yyyy-MM-ddTHH`u{a789}mmZ"
$root = "$PSScriptRoot/Roblox"
$zips = Get-ChildItem "$root/*/*" -Directory | ForEach-Object {

	$zip = "$root/$($_.Parent.Name).$($_.Name).7z"

	# Do not overwrite.
	if (-not (Test-Path $zip*)) {
		Remove-Item $zip* -Force
		7z a $zip $_.FullName
	}
	return Get-ChildItem $zip*
}

gh release create "$release_name" --notes "" $zips