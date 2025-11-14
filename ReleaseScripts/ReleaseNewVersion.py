import shutil
import sys
import requests
import subprocess
from pathlib import Path
from datetime import datetime, timezone
import re
import os

# --- Global Variables ---
required_apps = ["gh", "7z", "git"]
# Defines root directory. $PSScriptRoot/..
root = Path(__file__).resolve().parent.parent

# Initialize list of files to include in release
files = []

release_name = None
release_name_suffixed = None
commit_name = None

# --- Utility Functions ---

def retrieve_input(suffix=''):
    """Retrieves user input for version title and commit message."""
    global release_name, release_name_suffixed, commit_name

    release_name = input("Version title? ")
    release_name_suffixed = release_name + suffix

    # Get the date from the 1.1.1.1 header (similar to curl -I -s http://1.1.1.1 | grep "Date:" | cut -d " " -f 2-)
    # Fallback to the current time if the request fails or 'Date' header is missing
    try:
        response = requests.head("http://1.1.1.1", timeout=5)
        date_header = response.headers.get('Date')
        if date_header:
            # Parse the RFC 1123 date string
            date_obj = datetime.strptime(date_header, '%a, %d %b %Y %H:%M:%S %Z')
            # Format to ISO 8601, ensuring it's in UTC (Z) format
            commit_name = date_obj.strftime("%Y-%m-%dT%H%M%SZ")
        else:
            commit_name = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    except requests.RequestException:
        # If request fails, use the current UTC time
        commit_name = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")

def update_and_push():
    """Adds changes to git repository and push."""
    print(f"Committing with message: '{commit_name}'")
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", commit_name], check=True)
        subprocess.run(["git", "push"], check=True)
        print("Git push successful.")
    except subprocess.CalledProcessError as e:
        print(f"Error during git operation: {e}")
        sys.exit(1)

def update_const_release_version(labels, add_suffix=False):
    """Updates version number in const.py file."""
    if release_name is None:
        print("Error: release_name is not set. Run retrieve_input first.")
        sys.exit(1)

    const_file = root / "Source" / "util" / "const.py"
    label_value = release_name_suffixed if add_suffix else release_name

    try:
        with open(const_file, 'r') as f:
            content = f.read()

        new_content = content
        for label in labels:
            # Regex to find the label assignment and replace its value.
            # Handles single or double quotes, and preserves surrounding text.
            pattern = re.compile(rf"{label}\s*=\s*['\"].*?['\"]")
            replacement = f"{label} = '''{label_value}'''"
            new_content = pattern.sub(replacement, new_content)

        if new_content != content:
            with open(const_file, 'w') as f:
                f.write(new_content)
            print(f"Updated {', '.join(labels)} in {const_file.name} to '{label_value}'.")
        else:
            print(f"Warning: Did not find/update {', '.join(labels)} in {const_file.name}.")

    except FileNotFoundError:
        print(f"Error: const file not found at {const_file}")
        sys.exit(1)
    except Exception as e:
        print(f"Error updating const file: {e}")
        sys.exit(1)


def create_zipped_dirs():
    """Creates zipped directories for Roblox files using 7z."""
    roblox_dir = root / "Roblox"
    
    # Exclusions list for 7z
    exclusions = [
        "-xr!RFDStarterScript.lua",
        "-x!_*.exe",  # Temporary EXE files
        "-xr!dxgi.dll", "-xr!_dxgi.dll", "-xr!Reshade.ini", "-xr!ReShade.log", "-xr!ReShade_RobloxPlayerBeta.log", # Reshade
        "-xr!AppSettings.xml", "-xr!GlobalBasicSettings_13.xml", "-xr!AnalysticsSettings.xml", "-xr!LocalStorage", "-xr!minidump", "-xr!logs", # Rōblox-specific files
        "-xr!*.id1", "-xr!*.i32", "-xr!*.i64", # IDA debug files
        "-xr!*.dd32", "-xr!*.dd64", "-xr!*.1337", # x96dbg debug files
        "-x!*.bak",
    ]

    for dir_path in roblox_dir.glob("*/*"):
        if dir_path.is_dir():
            zip_name = f"{dir_path.parent.name}.{dir_path.name}.7z"
            zip_path = roblox_dir / zip_name

            # Always overwrites the file.
            if zip_path.exists():
                print(f"Removing existing file: {zip_path.name}")
                os.remove(zip_path)

            # Writes to the version-flag file.
            version_flag_path = dir_path / "rfd_version"
            try:
                with open(version_flag_path, 'w') as f:
                    f.write(release_name_suffixed)
                print(f"Wrote version flag to: {version_flag_path.name}")
            except Exception as e:
                print(f"Error writing version flag: {e}")
                continue

            # 7z command construction
            # 7z a $zip "$($dir.FullName)/*" @(...)
            command = ["7z", "a", str(zip_path), str(dir_path / "*")] + exclusions
            
            print(f"Creating zip: {zip_path.name}...")
            try:
                # Run the 7z command
                subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                files.append(str(zip_path))
                print(f"Successfully created: {zip_path.name}")
            except subprocess.CalledProcessError as e:
                print(f"Error creating 7z archive for {dir_path.name}:")
                print(f"Stdout: {e.stdout.decode()}")
                print(f"Stderr: {e.stderr.decode()}")
                sys.exit(1)

