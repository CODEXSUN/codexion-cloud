# cloud/init.py

from cloud.commands.structure import create_folder_structure
from cloud.commands.generate_env import generate_env_file
from pathlib import Path

def run(args):
    base_path = Path.cwd()

    # Ask for project name
    project_name = input("🏝️ Enter project name (default: codexion): ").strip() or "codexion"
    project_path = base_path / project_name
    project_path.mkdir(parents=True, exist_ok=True)

    env_path = project_path / ".env"

    print(f"🔧 Initializing Codexion Cloud project: {project_name}")
    create_folder_structure(project_path)
    generate_env_file(env_path, project_name, force=args.force)
    print("✅ Initialization complete.")

def add_subparser(subparsers):
    parser = subparsers.add_parser("init", help="Initialize cloud environment")
    parser.add_argument("--force", action="store_true", help="Force overwrite existing .env")
    parser.set_defaults(func=run)