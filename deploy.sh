#!/bin/bash
set -e

# CBass Deployment Script for VPS
# This script handles deployment of the CBass self-hosted AI stack

echo "=== CBass Deployment Script ==="
echo ""

# Configuration
PROFILE="${PROFILE:-gpu-nvidia}"
ENVIRONMENT="${ENVIRONMENT:-public}"
REPO_URL="https://github.com/mdc159/cbass.git"
DEPLOY_DIR="/opt/cbass"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Helper functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    log_error "Please run as root (use sudo)"
    exit 1
fi

# Check prerequisites
log_info "Checking prerequisites..."

if ! command -v docker &> /dev/null; then
    log_error "Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    log_error "Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

if ! command -v git &> /dev/null; then
    log_error "Git is not installed. Please install Git first."
    exit 1
fi

log_info "All prerequisites met."

# Create deployment directory if it doesn't exist
if [ ! -d "$DEPLOY_DIR" ]; then
    log_info "Creating deployment directory: $DEPLOY_DIR"
    mkdir -p "$DEPLOY_DIR"
fi

cd "$DEPLOY_DIR"

# Clone or update repository
if [ ! -d ".git" ]; then
    log_info "Cloning repository..."
    git clone "$REPO_URL" .
else
    log_info "Updating repository..."
    git fetch origin
    git reset --hard origin/master
fi

# Check for .env file
if [ ! -f ".env" ]; then
    log_warn ".env file not found!"
    log_info "Copying env.example to .env..."
    cp env.example .env
    log_warn "IMPORTANT: Edit .env and set all required variables before continuing!"
    log_warn "Required variables: N8N_ENCRYPTION_KEY, JWT_SECRET, POSTGRES_PASSWORD, etc."
    log_warn "Run: nano .env"
    exit 1
fi

# Validate .env has no @ in POSTGRES_PASSWORD
if grep -q "POSTGRES_PASSWORD=.*@" .env; then
    log_error "POSTGRES_PASSWORD contains @ symbol which breaks connection strings!"
    log_error "Please edit .env and remove @ from POSTGRES_PASSWORD"
    exit 1
fi

# Stop existing containers
log_info "Stopping existing containers..."
python3 start_services.py --profile "$PROFILE" --environment "$ENVIRONMENT" || true
docker compose -p localai down || true

# Pull latest images
log_info "Pulling latest Docker images..."
docker compose -p localai pull

# Start services
log_info "Starting CBass stack with profile: $PROFILE, environment: $ENVIRONMENT"
python3 start_services.py --profile "$PROFILE" --environment "$ENVIRONMENT"

# Wait for services to be healthy
log_info "Waiting for services to start..."
sleep 30

# Check service health
log_info "Checking service health..."
docker compose -p localai ps

# Show access URLs
echo ""
log_info "=== Deployment Complete ==="
echo ""
log_info "Services are starting. Access them at:"
echo "  - n8n: http://localhost:5678 (or your configured hostname)"
echo "  - Open WebUI: http://localhost:3000"
echo "  - Flowise: http://localhost:3001"
echo ""
log_info "Check logs with: docker compose -p localai logs -f"
log_info "Check status with: docker compose -p localai ps"
echo ""
