# cloud/init.py

from cloud.commands.generate_env import generate_env_file
from cloud.utils.scaffold import create_codexion_scaffold


def run(args):
    base_path = args.project_path
    project_name = args.project_name
    env_path = base_path / ".env"

    print(f"🔧 Initializing Codexion Cloud project: {project_name}")
    base_path.mkdir(parents=True, exist_ok=True)

    generate_env_file(env_path, project_name, force=args.force)
    create_codexion_scaffold()

    print("✅ Initialization complete.")

def add_subparser(subparsers):
    parser = subparsers.add_parser("init", help="Initialize cloud environment")
    parser.add_argument("--force", action="store_true", help="Force overwrite existing .env")
    parser.set_defaults(func=run)
