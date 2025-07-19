# commands/utils/structure.py

from pathlib import Path
from datetime import datetime
import os
import subprocess

def get_git_username():
    try:
        username = subprocess.check_output(
            ["git", "config", "user.name"], stderr=subprocess.DEVNULL
        ).decode().strip()
        if username:
            return username
    except Exception:
        pass
    return os.getenv("USERNAME") or os.getenv("USER") or "unknown"

def create_folder_structure(base_path: Path):
    author = get_git_username()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    folders = [
        "certs",
        "docker",
        "backend",
        "frontend",
        "database",
        "utils"
    ]

    for folder in folders:
        folder_path = base_path / folder
        folder_path.mkdir(parents=True, exist_ok=True)
        print(f"📁 Created folder: {folder_path}")

        # Create __init__.py with metadata
        init_file = folder_path / "__init__.py"
        relative_path = f"{base_path.name}/{folder}/__init__.py"
        content = (
            f"# {relative_path}\n"
            f"# Created: {timestamp}\n"
            f"# Author: {author}\n"
        )
        # ✅ FIX UnicodeEncodeError on Windows
        init_file.write_text(content, encoding="utf-8")
