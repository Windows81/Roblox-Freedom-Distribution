$date = Get-Date -Format "yyyy-MM-ddTHH`u{a789}mmZ"
$root = "$PSScriptRoot/Roblox"
$dirs = Get-ChildItem "$root/*/*" -Directory

$zips = $dirs | ForEach-Object {
	$zip = "$root/$($_.Parent.Name).$($_.Name).7z"
	Remove-Item $zip* -Force
	7z a $zip $_.FullName
	return Get-ChildItem $zip*
}

gh release create "$date" --notes "" $zips