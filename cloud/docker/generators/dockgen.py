import os

from cloud.docker.generators.dockfile import dockerfile
from cloud.docker.generators.composefile import docker_compose
from cloud.docker.generators.service_compose import service_compose

def run_all(output_dir: str):
    dockerfile(output_dir)
    docker_compose(output_dir)
    service_compose(output_dir)
