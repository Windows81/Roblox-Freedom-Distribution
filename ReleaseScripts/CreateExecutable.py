import subprocess
import platform
from pathlib import Path

os_name = platform.system()
root = Path(__file__).resolve().parent.parent

data_separator = ";" if os_name == "Windows" else ":"
if os_name == "Darwin":
	icon_format = "icns"
else:
	icon_format = "ico"

command = ["pyinstaller"]
args = {
	"--name": "RFD",
	"--onefile": f"{root}/Source/_main.py",
	"--paths": f"{root}/Source/",
	"--workpath": f"{root}/PyInstallerWork",
	"--distpath": f"{root}",
	"--icon": f"{root}/Source/Icon.{icon_format}",
	"--specpath": f"{root}/PyInstallerWork/Spec",
	"--add-data": f"{root}/Source/*{data_separator}./Source",
	"--hidden-import": "requests" # Allows functions in config to use the `requests` library (1 MiB addition).
}

for flag, value in args.items():
    command.append(flag)
    command.append(value)

subprocess.run(command)