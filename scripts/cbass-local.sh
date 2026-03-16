#!/bin/bash
# cbass-local.sh — Start/stop the CBASS Docker stack locally
# Usage: cbass-local.sh [start|stop|status|restart]

CBASS_DIR="$HOME/projects/cbass"
PROJECT="localai"
PROFILE="none"        # Ollama runs natively via Homebrew
ENVIRONMENT="private"  # Local dev mode (ports on 127.0.0.1)
LOG_FILE="/tmp/cbass-startup.log"

wait_for_docker() {
    local max_wait=120
    local waited=0
    while ! docker info &>/dev/null; do
        if [ $waited -ge $max_wait ]; then
            echo "ERROR: Docker not ready after ${max_wait}s" >&2
            return 1
        fi
        sleep 2
        waited=$((waited + 2))
    done
    echo "Docker is ready (waited ${waited}s)"
}

cmd_start() {
    echo "Starting CBASS stack..."
    wait_for_docker || exit 1
    cd "$CBASS_DIR" || exit 1
    python3 start_services.py --profile "$PROFILE" --environment "$ENVIRONMENT" 2>&1 | tee "$LOG_FILE"
    # Caddy isn't needed locally (services expose their own ports)
    docker stop caddy 2>/dev/null && docker rm caddy 2>/dev/null
    echo "CBASS stack started. Dashboard: http://localhost:3002"
}

cmd_stop() {
    echo "Stopping CBASS stack..."
    cd "$CBASS_DIR" || exit 1
    docker compose -p "$PROJECT" --env-file .env -f docker-compose.yml down
    # Also stop Supabase containers
    docker compose -p "$PROJECT" --env-file .env -f supabase/docker/docker-compose.yml down
    echo "CBASS stack stopped."
}

cmd_status() {
    docker compose -p "$PROJECT" ps --format 'table {{.Name}}\t{{.Status}}\t{{.Ports}}' 2>/dev/null
    echo ""
    echo "Services not in project '$PROJECT':"
    docker ps --filter "label=com.docker.compose.project" --format '{{.Labels}}' 2>/dev/null \
        | grep -v "$PROJECT" | sort -u | head -5
}

cmd_restart() {
    cmd_stop
    sleep 3
    cmd_start
}

case "${1:-status}" in
    start)   cmd_start ;;
    stop)    cmd_stop ;;
    status)  cmd_status ;;
    restart) cmd_restart ;;
    *)
        echo "Usage: $0 {start|stop|status|restart}"
        exit 1
        ;;
esac
