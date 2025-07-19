# codexion-cloud.py

import argparse
from pathlib import Path
import shutil
from cloud import init, dockit  # assumes cloud/init.py and cloud/dockit.py exist with run() in each


def main():
    parser = argparse.ArgumentParser(description="Codexion Cloud CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # ✅ init command
    parser_init = subparsers.add_parser("init", help="Initialize Codexion Cloud project")
    parser_init.add_argument("--force", action="store_true", help="Force overwrite if project already exists")
    parser_init.set_defaults(func=init.run)

    # ✅ dockit command
    parser_dockit = subparsers.add_parser("dockit", help="Generate Docker setup for Codexion Cloud")
    parser_dockit.set_defaults(func=dockit.run)

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

        # Inject values into args and call init.run(args)
        args.project_name = project_name
        args.project_path = base_path
        args.func(args)

    elif hasattr(args, "func"):
        args.func(args)  # for dockit and future commands
    else:
        parser.print_help()


if __name__ == "__main__":
    main()