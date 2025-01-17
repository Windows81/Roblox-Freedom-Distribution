# Prompt user to select build mode
$mode = (Read-Host @"
1. Update version string
2. Update version string then create new commit
3. Zip binaries and add them to a new version in GitHub Releases


"@)

# Defines root directory.
$root = "$PSScriptRoot/.."
# Initialize list of files to include in release
$files = New-Object System.Collections.Generic.List[System.Object]

# Retrieves user input for version title and commit message.
function RetrieveInput($suffix = '') {
	$script:release_name = (Read-Host "Version title?") + $suffix
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
function UpdateConstReleaseVersion($labels) {
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

		# The users confirms whether to remove each zipped archive.
		Remove-Item $zip -Force -Confirm -ErrorAction Ignore

		if (Test-Path $zip) {
			$files.Add($zip)
			return
		}

		# Writes to the version-flag file.
		$script:release_name | Set-Content "$($dir.FullName)/rfd_version"

		# The `-xr` switches are for excluding specific file names (https://documentation.help/7-Zip-18.0/exclude.htm).
		7z a $zip "$($dir.FullName)/*" `
			"-xr!dxgi.dll" "-xr!Reshade.ini" "-xr!ReShade.log" "-xr!ReShade_RobloxPlayerBeta.log" `
			"-xr!AppSettings.xml" `
			"-xr!RFDStarterScript.lua" `
			"-xr!cacert.pem"

		$files.Add($zip)
	}
}

# Creates a GitHub release with specified files.
function ReleaseToGitHub() {
	gh release create "${release_name}" --title "${release_name} Binaries" --notes "" $files
}

# Executes selected build mode.
switch ($mode) {
	'1' {
		RetrieveInput
		UpdateConstReleaseVersion @("GIT_RELEASE_VERSION")
	}
	'2' {
		RetrieveInput
		UpdateConstReleaseVersion @("GIT_RELEASE_VERSION")
		UpdateAndPush
	}
	'3' {
		RetrieveInput "-binaries"
		UpdateConstReleaseVersion @("ZIPPED_RELEASE_VERSION")
		CreateZippedDirs
		UpdateAndPush
		ReleaseToGitHub
	}
	Default {}
}