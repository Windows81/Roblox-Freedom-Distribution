#!/bin/bash

# replacement for $PSScriptRoot
root="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/"

pyinstaller \
	--name "RFD" \
	--onefile "$root/Source/_main.py" \
	--paths "$root/Source/" \
	--workpath "$root/PyInstallerWork" \
	--distpath "$root" \
	--icon "$root/Source/Icon.ico" \
	--specpath "$root/PyInstallerWork/Spec" \
	--add-data "$root/Source/*:./Source" \
	--hidden-import requests