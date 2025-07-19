# dockit.py

import os
from pathlib import Path
from dotenv import load_dotenv
from cloud.docker.generators import (
    dockgen,
    # env_gen,
    # other_files_gen,
)

from cloud.docker.generators.dockfile import dockerfile
from cloud.docker.generators.composefile import docker_compose
from cloud.docker.generators.service_compose import service_compose


def run(args):
    # Default values
    project_name = "codexion"
    base_path = Path(os.getcwd()) / project_name
    env_path = base_path / ".env"

    print(f"🐳 Docker project: {project_name}")
    base_path.mkdir(parents=True, exist_ok=True)

    output_dir = base_path / "docker" / "output"
    os.makedirs(output_dir, exist_ok=True)
    output_dir = str(output_dir)

    dockerfile(output_dir)
    docker_compose(output_dir)
    service_compose(output_dir)

    print(f"✅ All Docker files generated inside: {output_dir}")