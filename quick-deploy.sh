#!/bin/bash
#
# Quick Deploy to 192.168.60.140
# Simple one-liner deployment
#
# Usage: 
#   With password: export SSHPASS='your-password' && ./quick-deploy.sh
#   Or manually: ssh root@192.168.60.140 < quick-deploy-commands.sh
#

REMOTE_HOST="192.168.60.140"
REMOTE_USER="sigmadev"
REMOTE_DIR="/opt/drs-validation"
REPO_URL="https://github.com/arturoSigmadev/sw-DrsValidator.git"
BRANCH="feature/ui-fixes-final"

echo "🚀 Quick Deploy to ${REMOTE_HOST}"
echo "=================================="

# Use SSH key authentication (no password)
SSH_CMD="ssh -o StrictHostKeyChecking=no"

# Execute deployment commands
$SSH_CMD ${REMOTE_USER}@${REMOTE_HOST} bash << 'ENDSSH'
set -e
echo "📦 Step 1: Cloning/Updating repository..."
if [ -d /opt/drs-validation ]; then
    cd /opt/drs-validation
    sudo git fetch origin
    sudo git checkout feature/ui-fixes-final
    sudo git pull origin feature/ui-fixes-final
    echo "✅ Repository updated"
else
    cd /opt
    sudo git clone -b feature/ui-fixes-final https://github.com/arturoSigmadev/sw-DrsValidator.git drs-validation
    cd drs-validation
    echo "✅ Repository cloned"
fi

echo ""
echo "🐳 Step 2: Stopping existing containers..."
sudo docker-compose down 2>/dev/null || true
echo "✅ Containers stopped"

echo ""
echo "🔨 Step 3: Building and starting containers..."
sudo docker-compose up -d --build

echo ""
echo "⏳ Step 4: Waiting for service to be ready..."
sleep 5

echo ""
echo "🔍 Step 5: Verifying deployment..."
sudo docker-compose ps

echo ""
if curl -s http://localhost:8089/api/test | grep -q success; then
    echo "✅ Service is responding correctly!"
else
    echo "⚠️  Warning: Service may not be ready yet"
fi

echo ""
echo "================================================"
echo "✅ Deployment completed!"
echo "================================================"
echo "🌐 Access: http://192.168.60.140:8089"
echo ""
ENDSSH

echo ""
echo "Done! ✨"
