#!/bin/bash
#
# Deploy DRS Validator to Remote Server
# Simple deployment script without full Ansible installation
#
# Usage: ./deploy-remote.sh [remote-host] [port] [password]
# Example: ./deploy-remote.sh 192.168.60.140 8089 mypassword
#

set -e  # Exit on error

# Configuration
REMOTE_HOST="${1:-192.168.60.140}"
DRS_PORT="${2:-8089}"
SSH_PASSWORD="${3}"
REMOTE_USER="sigmadev"
REMOTE_DIR="/opt/drs-validation"
REPO_URL="https://github.com/arturoSigmadev/sw-DrsValidator.git"
BRANCH="feature/ui-fixes-final"

echo "================================================"
echo "🚀 DRS Validator - Remote Deployment"
echo "================================================"
echo "Target: ${REMOTE_USER}@${REMOTE_HOST}"
echo "Port: ${DRS_PORT}"
echo "Branch: ${BRANCH}"
echo "================================================"
echo ""

# Function to execute remote commands
remote_exec() {
    if [ -n "$SSH_PASSWORD" ]; then
        sshpass -p "$SSH_PASSWORD" ssh -o StrictHostKeyChecking=no ${REMOTE_USER}@${REMOTE_HOST} "$@"
    else
        ssh -o StrictHostKeyChecking=no ${REMOTE_USER}@${REMOTE_HOST} "$@"
    fi
}

# Step 1: Check SSH connectivity
echo "1️⃣  Verificando conectividad SSH..."
if ! remote_exec "echo 'SSH OK'" &> /dev/null; then
    echo "❌ Error: No se puede conectar a ${REMOTE_HOST}"
    echo "   Asegúrate de tener acceso SSH configurado"
    exit 1
fi
echo "   ✅ Conectividad OK"
echo ""

# Step 2: Check if Docker is installed
echo "2️⃣  Verificando Docker en servidor remoto..."
if ! remote_exec "command -v docker &> /dev/null"; then
    echo "❌ Error: Docker no está instalado en el servidor remoto"
    exit 1
fi
echo "   ✅ Docker instalado"
echo ""

# Step 3: Clone or update repository
echo "3️⃣  Actualizando código desde GitHub..."
remote_exec "
    if [ -d ${REMOTE_DIR} ]; then
        cd ${REMOTE_DIR}
        git fetch origin
        git checkout ${BRANCH}
        git pull origin ${BRANCH}
        echo '   ✅ Código actualizado'
    else
        git clone -b ${BRANCH} ${REPO_URL} ${REMOTE_DIR}
        echo '   ✅ Repositorio clonado'
    fi
"
echo ""

# Step 4: Update docker-compose.yml port
echo "4️⃣  Configurando puerto ${DRS_PORT}..."
remote_exec "
    cd ${REMOTE_DIR}
    sed -i 's/- \"[0-9]*:8080\"/- \"${DRS_PORT}:8080\"/' docker-compose.yml
    echo '   ✅ Puerto configurado'
"
echo ""

# Step 5: Stop existing containers
echo "5️⃣  Deteniendo contenedores existentes..."
remote_exec "
    cd ${REMOTE_DIR}
    docker-compose down || true
    echo '   ✅ Contenedores detenidos'
"
echo ""

# Step 6: Build and start containers
echo "6️⃣  Construyendo y iniciando contenedores..."
remote_exec "
    cd ${REMOTE_DIR}
    docker-compose up -d --build
    echo '   ✅ Contenedores iniciados'
"
echo ""

# Step 7: Wait for service to be ready
echo "7️⃣  Esperando que el servicio esté listo..."
sleep 5
echo ""

# Step 8: Verify deployment
echo "8️⃣  Verificando deployment..."
if remote_exec "curl -s http://localhost:${DRS_PORT}/api/test | grep -q success"; then
    echo "   ✅ Servicio funcionando correctamente"
else
    echo "   ⚠️  Advertencia: El servicio puede no estar respondiendo correctamente"
fi
echo ""

# Step 9: Show logs
echo "9️⃣  Últimas líneas del log:"
remote_exec "cd ${REMOTE_DIR} && docker-compose logs --tail=10"
echo ""

# Summary
echo "================================================"
echo "✅ Deployment completado exitosamente!"
echo "================================================"
echo ""
echo "🌐 Acceso al servicio:"
echo "   http://${REMOTE_HOST}:${DRS_PORT}"
echo ""
echo "📊 Comandos útiles:"
echo "   Ver logs:      ssh ${REMOTE_USER}@${REMOTE_HOST} 'cd ${REMOTE_DIR} && docker-compose logs -f'"
echo "   Reiniciar:     ssh ${REMOTE_USER}@${REMOTE_HOST} 'cd ${REMOTE_DIR} && docker-compose restart'"
echo "   Detener:       ssh ${REMOTE_USER}@${REMOTE_HOST} 'cd ${REMOTE_DIR} && docker-compose down'"
echo "   Estado:        ssh ${REMOTE_USER}@${REMOTE_HOST} 'cd ${REMOTE_DIR} && docker-compose ps'"
echo ""
