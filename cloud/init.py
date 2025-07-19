# cloud/init.py
from cloud.commands.gitutils import init_git_repo
from cloud.commands.structure import create_folder_structure
from cloud.commands.generate_env import generate_env_file
from cloud.utils.scaffold import create_codexion_scaffold


def run(args):
    base_path = args.project_path
    project_name = args.project_name
    env_path = base_path / ".env"

    print(f" Initializing Codexion Cloud project: {project_name}")
    base_path.mkdir(parents=True, exist_ok=True)

    generate_env_file(env_path, project_name, force=args.force)

    create_folder_structure(base_path)

    create_codexion_scaffold(project_name=args.project_name, force_env=args.force)

    init_git_repo()

    print("Initialization complete.")

def add_subparser(subparsers):
    parser = subparsers.add_parser("init", help="Initialize cloud environment")
    parser.add_argument("--force", action="store_true", help="Force overwrite existing .env")
    parser.set_defaults(func=run)
