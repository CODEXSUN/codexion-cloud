# cloud/commands/filegenerator.py

import os
import subprocess
from pathlib import Path
from datetime import datetime
import getpass

from cloud.utils.docgen import generate_header  # 🧠 Unified header logic

# 🎯 Supported file extensions
FILE_TYPES = {
    "py": ".py",
    "md": ".md",
    "env": ".env",
    "txt": ".txt",
    "json": ".json",
    "yml": ".yml",
    "js": ".js",
    "html": ".html",
    "css": ".css"
}

# 🔍 File-type-specific comment styles
COMMENT_STYLES = {
    ".py": "# {text}",
    ".env": "# {text}",
    ".txt": "# {text}",
    ".md": "[//]: # ({text})",
    ".json": "// {text}",
    ".yml": "# {text}",
    ".js": "// {text}",
    ".html": "<!-- {text} -->",
    ".css": "/* {text} */"
}


def get_git_username() -> str:
    """🧑‍💻 Tries to get the current Git username; falls back to OS user or 'unknown'."""
    try:
        username = subprocess.check_output(
            ["git", "config", "user.name"], stderr=subprocess.DEVNULL
        ).decode().strip()
        if username:
            return username
    except Exception:
        pass
    return os.getenv("USERNAME") or os.getenv("USER") or getpass.getuser() or "unknown"


def wrap_header_with_comment_style(header: str, extension: str) -> str:
    """🎨 Apply file-type-specific comment syntax to each line of the header."""
    style = COMMENT_STYLES.get(extension, "# {text}")
    return "\n".join(style.format(text=line) for line in header.strip().splitlines()) + "\n\n"


def generate_file(file_path: Path, content: str = "", overwrite: bool = False):
    """📝 Generates a file with optional content, adds comment-style headers, and handles overwrite rules."""
    file_path.parent.mkdir(parents=True, exist_ok=True)

    if file_path.exists() and not overwrite:
        print(f"⚠️  File exists: {file_path} (skipped)")
        return

    author = get_git_username()
    extension = file_path.suffix
    version = os.getenv("app_version")

    # ✅ Pass Path object to generate_header, not string

    raw_header = generate_header(file_path=file_path, author=author, version=version)

    comment_header = wrap_header_with_comment_style(raw_header, extension)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(comment_header + content)

    print(f"✅ Created: {file_path}")


def prompt_file_type() -> str:
    """🔧 Prompts user to choose from supported file types."""
    print("\n📄 Choose a file type:")
    for i, ext in enumerate(FILE_TYPES.keys(), start=1):
        print(f"{i}. {ext}")

    while True:
        try:
            choice = int(input("Enter number: ").strip())
            if 1 <= choice <= len(FILE_TYPES):
                return list(FILE_TYPES.values())[choice - 1]
        except Exception:
            pass
        print("❌ Invalid choice. Try again.")


def generate_interactive():
    """👤 Interactive CLI prompt for creating a single file."""
    name = input("Enter file name (no extension): ").strip()
    ext = prompt_file_type()
    path = input("Enter folder path (relative): ").strip()
    content = input("Enter file content (optional): ").strip()

    full_path = Path(path) / f"{name}{ext}"
    generate_file(full_path, content=content)


def generate_multiple_files(file_defs: list[dict], overwrite=False):
    """
    📦 Batch generator for multiple files via list of dicts.
    Example entry: {"name": "README", "path": "docs", "extension": ".md", "content": "Hello"}
    """
    for f in file_defs:
        name = f.get("name")
        path = Path(f.get("path", "."))  # default to current dir
        ext = f.get("extension", ".txt")
        content = f.get("content", "")

        full_path = path / f"{name}{ext}"
        generate_file(full_path, content=content, overwrite=overwrite)
