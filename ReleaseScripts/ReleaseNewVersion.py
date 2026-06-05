# DO NOT USE YET!!!

from datetime import datetime
from pathlib import Path
import subprocess
import textwrap
import shutil


def check_software(software_list: list[str]) -> bool:
    """Checks if the appropriate software is installed."""
    for software in software_list:
        if shutil.which(software) is None:
            print(f"You need to install ``{software}``!")
            return False
    return True


def retrieve_input(suffix: str = ''):
    """Retrieves user input for version title and commit message."""
    global release_name, release_name_suffixed, commit_name

    release_name = input("Version title? ")
    release_name_suffixed = release_name + suffix
    commit_name = datetime.now().strftime("%Y-%m-%dT%H%MZ")


def update_and_push():
    # Updates submodules,
    subprocess.run(
        [
            "git", "submodule", "foreach",
            f"git add . && git commit -m {commit_name} && git push",
        ],
        shell=True,
    )
    # Updates main repository.
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", commit_name])
    subprocess.run(["git", "push"])


def update_const_release_version(labels: list[str], add_suffix: bool = False):
    const_file = Path("../Source/util/const.py")
    label_value = release_name_suffixed if add_suffix else release_name

    with open(const_file, 'r') as f:
        const_txt = f.readlines()

    # Update each label
    for label in labels:
        start = f"{label} = "
        for i, line in enumerate(const_txt):
            if not line.startswith(start):
                continue
            const_txt[i] = start + f"'''{label_value}'''\n"
            break

    with open(const_file, 'w') as f:
        f.writelines(const_txt)


def create_zipped_dirs():
    """Creates zipped directories for Roblox files."""
    global files

    root = Path("..")
    roblox_dirs = list(root.glob("Roblox/*/*"))

    for dir_path in roblox_dirs:
        if not dir_path.is_dir():
            continue

        zip_name = f"{root}/Roblox/{dir_path.parent.name}.{dir_path.name}.7z"

        # Always overwrites the file
        if Path(zip_name).exists():
            Path(zip_name).unlink()

        # Writes to the version-flag file
        version_file = dir_path / "rfd_version"
        with open(version_file, 'w') as f:
            f.write(release_name_suffixed)

        # Build exclusion patterns
        exclude_patterns = [
            "-xr!RFDStarterScript.lua",
            "-x!_*.exe",
            "-x!_*.json",
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

        # Run 7z command
        cmd = ["7z", "a", zip_name, f"{dir_path}/*"] + exclude_patterns
        subprocess.run(cmd)

        files.append(zip_name)


def mark_latest_version():
    """Marks the most recent release on GitHub as the latest."""
    result = subprocess.run(
        ["gh", "release", "list", "--json", "tagName", "--template",
            "{{range .}}{{.tagName}}{{end}}", "--limit", "1"],
        capture_output=True, text=True
    )
    latest = result.stdout.strip()
    subprocess.run(["gh", "release", "edit", latest, "--latest"])


def release_to_github():
    """Creates a GitHub release with specified files."""
    cmd = ["gh", "release", "create", release_name_suffixed] + \
        files + ["--prerelease", "--generate-notes"]
    subprocess.run(cmd)


def main():
    # Checks software.
    if not check_software(["gh", "7z", "git"]):
        return

    global files, release_name, release_name_suffixed, commit_name
    files = []

    # Defines root directory.
    root = Path(__file__).parent.parent

    # Prompts user to select build mode.
    mode = input(textwrap.dedent("""
	1. Update version string
	2. Update version string then create new commit
	3. Zip binaries and add them to a new version in GitHub Releases
	"""))

    # Executes selected build mode.
    if mode == '1':
        retrieve_input()
        update_const_release_version(
            labels=["GIT_RELEASE_VERSION"],
            add_suffix=False,
        )
    elif mode == '2':
        retrieve_input()
        update_const_release_version(
            labels=["GIT_RELEASE_VERSION"],
            add_suffix=False,
        )
        update_and_push()
    elif mode == '3':
        retrieve_input(suffix="-binaries")
        update_const_release_version(
            labels=["GIT_RELEASE_VERSION"],
            add_suffix=False,
        )
        update_const_release_version(
            labels=["ZIPPED_RELEASE_VERSION"],
            add_suffix=True,
        )
        create_zipped_dirs()
        update_and_push()
        release_to_github()


if __name__ == "__main__":
    main()
