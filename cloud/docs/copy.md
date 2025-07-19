fix this composefile to use the new mariadb image and add nginx service


# cloud/docker/generators/composefile.py
import os
from cloud.docker.generators.generate_from_template import generate_from_template, generate_template_to_string


def docker_compose(output_dir: str):
    context = {
        "services": [
            "mariadb",
            "cloud",
            "nginx"
        ],
        "volumes": [
            "cloud_volume",
            "db_data"
        ]
    }

    output_path = os.path.join(output_dir, "docker", "output")
    os.makedirs(output_path, exist_ok=True)

    # Combine partials
    service_blocks = ""
    for service_name in context["services"]:

        template_file = f"{service_name}.j2"

        service_yaml = generate_template_to_string(template_file, context={})

        service_blocks += service_yaml + "\n"

    # Final context for base template
    full_context = {
        "service_blocks": service_blocks,
        "volumes": context["volumes"]
    }

    generate_from_template("base-compose.j2", "docker-compose.yml", full_context, output_path)
    print(f"✅ docker-compose.yml generated at: {output_path}")


# (cloud/docker/generators/templates/base-compose.j2)

{#version: '3.8'#}
@@B@@
services:
{% for block in services %}
{{ block }}
{% endfor %}

volumes:
  cloud_volume:
  db_data:



# cloud/docker/generators/templates/mariadb.j2

  mariadb:
    image: mariadb:11.8
    container_name: codexion-db
    restart: unless-stopped
    environment:
      MARIADB_ROOT_PASSWORD: DbPass1@@
    volumes:
      - db_data:/var/lib/mysql
    ports:
      - "3306:3306"

# cloud/docker/generators/templates/cloud.j2

  cloud:
    build:
      context: .
      dockerfile: Dockerfile
    image: codexion-cloud:latest
    container_name: codexion-cloud
    depends_on:
      - mariadb
    ports:
      - "8000:8000"    # Frappe backend
      - "9000:9000"    # Optional: code-server or admin UI
    volumes:
      - cloud_volume:/home/devops
      - ./supervisor:/etc/supervisor/conf.d
    tty: true
    restart: unless-stopped

# cloud/docker/generators/templates/nginx.j2

    nginx:
        image: nginx:latest
        container_name: codexion-nginx
        depends_on:
        - cloud
        ports:
        - "80:80"
        - "443:443"
        volumes:
        - ./nginx.conf:/etc/nginx/nginx.conf
        - cloud_volume:/var/www/html
        restart: unless-stopped










