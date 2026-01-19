#!/bin/bash
# Update a specific container by pulling latest image and recreating

CONTAINER=$1
VALID_CONTAINERS="open-webui n8n flowise langfuse-web"

if [[ ! " $VALID_CONTAINERS " =~ " $CONTAINER " ]]; then
    echo "ERROR: Invalid container. Valid options: $VALID_CONTAINERS"
    exit 1
fi

cd /opt/cbass

echo "=== Updating $CONTAINER ==="
echo "Step 1: Pulling latest image..."
docker compose -p localai pull $CONTAINER

echo "Step 2: Recreating container..."
docker compose -p localai up -d $CONTAINER

echo "Step 3: Cleaning up old images..."
docker image prune -f

echo "=== Update complete for $CONTAINER ==="
docker ps --filter name=$CONTAINER --format "Name: {{.Names}}\nStatus: {{.Status}}\nImage: {{.Image}}"