def mark_latest_version():
    """Marks the most recent release on GitHub as the latest."""
    print("Marking the most recent release as latest...")
    try:
        # Get the latest tag name
        result = subprocess.run(
            ["gh", "release", "list", "--json", "tagName", "--template", '{{index . 0 "tagName"}}', "--limit", "1"],
            check=True,
            capture_output=True,
            text=True
        )
        latest_tag = result.stdout.strip()
        
        if latest_tag:
            # Edit the release to mark it as latest
            subprocess.run(["gh", "release", "edit", latest_tag, "--latest"], check=True)
            print(f"Marked release '{latest_tag}' as latest.")
        else:
            print("Warning: Could not find any existing releases to mark as latest.")

    except subprocess.CalledProcessError as e:
        print(f"Error during GitHub release latest operation: {e}")
        print(f"Stderr: {e.stderr.decode()}")
        sys.exit(1)


def release_to_github():
    """Creates a GitHub release with specified files."""
    if not release_name_suffixed:
        print("Error: release_name_suffixed is not set.")
        sys.exit(1)
        
    print(f"Creating GitHub release '{release_name_suffixed}' with {len(files)} files...")
    
    # gh release create $script:release_name_suffixed $files --prerelease --generate-notes
    command = ["gh", "release", "create", release_name_suffixed] + files + ["--prerelease", "--generate-notes"]
    
    try:
        subprocess.run(command, check=True)
        print("GitHub release successful.")
    except subprocess.CalledProcessError as e:
        print(f"Error during GitHub release creation: {e}")
        print(f"Stderr: {e.stderr.decode()}")
        sys.exit(1)


def check_requirements():
    """Checks if the appropriate software is installed."""
    for app in required_apps:
        if shutil.which(app) is None:
            print(f"You need to install `{app}`!")
            # Stop the script if a requirement is missing
            sys.exit(1)

# --- Main Execution ---

def main():
    """Prompts user for mode and executes the selected action."""
    check_requirements()

    mode = None
    while mode not in ('1', '2', '3', '4'):
        mode = input(
f"""
1. Update version string
2. Update version string then create new commit
3. Create new commit only
4. Zip binaries and add them to a new version in GitHub Releases

Select mode (1, 2, 3 or 4): """
        ).strip()
    
    print("-" * 30)

    if mode == '1':
        # 1. Update version string
        retrieve_input()
        update_const_release_version(["GIT_RELEASE_VERSION"], False)
        mark_latest_version()
    elif mode == '2':
        # 2. Update version string then create new commit
        retrieve_input()
        update_const_release_version(["GIT_RELEASE_VERSION"], False)
        update_and_push()

    elif mode == '3':
        update_and_push()

    elif mode == '4':
        # 3. Zip binaries and add them to a new version in GitHub Releases
        retrieve_input("-binaries")
        update_const_release_version(["GIT_RELEASE_VERSION"], False)
        update_const_release_version(["ZIPPED_RELEASE_VERSION"], True)
        create_zipped_dirs()
        update_and_push()
        release_to_github()
    else:
        print("Invalid mode selected. Exiting.")


if __name__ == "__main__":
    main()
