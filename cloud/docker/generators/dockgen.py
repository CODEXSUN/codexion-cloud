from jinja2 import Environment, FileSystemLoader
import os


def run(output_dir):
    print(f" Running dockgen for: {output_dir}")

    # Load Jinja2 template environment
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    env = Environment(loader=FileSystemLoader(template_dir))

    # Load dockerfile.j2
    template = env.get_template('dockerfile.j2')

    # Define context for template rendering (add as needed)
    context = {
        "base_image": "ubuntu:24.04",
        "packages": ["python3", "python3-pip", "curl", "nano"],
        "cmd": "bash"
    }

    # Render template
    rendered = template.render(context)

    # Save to output directory
    os.makedirs(output_dir, exist_ok=True)
    dockerfile_path = os.path.join(output_dir, "Dockerfile")

    with open(dockerfile_path, "w") as f:
        f.write(rendered)

    print(f"✅ Dockerfile generated at: {dockerfile_path}")
