import os

from cloud.docker.generators.generate_from_template import generate_from_template


def dockerfile(output_dir: str):
    context = {
        "base_image": "ubuntu:24.04",
        "packages": ["python3", "python3-pip", "curl", "nano"],
        "cmd": "bash"
    }

    output_path = os.path.join(output_dir, "docker", "output")

    generate_from_template('dockerfile.j2', 'Dockerfile', context, output_path)
    print(f"✅ Dockerfile generated at: {output_path}")