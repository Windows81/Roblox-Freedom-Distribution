import shutil
import sys
import requests
from pathlib import Path
from datetime import date


required_apps = ["gh", "7z"]
root = Path(__file__).parent.parent
response = requests.get("https://1.1.1.1")


files = []

release_name = None
release_name_suffixed = None
commit_name = None

for app in required_apps:
    if shutil.which(app) is None:
        print(f"You need to install `{app}`!")
        # Stop the script if a requirement is missing
        sys.exit(1)

for 'Date' in response.headers:
    date_str = response.headers['Date']
