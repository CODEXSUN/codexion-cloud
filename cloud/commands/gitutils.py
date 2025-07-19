import os
import subprocess
from pathlib import Path
from dotenv import load_dotenv
from cloud.commands.filegenerator import generate_file

GITIGNORE_CONTENT = """
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Virtual environment
.env
venv/
ENV/
env/

# VSCode
.vscode/

# MacOS
.DS_Store

# Node.js
node_modules/
dist/
build/
.npm/

# Python
*.egg-info/
.eggs/
*.log
*.sqlite3

# Git
.git/
"""

def init_git_repo():
    load_dotenv()
    project_path_str = os.getenv("PROJECT_DIR")

    if not project_path_str:
        print("❌ PROJECT_DIR not set in .env")
        return

    project_path = Path(project_path_str)

    if not project_path.exists():
        print(f"❌ Path does not exist: {project_path}")
        return

    print(f"📦 Initializing Git repository in {project_path}...")

    try:
        subprocess.run(["git", "init"], cwd=project_path, check=True)
        generate_file(project_path / ".gitignore", content=GITIGNORE_CONTENT, overwrite=False)
        print("✅ Git repo initialized and .gitignore added")
    except subprocess.CalledProcessError as e:
        print(f"❌ Git initialization failed: {e}")