import os
import subprocess
import datetime
import requests
import shutil
from pathlib import Path

# Checks if the appropriate software is installed.
for e in ["gh", "7z"]:
    if not shutil.which(f"{e}.exe"):
        print(f"You need to install `{e}`!")
        exit()

# Defines root directory.
root = Path(__file__).parent.parent

# Initialize list of files to include in release
files = []

# Global variables to hold release and commit names
release_name = None
release_name_suffixed = None
commit_name = None

def retrieve_input(suffix=''):
    global release_name, release_name_suffixed, commit_name
    release_name = input("Version title? ")
    release_name_suffixed = release_name + suffix

    # Get date from HTTP header or fallback to local date
    try:
        r = requests.head("http://1.1.1.1")
        date_str = r.headers.get("Date")
        if date_str:
            dt = datetime.datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %Z")
            commit_name = dt.strftime("%Y-%m-%dT%H%MZ")
        else:
            commit_name = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H%MZ")
    except Exception:
        commit_name = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H%MZ")

def update_and_push():
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", commit_name], check=True)
    subprocess.run(["git", "push"], check=True)

def update_const_release_version(labels, add_suffix=False):
    const_file = root / "Source" / "util" / "const.py"
    label_value = release_name_suffixed if add_suffix else release_name

    with open(const_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        for label in labels:
            if line.strip().startswith(f"{label} ="):
                line = f"{label} = '''{label_value}'''\n"
        new_lines.append(line)

    with open(const_file, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

def create_zipped_dirs():
    global files
    roblox_path = root / "Roblox"
    for dir_path in roblox_path.glob("*/*"):
        if dir_path.is_dir():
            zip_path = root / "Roblox" / f"{dir_path.parent.name}.{dir_path.name}.7z"

            # Always overwrites the file.
            if zip_path.exists():
                zip_path.unlink()

            # Writes to the version-flag file.
            version_flag_file = dir_path / "rfd_version"
            version_flag_file.write_text(release_name_suffixed, encoding="utf-8")

            exclude_args = [
                "-xr!RFDStarterScript.lua",
                "-x!_*.exe",
                "-xr!dxgi.dll",
                "-xr!_dxgi.dll",
                "-xr!Reshade.ini",
                "-xr!ReShade.log",
                "-xr!ReShade_RobloxPlayerBeta.log",
                "-xr!AppSettings.xml",
                "-xr!GlobalBasicSettings_13.xml",
                "-xr!AnalysticsSettings.xml",
                "-xr!LocalStorage",
                "-xr!minidump",
                "-xr!logs",
                "-xr!*.id1", "-xr!*.i32", "-xr!*.i64",
                "-xr!*.dd32", "-xr!*.dd64",
                "-xr!*.1337",
                "-x!*.bak"
            ]

            cmd = ["7z", "a", str(zip_path), f"{dir_path}/*"] + exclude_args
            subprocess.run(cmd, check=True)

            files.append(str(zip_path))

def mark_latest_version():
    result = subprocess.run(
        ["gh", "release", "list", "--json", "tagName", "--template", "{{range .}}{{.tagName}}{{end}}", "--limit", "1"],
        capture_output=True, text=True, check=True
    )
    latest = result.stdout.strip()
    if latest:
        subprocess.run(["gh", "release", "edit", latest, "--latest"], check=True)

def release_to_github():
    subprocess.run(["gh", "release", "create", release_name_suffixed, *files, "--prerelease", "--generate-notes"], check=True)

# Prompts user to select build mode.
mode = input("""
1. Update version string
2. Update version string then create new commit
3. Zip binaries and add them to a new version in GitHub Releases

""")

# Executes selected build mode.
if mode == '1':
    retrieve_input()
    update_const_release_version(["GIT_RELEASE_VERSION"], False)
    mark_latest_version()
elif mode == '2':
    retrieve_input()
    update_const_release_version(["GIT_RELEASE_VERSION"], False)
    update_and_push()
elif mode == '3':
    retrieve_input("-binaries")
    update_const_release_version(["GIT_RELEASE_VERSION"], False)
    update_const_release_version(["ZIPPED_RELEASE_VERSION"], True)
    create_zipped_dirs()
    update_and_push()
    release_to_github()
