#!/bin/bash
# CBass VPS Deployment Script
# Run this script on your VPS after SSH'ing in

set -e  # Exit on error

echo "========================================"
echo "CBass VPS Deployment"
echo "========================================"
echo ""

# Step 1: Update system
echo "[1/8] Updating system..."
apt update && apt upgrade -y

# Step 2: Install Docker
echo "[2/8] Installing Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
else
    echo "Docker already installed"
fi

# Step 3: Install Docker Compose plugin
echo "[3/8] Installing Docker Compose..."
if ! docker compose version &> /dev/null; then
    apt install -y docker-compose-plugin
else
    echo "Docker Compose already installed"
fi

# Step 4: Install Python and Git
echo "[4/8] Installing Python and Git..."
apt install -y python3 python3-pip git

# Step 5: Configure firewall
echo "[5/8] Configuring firewall..."
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable

# Step 6: Clone repository
echo "[6/8] Cloning CBass repository..."
cd /opt
if [ -d "cbass" ]; then
    echo "Repository already exists, pulling latest..."
    cd cbass
    git pull
else
    git clone https://github.com/mdc159/cbass.git
    cd cbass
fi

# Step 7: Create .env file
echo "[7/8] Creating .env file..."
echo "IMPORTANT: You need to create the .env file manually"
echo "Copy the .env file from your local machine or create it from env.example"
echo ""
echo "To transfer .env from your local machine, run this on your LOCAL machine:"
echo "  scp X:\GitHub\CBass\.env root@191.101.0.164:/opt/cbass/.env"
echo ""
echo "Or create it manually:"
echo "  nano /opt/cbass/.env"
echo ""
read -p "Press Enter when .env file is ready..."

# Step 8: Deploy
echo "[8/8] Deploying CBass..."
chmod +x deploy.sh
./deploy.sh --profile cpu --environment public

echo ""
echo "========================================"
echo "Deployment Complete!"
echo "========================================"
echo ""
echo "Services will be accessible at:"
echo "  n8n: http://191.101.0.164:8001"
echo "  Open WebUI: http://191.101.0.164:8002"
echo "  Flowise: http://191.101.0.164:8003"
echo "  Supabase: http://191.101.0.164:8005"
echo "  Langfuse: http://191.101.0.164:8007"
echo "  Neo4j: http://191.101.0.164:8008"
echo ""
echo "To check status: docker compose -p localai ps"
echo "To view logs: docker compose -p localai logs -f"
