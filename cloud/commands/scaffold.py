# cloud/commands/scaffold.py

from pathlib import Path
import os
from dotenv import load_dotenv

from cloud.commands.structure import create_folder_structure
from cloud.commands.filegenerator import generate_multiple_files


def create_codexion_scaffold(project_name: str, force_env: bool = False):
    """
    Creates the full folder and file scaffold for a Codexion project.

    Parameters:
    - project_name (str): Name of the project folder (used only if .env is not prioritized).
    - force_env (bool): If True, will use PROJECT_DIR from .env forcibly.
    """
    load_dotenv()

    # Get .env path if exists and requested
    env_project_dir = os.getenv("PROJECT_DIR")
    if env_project_dir and force_env:
        base_path = Path(env_project_dir).resolve()
        print(f"📂 Using project directory from .env: {base_path}")
    else:
        base_path = Path.cwd() / project_name
        print(f"📂 Using project directory: {base_path}")

    # Ensure structure exists
    create_folder_structure(base_path)

    # Define initial scaffold files
    files = [
        {
            "name": "main",
            "path": base_path / "backend",
            "extension": ".py",
            "content": "# Entry point for backend server\n"
        },
        {
            "name": "README",
            "path": base_path,
            "extension": ".md",
            "content": "# Codexion\n\nA full-stack Frappe + FastAPI + React DevOps scaffold."
        },
        {
            "name": "requirements",
            "path": base_path / "backend",
            "extension": ".txt",
            "content": "fastapi\nuvicorn\n"
        },
        {
            "name": "vite.config",
            "path": base_path / "frontend",
            "extension": ".js",
            "content": "// Vite config\n"
        },
        {
            "name": "index",
            "path": base_path / "frontend",
            "extension": ".html",
            "content": "<!-- Entry HTML for frontend -->\n"
        },
    ]

    generate_multiple_files(files)
    print("\n✅ Scaffold generated successfully at:", base_path)
