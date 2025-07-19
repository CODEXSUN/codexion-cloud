"""
Codexion Scaffold Generator

Creates the base file and folder structure for a full-stack Frappe + FastAPI + React project.

# Created on: 19-07-2025 03:02:30 Am
# Author: Sundar
# Version: 24-02-2025
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from cloud.commands.filegenerator import generate_multiple_files


def create_codexion_scaffold(project_name: str = "codexion"):
    """
    Generate the initial scaffold structure for a Codexion project.

    Args:
        project_name (str): Name of the base project folder. Defaults to "codexion".
    """
    load_dotenv()

    # Determine base project path
    env_project_dir = os.getenv("PROJECT_DIR")
    if env_project_dir:
        base_path = Path(env_project_dir).resolve()
        print(f"📂 Using project directory from .env: {base_path}")
    else:
        base_path = Path.cwd() / project_name
        print(f"📂 Using project directory: {base_path}")

    # Define scaffold file list
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

    # Use file generator to create all files and folders
    generate_multiple_files(files)
    print("\n✅ Scaffold generated successfully at:", base_path)
