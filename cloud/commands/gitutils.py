from dotenv import load_dotenv
from pathlib import Path
import os
import subprocess
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

def init_git_repo(env_path=None):
    if env_path is None:
        env_path = Path.cwd() / ".env"
    else:
        env_path = Path(env_path)

    # ✅ This is the missing piece
    load_dotenv(dotenv_path=env_path)

    print(env_path)  # for confirmation

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
