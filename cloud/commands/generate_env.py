# commands/utils/generate_env.py
from pathlib import Path

ENV_TEMPLATE = """# Codexion Environment Configuration
PROJECT_NAME={project_name}
PROJECT_DIR={project_dir}
MARIADB_ROOT_PASSWORD=DbPass1@@
DOMAIN={project_name}.local
"""

def generate_env_file(env_path: Path, project_name: str, force: bool = False):
    if env_path.exists() and not force:
        print(f"⚠️  .env file already exists at {env_path}. Use --force to overwrite.")
        return

    project_dir = str(env_path.parent.resolve())
    content = ENV_TEMPLATE.format(
        project_name=project_name,
        project_dir=project_dir
    )

    with env_path.open('w') as f:
        f.write(content)
    print(f"✅ Generated .env file at {env_path}")