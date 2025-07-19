# dockit.py

import os
from pathlib import Path
from dotenv import load_dotenv
from cloud.docker.generators import (
    dockgen,
    # env_gen,
    # other_files_gen,
)


def run(args):
    # Default values
    project_name = "codexion"
    base_path = Path(os.getcwd()) / project_name
    env_path = base_path / ".env"

    print(f"🐳 Docker project: {project_name}")
    base_path.mkdir(parents=True, exist_ok=True)

    output_dir = base_path / "docker" / "output"
    os.makedirs(output_dir, exist_ok=True)

    dockgen.run_all(project_name)

    print(f"✅ All Docker files generated inside: {output_dir}")