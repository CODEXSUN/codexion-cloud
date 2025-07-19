# dockit.py

import os
from dotenv import load_dotenv
from cloud.docker.generators import (
    dockerfile_gen,
    compose_gen,
    env_gen,
    other_files_gen,
)

def run():
    # Load environment
    load_dotenv()
    project_name = os.getenv("PROJECT_NAME", "codexion")
    print(f"🚀 Generating Docker setup for: {project_name}")

    # Define output folder (reuse if exists)
    output_dir = os.path.join(os.getcwd(), project_name)
    os.makedirs(output_dir, exist_ok=True)

    # Step-by-step generation
    dockerfile_gen.generate(output_dir)
    compose_gen.generate(output_dir)
    env_gen.generate(output_dir)
    other_files_gen.generate(output_dir)

    print(f"✅ All Docker files generated inside: {output_dir}")

if __name__ == "__main__":
    main()
