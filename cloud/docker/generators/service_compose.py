import os
from cloud.docker.generators.generate_from_template import generate_from_template, generate_template_to_string

def service_compose(output_dir: str):
    service_names = ["mariadb", "cloud", "nginx"]
    networks = ["codexion-network", "external:true"]

    output_path = os.path.join(output_dir, "docker", "output")
    os.makedirs(output_path, exist_ok=True)

    for service in service_names:
        rendered_service = generate_template_to_string(f"{service}.j2")

        context = {
            "service_blocks": rendered_service.strip(),
            "networks": networks,
        }

        output_filename = f"docker-{service}.yml"
        generate_from_template("service-compose.j2", output_filename, context, output_path)
        print(f"✅ {output_filename} generated at: {output_path}")
