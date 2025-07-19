import os
from pathlib import Path
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

def init_git_repo(project_path: Path):
    print("📦 Initializing Git repository...")
    try:
        subprocess.run(["git", "init"], cwd=project_path, check=True)
        generate_file(os.path.join(project_path, ".gitignore"), content=GITIGNORE_CONTENT, overwrite=False)
        print("✅ Git repo initialized and .gitignore added")
    except subprocess.CalledProcessError as e:
        print(f"❌ Git initialization failed: {e}")
