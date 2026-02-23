import os
import zipfile
import shutil
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.resolve()
DOWNLOADS = Path.home() / "Downloads"
UPDATE_NAME = "sciencefair_update.zip"


def apply_update_if_exists():
    update_path = DOWNLOADS / UPDATE_NAME

    if not update_path.exists():
        return

    print("Update file detected. Applying update...")

    with zipfile.ZipFile(update_path, 'r') as zip_ref:
        for member in zip_ref.namelist():

            # Security: prevent absolute paths or parent traversal
            if ".." in member or member.startswith("/"):
                continue

            target_path = PROJECT_ROOT / member

            # Ensure target stays inside project
            if not str(target_path.resolve()).startswith(str(PROJECT_ROOT)):
                continue

            # Create directories if needed
            target_path.parent.mkdir(parents=True, exist_ok=True)

            with zip_ref.open(member) as source, open(target_path, "wb") as target:
                shutil.copyfileobj(source, target)

            print(f"Updated: {member}")

    update_path.unlink()
    print("Update complete. Launching system.\n")


if __name__ == "__main__":

    apply_update_if_exists()

    subprocess.run(["streamlit", "run", "app/ui.py"])