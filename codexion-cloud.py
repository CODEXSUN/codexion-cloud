# codexion-cloud.py

import argparse
from pathlib import Path
import shutil
from cloud import init


def main():
    parser = argparse.ArgumentParser(description="Codexion Cloud CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # init command
    init_parser = subparsers.add_parser("init", help="Initialize Codexion Cloud project")
    init_parser.add_argument("--force", action="store_true", help="Force overwrite if project already exists")

    init_parser.set_defaults(func=init.run)

    args = parser.parse_args()

    if args.command == "init":
        print("🏝️ Enter project name (default: codexion): ", end="")
        project_name = input().strip() or "codexion"
        base_path = Path.cwd() / project_name

        if base_path.exists() and not args.force:
            print(f"⚠️  Project '{project_name}' already exists at {base_path}.")
            confirm = input("❓ Do you want to overwrite it? (y/n): ").strip().lower()
            if confirm != "y":
                print("❌ Aborting setup.")
                return
            print(f"🧹 Removing existing project folder: {base_path}")
            shutil.rmtree(base_path)

        # Pass project name and path to init
        args.project_name = project_name
        args.project_path = base_path
        args.func(args)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()