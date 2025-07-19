# commands/utils/filegenerator.py

from pathlib import Path
from datetime import datetime
import getpass

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

def generate_file(file_path: Path, content: str = "", overwrite: bool = False):
    file_path.parent.mkdir(parents=True, exist_ok=True)

    if file_path.exists() and not overwrite:
        print(f"⚠️  File exists: {file_path} (skipped)")
        return

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    author = getpass.getuser()
    relative_path = str(file_path).replace(str(Path.cwd()), "").lstrip("\\/")

    header = f"""# {relative_path}
# Created on: {created_at}
# Author: {author}

"""

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(header + content)

    print(f"✅ Created: {file_path}")


def prompt_file_type() -> str:
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
    name = input("Enter file name (no extension): ").strip()
    ext = prompt_file_type()
    path = input("Enter folder path (relative): ").strip()

    content = input("Enter file content (optional): ").strip()

    full_path = Path(path) / f"{name}{ext}"
    generate_file(full_path, content=content)


def generate_multiple_files(file_defs: list[dict], overwrite=False):
    for f in file_defs:
        name = f.get("name")
        path = Path(f.get("path", "."))
        ext = f.get("extension", ".txt")
        content = f.get("content", "")

        full_path = path / f"{name}{ext}"
        generate_file(full_path, content=content, overwrite=overwrite)
