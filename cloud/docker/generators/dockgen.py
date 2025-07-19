import os
from jinja2 import Environment, FileSystemLoader
from cloud.utils.jinja_cleanup import postprocess_rendered


def generate_from_template(template_name: str, output_filename: str, context: dict, output_dir: str):
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    env = Environment(loader=FileSystemLoader(template_dir))
    template_file = env.get_template(template_name)

    # Render template
    raw_output = template_file.render(context)
    final_output = postprocess_rendered(raw_output)

    # Write to file
    output_path = os.path.join(output_dir, output_filename)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        f.write(final_output)

    print(f"✅ Generated: {output_filename}")


def run_all(output_dir: str):
    context = {
        "base_image": "ubuntu:24.04",
        "packages": ["python3", "python3-pip", "curl", "nano"],
        "cmd": "bash"
    }

    output_path = os.path.join(output_dir, "docker", "output")

    generate_from_template('dockerfile.j2', 'Dockerfile', context, output_path)
    generate_from_template('docker-compose.j2', 'docker-compose.yml', context, output_path)
