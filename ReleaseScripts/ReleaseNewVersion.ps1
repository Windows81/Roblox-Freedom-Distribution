# Checks if the appropriate software is installed.
foreach ($e in @("gh", "7z")) {
	if ($null -eq (Get-Command "$e.exe" -ErrorAction SilentlyContinue)) {
		Write-Output "You need to install ``$e``!"
		return
	}
}

# Defines root directory.
$root = "$PSScriptRoot/.."
# Initialize list of files to include in release
$files = New-Object System.Collections.Generic.List[System.Object]

# Retrieves user input for version title and commit message.
function RetrieveInput($suffix = '') {
	$script:release_name = (Read-Host "Version title?")
	$script:release_name_suffixed = $script:release_name + $suffix
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

# Updates version number in const.py file.
function UpdateConstReleaseVersion($labels, [bool]$add_suffix = $false) {
	$const_file = "$root/Source/util/const.py"
	$label_value = $add_suffix ? $script:release_name_suffixed : $script:release_name
	$const_txt = (Get-Content $const_file) | ForEach-Object {
		$r = $_
		foreach ($label in $labels) {
			$r = $r -replace "$label =.+", "$label = '''$label_value'''"
		}
		return $r
	}
	$const_txt | Set-Content $const_file
}

# Creates zipped directories for Roblox files.
function CreateZippedDirs() {
	foreach ($dir in (Get-ChildItem "$root/Roblox/*/*" -Directory)) {
		$zip = "$root/Roblox/$($dir.Parent.Name).$($dir.Name).7z"

		# Always overwrites the file.
		Remove-Item $zip -Force -ErrorAction Ignore

		# Writes to the version-flag file.
		$script:release_name_suffixed | Set-Content "$($dir.FullName)/rfd_version"

		# The `-xr` switches are for excluding specific file names (https://documentation.help/7-Zip-18.0/exclude.htm).
		7z a $zip "$($dir.FullName)/*" `
			"-xr!RFDStarterScript.lua" `
			"-xr!dxgi.dll" "-xr!_dxgi.dll" "-xr!Reshade.ini" "-xr!ReShade.log" "-xr!ReShade_RobloxPlayerBeta.log" `
			`
			"-xr!AppSettings.xml" `
			"-xr!GlobalBasicSettings_13.xml" `
			"-xr!AnalysticsSettings.xml" `
			"-xr!LocalStorage" `
			"-xr!logs" `
			`
			"-xr!*.id1" `
			"-xr!*.i32" "-xr!*.i64" `
			"-x!_*.exe"

		$files.Add($zip)
	}
}

# Marks the most recent release on GitHub as the latest.
function MarkLatestVersion() {
	$latest = (gh release list --json tagName --template '{{range .}}{{.tagName}}{{end}}' --limit 1)
	gh release edit $latest --latest
}

# Creates a GitHub release with specified files.
function ReleaseToGitHub() {
	gh release create $script:release_name_suffixed $files --prerelease --generate-notes
}

# Prompts user to select build mode.
$mode = (Read-Host @"
1. Update version string
2. Update version string then create new commit
3. Zip binaries and add them to a new version in GitHub Releases


"@)

# Executes selected build mode.
switch ($mode) {
	'1' {
		RetrieveInput
		UpdateConstReleaseVersion @("GIT_RELEASE_VERSION") $false
		MarkLatestVersion
	}
	'2' {
		RetrieveInput
		UpdateConstReleaseVersion @("GIT_RELEASE_VERSION") $false
		UpdateAndPush
	}
	'3' {
		RetrieveInput "-binaries"
		UpdateConstReleaseVersion @("GIT_RELEASE_VERSION") $false
		UpdateConstReleaseVersion @("ZIPPED_RELEASE_VERSION") $true
		CreateZippedDirs
		UpdateAndPush
		ReleaseToGitHub
	}
	Default {}
}