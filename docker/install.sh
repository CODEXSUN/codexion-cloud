#!/bin/bash

set -euo pipefail

PROJECT_NAME="codexion-cloud"
COMPOSE_FILE="docker.yml"

echo ""
echo "Stopping and removing existing containers, volumes, images..."
docker compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" down -v --remove-orphans || true

echo ""
echo "Pruning unused Docker images, containers, volumes..."
docker system prune -af
docker volume prune -f

echo ""
echo "Rebuilding and starting containers..."
docker compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" up --build -d

echo "🧪 Version Info:"
docker run --rm "${PROJECT_NAME}" bash -c "
  echo 'Python:' && python3 --version
  echo 'Pip:' && pip3 --version
  echo 'Node:' && node -v
  echo 'Yarn:' && yarn -v
  echo 'Bench:' && bench --version
  echo 'NGINX:' && nginx -v 2>&1
"

echo ""
echo "Showing container status..."
docker ps -a --filter "name=$PROJECT_NAME"

echo ""
echo "🎉 All services started successfully!"
echo "copy and run in bash"
echo "docker exec -it codexion-cloud bash"
echo "./setup/ifrappe.py"
exit 0