# cloud/utils/docgen.py

"""
# Codexion Header Generator

usage: This script scans Python files in the current directory and subdirectories and adds a standard header
with metadata such as file name, author, creation date, and version.
It can also overwrite existing headers or simulate changes without modifying files.

$ python cloud/utils/docgen.py --author sundar

📁 Scanning path: /home/user/project
[?] Header exists in main.py. Overwrite? [y/N]: y
✔ Updated: main.py
✔ Updated: utils/helper.js
✔ Updated: docs/README.md

✅ Done.


"""

import os
import argparse
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
VERSION = os.getenv("APP_VERSION", "24-02-2025")
SKIP_DIRS = {"__pycache__", "venv", "migrations"}
DATETIME_FORMAT = "%d-%m-%Y %I:%M:%S %p"


def should_skip(path: Path) -> bool:
    """Check if the file is inside a directory that should be skipped."""
    return any(part in SKIP_DIRS for part in path.parts)


def generate_header(filepath: Path, author: str) -> str:
    """Generate a standard header for the file with metadata."""
    date_str = datetime.now().strftime(DATETIME_FORMAT)
    return (
        f"File: {filepath}\n"
        f"Author: {author}\n"
        f"Created on: {date_str}\n"
        f"Version: {VERSION}\n"
        f"--------------------------------------------------\n\n"
    )


def ask_to_overwrite(file_path: Path) -> bool:
    """Prompt user to ask whether to overwrite existing header."""
    response = input(f"❓ Header already exists in {file_path}. Overwrite? (y/n): ").strip().lower()
    return response == "y"


def apply_header_to_file(file_path: Path, author: str, overwrite: bool = False, dry_run: bool = False):
    """Insert the header into the file if not present, or overwrite if specified."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    header_exists = content.startswith("# File:")

    if header_exists and not overwrite:
        if not ask_to_overwrite(file_path):
            print(f"⏭ Skipped: {file_path}")
            return

    header = generate_header(file_path, author)
    updated = header + content if not header_exists else header + "\n".join(content.splitlines()[5:])

    if dry_run:
        print(f"[DRY-RUN] Would update: {file_path}")
    else:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(updated)
        print(f"✔ Updated: {file_path}")


def scan_and_apply_headers(base_path: Path, author: str, overwrite: bool = False, dry_run: bool = False):
    """Walk the directory and apply headers to .py files."""
    for path in base_path.rglob("*.py"):
        if should_skip(path):
            continue
        apply_header_to_file(path, author=author, overwrite=overwrite, dry_run=dry_run)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Codexion Header Generator")
    parser.add_argument("folder", help="Root folder to scan (e.g., codexion)")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing headers without asking")
    parser.add_argument("--dry-run", action="store_true", help="Simulate header update without saving")
    parser.add_argument("--author", type=str, default="auto-docgen", help="Author name to include in headers")
    args = parser.parse_args()

    root_folder = Path(args.folder).resolve()
    if not root_folder.exists():
        print(f"❌ Error: The folder '{root_folder}' does not exist.")
        exit(1)

    scan_and_apply_headers(root_folder, author=args.author, overwrite=args.overwrite, dry_run=args.dry_run)


