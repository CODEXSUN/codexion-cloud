# cloud/commands/generate_env.py

from pathlib import Path

ENV_TEMPLATE = """# ──────────────────────────────────────────────
# Codexion Environment Configuration
# ──────────────────────────────────────────────

# Project Settings
PROJECT_NAME={project_name}
PROJECT_DIR={project_dir}

# Application Environment
ENV=development
DEBUG=true
APP_VERSION=1.0.0

# Domain and Networking
DOMAIN={project_name}
BACKEND_PORT=8000
FRONTEND_PORT=8000

# Database Settings
DB_ENGINE=mariadb
MARIADB_ROOT_PASSWORD=DbPass1@@
DB_HOST=codexion-db
DB_PORT=3306
DB_NAME=codexion_db
DB_USER=root
DB_PASSWORD=DbPass1@@

# Redis Settings
REDIS_HOST=codexion-redis
REDIS_PORT=6379

# Email Settings (Optional)
EMAIL_PROVIDER=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USERNAME=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_USE_TLS=true

# Git Config (Optional)
GIT_REPO_URL=https://github.com/your-org/codexion.git
GIT_BRANCH=main

# Docker / Traefik
TRAEFIK_ENABLED=true
TRAEFIK_HTTP_PORT=80
TRAEFIK_HTTPS_PORT=443

# Logging
LOG_LEVEL=info
LOG_DIR=logs/

# Misc
TIMEZONE=Asia/Kolkata
LANGUAGE_CODE=en-us
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
