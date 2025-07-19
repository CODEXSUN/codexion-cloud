import os
from cloud.docker.generators.generate_from_template import generate_from_template, generate_template_to_string


def docker_compose(output_dir: str):
    service_names = ["mariadb", "cloud", "nginx"]
    volumes = ["cloud_volume", "db_data"]

    output_path = os.path.join(output_dir, "docker", "output")
    os.makedirs(output_path, exist_ok=True)

    service_blocks = ""
    for service_name in service_names:
        template_file = f"{service_name}.j2"
        # No context needed for now
        rendered = generate_template_to_string(template_file, context=None)
        service_blocks += rendered.strip() + "\n"

    full_context = {
        "service_blocks": service_blocks.strip(),
        "volumes": volumes
    }

    generate_from_template("base-compose.j2", "docker-compose.yml", full_context, output_path)
    print(f"✅ docker-compose.yml generated at: {output_path}")
