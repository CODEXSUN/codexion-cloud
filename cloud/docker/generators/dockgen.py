import os
import re
from jinja2 import Environment, FileSystemLoader
from cloud.utils.jinja_cleanup import postprocess_rendered

def run(output_dir: str):
    print(f"🛠️  Running dockgen for: {output_dir}")

    # Load Jinja2 templates
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    env = Environment(loader=FileSystemLoader(template_dir))
    template_file = env.get_template('dockerfile.j2')

    # Your context for rendering
    context = {
        "base_image": "ubuntu:24.04",
        "packages": ["python3", "python3-pip", "curl", "nano"],
        "cmd": "bash"
    }

    # Render and process
    rendered = template_file.render(context)
    rendered_clean = postprocess_rendered(rendered)

    # Write output
    docker_output_dir = os.path.join(output_dir, "docker", "output")
    os.makedirs(docker_output_dir, exist_ok=True)
    dockerfile_path = os.path.join(docker_output_dir, "Dockerfile")

    print(f"[DEBUG] Writing Dockerfile to: {dockerfile_path}")
    with open(dockerfile_path, "w") as f:
        f.write(rendered_clean)

    print("✅ Dockerfile generated successfully.")
