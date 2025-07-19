# cloud/commands/generate_env.py

from pathlib import Path

ENV_TEMPLATE = """# Codexion Environment Configuration
# Generated automatically by generate_env_file()

PROJECT_NAME={project_name}
PROJECT_DIR={project_dir}
MARIADB_ROOT_PASSWORD=DbPass1@@
DOMAIN={project_name}.local
"""

def generate_env_file(env_path: Path, project_name: str, force: bool = False):

    """
    Generate a .env file with default project environment variables.
    """

    if isinstance(env_path, str):
        env_path = Path(env_path)

    if env_path.exists() and not force:
        print(f"⚠️  .env file already exists at {env_path}. Use --force to overwrite.")
        return

    project_dir = str(env_path.parent.resolve())

    try:
        content = ENV_TEMPLATE.format(
            project_name=project_name,
            project_dir=project_dir
        )

        env_path.write_text(content.strip() + '\n', encoding="utf-8")
        # Ensures trailing newline
        print(f"✅ Generated .env file at {env_path}")
    except Exception as e:
        print(f"❌ Failed to generate .env file: {e}")
