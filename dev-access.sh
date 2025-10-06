#!/bin/bash

# DRS Validator - Development Access Helper
# Script para obtener las URLs correctas de acceso en WSL

echo "🚀 DRS Validator - Información de Acceso"
echo "=========================================="

# Obtener IP de WSL
WSL_IP=$(ip addr show eth0 | grep inet | grep -v inet6 | awk '{print $2}' | cut -d'/' -f1)

echo ""
echo "📡 URLs de Acceso:"
echo "  - Aplicación Web: http://$WSL_IP:8080"
echo "  - Localhost (WSL): http://localhost:8080"
echo "  - Puerto Debug: $WSL_IP:5678"

echo ""
echo "🐳 Estado del Contenedor:"
docker-compose -f docker-compose.yml -f docker-compose.dev.yml ps

echo ""
echo "🌐 Verificación de Conectividad:"
if curl -s http://localhost:8080/health > /dev/null; then
    echo "  ✅ Aplicación respondiendo correctamente"
else
    echo "  ❌ Aplicación no responde"
fi

echo ""
echo "💡 Instrucciones:"
echo "  1. Desde Windows: Usar http://$WSL_IP:8080"
echo "  2. Desde WSL: Usar http://localhost:8080"
echo "  3. Para debugging: Conectar IDE al puerto $WSL_IP:5678"

echo ""
echo "🔧 Comandos útiles:"
echo "  - Ver logs: docker-compose -f docker-compose.yml -f docker-compose.dev.yml logs -f"
echo "  - Reiniciar: docker-compose -f docker-compose.yml -f docker-compose.dev.yml restart"
echo "  - Detener: docker-compose -f docker-compose.yml -f docker-compose.dev.yml down"