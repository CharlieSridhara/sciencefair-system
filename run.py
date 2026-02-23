import sys
import subprocess
import json
import requests
import zipfile
import shutil
import io
from pathlib import Path

# ==============================
# CONFIG
# ==============================

GITHUB_USER = "CharlieSridhara"
REPO_NAME = "sciencefair-system"

REMOTE_VERSION_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/main/version.json"
REMOTE_ZIP_URL = f"https://github.com/{GITHUB_USER}/{REPO_NAME}/archive/refs/heads/main.zip"

PROJECT_ROOT = Path(__file__).parent
LOCAL_VERSION_FILE = PROJECT_ROOT / "version.json"
APP_PATH = PROJECT_ROOT / "app" / "ui.py"

# ==============================
def get_local_version():
    if not LOCAL_VERSION_FILE.exists():
        return "0.0.0"
    with open(LOCAL_VERSION_FILE) as f:
        return json.load(f)["version"]

def get_remote_version():
    try:
        r = requests.get(REMOTE_VERSION_URL, timeout=5)
        return r.json()["version"]
    except:
        return None

def update_project():
    print("Updating project from GitHub...")

    r = requests.get(REMOTE_ZIP_URL)
    z = zipfile.ZipFile(io.BytesIO(r.content))

    temp_dir = PROJECT_ROOT / "_update_temp"
    if temp_dir.exists():
        shutil.rmtree(temp_dir)

    z.extractall(temp_dir)

    extracted_root = next(temp_dir.iterdir())

    for item in extracted_root.iterdir():
        if item.name == ".git":
            continue

        target = PROJECT_ROOT / item.name

        if target.exists():
            if target.is_dir():
                shutil.rmtree(target)
            else:
                target.unlink()

        shutil.move(str(item), str(target))

    shutil.rmtree(temp_dir)

    print("Update complete.")

# ==============================
def main():

    local_version = get_local_version()
    remote_version = get_remote_version()

    if remote_version and remote_version != local_version:
        print(f"New version detected: {remote_version}")
        update_project()

    print("Launching FluoroBrush Pro...\n")

    subprocess.run([
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(APP_PATH)
    ])

if __name__ == "__main__":
    main()