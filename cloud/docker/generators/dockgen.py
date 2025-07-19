import os
import re
from jinja2 import Environment, FileSystemLoader

# Replace custom blank line tag with real blank line
def remove_jinja_comments(content: str) -> str:
    # Step 1: Replace {# r #} with placeholder
    content = re.sub(r"{#\s*r\s*#}", "@@B@@", content)

    # Step 2: Remove all other Jinja comments
    content = re.sub(r"{#.*?#}", "", content, flags=re.DOTALL)

    return content


def postprocess_rendered(content: str) -> str:
    # Step 1: Convert @@B@@ markers into actual blank lines
    content = content.replace('@@B@@', '\n')

    # Step 2: Normalize excess blank lines (e.g., more than 2 → just 1)
    content = re.sub(r'\n{3,}', '\n\n', content)

    # Step 3: Clean trailing spaces per line
    lines = [line.rstrip() for line in content.splitlines()]
    cleaned = "\n".join(lines)

    return cleaned.strip() + "\n"  # Ensure exactly one trailing newline


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
    pre_output = remove_jinja_comments(rendered)
    rendered_clean = postprocess_rendered(pre_output)

    # Write output
    docker_output_dir = os.path.join(output_dir, "docker", "output")
    os.makedirs(docker_output_dir, exist_ok=True)
    dockerfile_path = os.path.join(docker_output_dir, "Dockerfile")

    print(f"[DEBUG] Writing Dockerfile to: {dockerfile_path}")
    with open(dockerfile_path, "w") as f:
        f.write(rendered_clean)

    print("✅ Dockerfile generated successfully.")
