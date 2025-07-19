# commands/utils/structure.py
from pathlib import Path

def create_folder_structure(base_path: Path):
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
