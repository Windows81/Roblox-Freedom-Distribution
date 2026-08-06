# pyright: reportUnusedCallResult=false

# This script was orignally AI slop.
# Either Deepseek or Qwen did the initial conversion from PowerShell.  I forgot which one.

from datetime import datetime
import subprocess
import textwrap
import shutil
import os

os.chdir(os.path.dirname(__file__))


def check_software(software_list: list[str]) -> bool:
    """Checks if the appropriate software is installed."""
    for software in software_list:
        if shutil.which(software) is None:
            print(f"You need to install ``{software}``!")
            return False
    return True


def retrieve_input():
    """Retrieves user input for version title and commit message."""

    commit_name = datetime.now().strftime("%Y-%m-%dT%H%MZ")
    release_name = input("Version title? ")

    return (commit_name, release_name)


def update_and_push(commit_name: str):
    # Updates submodules.
    subprocess.run([
        "git", "submodule", "foreach",
        f"git add . && git commit -m {commit_name} && git push",
    ])
    # Updates main repository.
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", commit_name])
    subprocess.run(["git", "push"])


def update_const_release_version(labels: dict[str, str]):
    const_file = "../Source/util/const.py"

    with open(const_file, 'r') as f:
        const_txt = f.readlines()

    # Updates each label.
    for i, line in enumerate(const_txt):
        label_name = line.split(' ', 1)[0]
        label_replacement = labels.get(label_name)
        if label_replacement is None:
            continue
        const_txt[i] = f"{label_name} = '''{label_replacement}'''\n"

    with open(const_file, 'w') as f:
        f.writelines(const_txt)


def create_zipped_dirs(release_name_suffixed: str):
    """Creates zipped directories for Roblox files."""
    files: list[str] = []

    version_data = [
        (t_path, version, typ)
        for version in os.listdir('../Roblox')
        if os.path.isdir(v_path := f'../Roblox/{version}')
        for typ in os.listdir(v_path)
        if not typ.startswith('_') and os.path.isdir(t_path := f'{v_path}/{typ}')
    ]

    for (t_path, version, typ) in version_data:
        zip_name = f'../Roblox/{version}.{typ}.7z'

        # Writes to the version-flag file.
        version_file = t_path + "/rfd_version"
        with open(version_file, 'w') as f:
            f.write(release_name_suffixed)

        # Builds exclusion patterns.
        exclude_patterns = [
            "-xr!RFDStarterScript.lua",
            "-x!_*",
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

        # Runs `7z`` command.
        subprocess.run([
            "7z", "a", zip_name,
            f"{t_path}/*", *exclude_patterns,
        ])

        # Appends resultant zip file.
        files.append(zip_name)
    return files


def mark_latest_version():
    """Marks the most recent release on GitHub as the latest."""
    result = subprocess.run(
        ["gh", "release", "list", "--json", "tagName", "--template",
            "{{range .}}{{.tagName}}{{end}}", "--limit", "1"],
        capture_output=True, text=True
    )
    latest = result.stdout.strip()
    subprocess.run([
        "gh", "release", "edit", latest, "--latest",
    ])


def release_to_github(files: list[str], release_name_suffixed: str):
    """Creates a GitHub release with specified files."""
    subprocess.run([
        "gh", "release", "create",
        release_name_suffixed, *files,
        "--prerelease", "--generate-notes",
    ])


def main():
    # Checks software.
    if not check_software(["gh", "7z", "git"]):
        return
    files = []

    # Prompts user to select build mode.
    mode = input(textwrap.dedent("""
	1. Update version string
	2. Update version string then create new commit
	3. Zip binaries and add them to a new version in GitHub Releases
	"""))

    # Executes selected build mode.
    match mode:
        case '1':
            (commit_name, release_name) = retrieve_input()
            update_const_release_version(
                labels={
                    "GIT_RELEASE_VERSION": release_name,
                }
            )
        case '2':
            (commit_name, release_name) = retrieve_input()
            update_const_release_version(
                labels={
                    "GIT_RELEASE_VERSION": release_name,
                }
            )
            update_and_push(commit_name)
        case '3':
            (commit_name, release_name) = retrieve_input()
            release_name_suffixed = release_name + '-binaries'
            update_const_release_version(
                labels={
                    "GIT_RELEASE_VERSION": release_name,
                    "ZIPPED_RELEASE_VERSION": release_name_suffixed
                }
            )
            files = create_zipped_dirs(release_name_suffixed)
            update_and_push(commit_name)
            release_to_github(files, release_name_suffixed)
        case _:
            pass


if __name__ == "__main__":
    main()
