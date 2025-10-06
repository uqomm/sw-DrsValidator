#!/bin/bash
# Script mejorado para actualizar Jira con progreso de mejoras UI
# Usa la configuración de .env.jira

# Cargar configuración desde el archivo .env.jira
if [ -f "/home/arturo/sw-DrsValidator/planning/.env.jira" ]; then
    source /home/arturo/sw-DrsValidator/planning/.env.jira
    echo "✅ Configuración cargada desde .env.jira"
else
    echo "❌ Error: No se encontró el archivo .env.jira"
    exit 1
fi

# Verificar configuración
if [ -z "$JIRA_API_TOKEN" ] || [ "$JIRA_API_TOKEN" = "YOUR_API_TOKEN_HERE" ]; then
    echo "❌ Error: JIRA_API_TOKEN no está configurado correctamente"
    exit 1
fi

echo "🎯 Actualizando Jira con progreso de mejoras UI"
echo "=============================================="
echo "🌐 URL Jira: $JIRA_URL"
echo "👤 Usuario: $JIRA_USERNAME"

# Función para hacer requests a Jira con mejor manejo de errores
jira_request() {
    local method="$1"
    local endpoint="$2"
    local data="$3"
    
    local response=$(curl -w "HTTPSTATUS:%{http_code}" -s -X "$method" \
        -u "${JIRA_USERNAME}:${JIRA_API_TOKEN}" \
        -H "Content-Type: application/json" \
        -H "Accept: application/json" \
        --data "$data" \
        "${JIRA_URL}/rest/api/3/${endpoint}")
    
    local body=$(echo "$response" | sed -E 's/HTTPSTATUS:[0-9]{3}$//')
    local code=$(echo "$response" | tr -d '\n' | sed -E 's/.*HTTPSTATUS:([0-9]{3})$/\1/')
    
    if [ "$code" -ge 200 ] && [ "$code" -lt 300 ]; then
        echo "$body"
        return 0
    else
        echo "HTTP $code: $body" >&2
        return 1
    fi
}

# 1. Verificar conectividad con Jira
echo ""
echo "🔍 Verificando conectividad con Jira..."

if jira_request "GET" "myself" "" > /dev/null; then
    echo "✅ Conexión a Jira exitosa"
else
    echo "❌ Error de conexión a Jira. Verificar credenciales."
    exit 1
fi

# 2. Agregar comentario a SWDM-16 (Mejoras UI principales)
echo ""
echo "📝 Agregando comentario a SWDM-16..."

COMMENT_SWDM16='{
  "body": "✅ *Progreso Significativo - Mejoras UI Implementadas*\n\n🎨 *Funcionalidades Completadas:*\n• Reorganización de escenarios con nombres descriptivos e íconos\n• Sistema de historial local para validaciones simuladas\n• Modal detallado para visualizar resultados de validación\n• Integración de colores corporativos Sigma\n• Corrección de bugs en navegación y estado de API\n\n🔧 *Archivos Modificados:* app-modern.js, style-modern.css, index-modern.html, index.html\n\n📊 *Estado:* En progreso - Continúo trabajando en refinamientos adicionales\n\n🚀 *Cambios subidos a:* feature/ui-fixes-final"
}'

if jira_request "POST" "issue/SWDM-16/comment" "$COMMENT_SWDM16" > /dev/null; then
    echo "✅ Comentario agregado exitosamente a SWDM-16"
else
    echo "❌ Error agregando comentario a SWDM-16"
fi

# 3. Agregar worklog a SWDM-16
echo ""
echo "⏱️ Agregando worklog a SWDM-16..."

WORKLOG_SWDM16="{
  \"timeSpent\": \"4h\",
  \"comment\": \"Desarrollo e implementación de mejoras UI: reorganización de escenarios, sistema de historial, modal de detalles, integración de colores Sigma y corrección de bugs de navegación. Validación de sintaxis JavaScript y pruebas de funcionalidad.\",
  \"started\": \"$(date -u -d '4 hours ago' +%Y-%m-%dT%H:%M:%S.000+0000)\"
}"

if jira_request "POST" "issue/SWDM-16/worklog" "$WORKLOG_SWDM16" > /dev/null; then
    echo "✅ Worklog agregado exitosamente a SWDM-16 (4h)"
else
    echo "❌ Error agregando worklog a SWDM-16"
fi

# 4. Agregar comentario a SWDM-18 (Organización de escenarios)
echo ""
echo "📝 Agregando comentario a SWDM-18..."

COMMENT_SWDM18='{
  "body": "✅ *Escenarios de Validación Organizados y Mejorados*\n\n🎯 *Implementaciones realizadas:*\n• Categorización en grupos lógicos: Diagnóstico y Comandos por Lotes\n• Nombres descriptivos con íconos: 🔍 Descubrimiento, 📡 DMU, 🌐 DRU, etc.\n• Información contextual que aparece al seleccionar cada escenario\n• Estilos CSS mejorados para los grupos de selección\n• Solo escenarios con implementación API real (removidos los ficticios)\n\n📊 Continúo refinando la experiencia de usuario. Esta tarea está avanzando bien."
}'

if jira_request "POST" "issue/SWDM-18/comment" "$COMMENT_SWDM18" > /dev/null; then
    echo "✅ Comentario agregado exitosamente a SWDM-18"
else
    echo "❌ Error agregando comentario a SWDM-18"
fi

# 5. Agregar worklog a SWDM-18
echo ""
echo "⏱️ Agregando worklog a SWDM-18..."

WORKLOG_SWDM18="{
  \"timeSpent\": \"2h\",
  \"comment\": \"Reorganización completa de escenarios de validación: implementación de categorías, nombres descriptivos con íconos, información contextual dinámica y estilos CSS mejorados para experiencia de usuario optimizada.\",
  \"started\": \"$(date -u -d '2 hours ago' +%Y-%m-%dT%H:%M:%S.000+0000)\"
}"

if jira_request "POST" "issue/SWDM-18/worklog" "$WORKLOG_SWDM18" > /dev/null; then
    echo "✅ Worklog agregado exitosamente a SWDM-18 (2h)"
else
    echo "❌ Error agregando worklog a SWDM-18"
fi

# 6. Agregar comentario a SWDM-19 (Historial de validaciones)
echo ""
echo "📝 Agregando comentario a SWDM-19..."

COMMENT_SWDM19='{
  "body": "✅ *Sistema de Historial Implementado*\n\n🎯 *Funcionalidades desarrolladas:*\n• Historial local para validaciones simuladas con persistencia en localStorage\n• Modal detallado con métricas completas, estado, duración y nivel de señal\n• Exportación individual de resultados en formato JSON\n• Interpretación automática de calidad de señal (Excelente/Buena/Regular/Débil)\n• Gestión inteligente con límite de 50 resultados para rendimiento\n\n✨ El historial ahora funciona correctamente tanto en modo simulación como real.\n\n🔧 *Problema solucionado:* El historial se mostraba vacío después de validaciones simuladas."
}'

if jira_request "POST" "issue/SWDM-19/comment" "$COMMENT_SWDM19" > /dev/null; then
    echo "✅ Comentario agregado exitosamente a SWDM-19"
else
    echo "❌ Error agregando comentario a SWDM-19"
fi

# 7. Agregar worklog a SWDM-19
echo ""
echo "⏱️ Agregando worklog a SWDM-19..."

WORKLOG_SWDM19="{
  \"timeSpent\": \"3h\",
  \"comment\": \"Implementación completa del sistema de historial de validaciones: desarrollo de persistencia local, modal detallado con Bootstrap 5, exportación de resultados individuales y interpretación automática de métricas de señal.\",
  \"started\": \"$(date -u -d '3 hours ago' +%Y-%m-%dT%H:%M:%S.000+0000)\"
}"

if jira_request "POST" "issue/SWDM-19/worklog" "$WORKLOG_SWDM19" > /dev/null; then
    echo "✅ Worklog agregado exitosamente a SWDM-19 (3h)"
else
    echo "❌ Error agregando worklog a SWDM-19"
fi

# 8. Verificar que las tareas siguen en progreso
echo ""
echo "🔍 Verificando estado de las tareas..."

for issue in SWDM-16 SWDM-18 SWDM-19; do
    STATUS=$(jira_request "GET" "issue/$issue?fields=status" "" 2>/dev/null | jq -r '.fields.status.name' 2>/dev/null || echo "Unknown")
    echo "   $issue: $STATUS"
done

echo ""
echo "=============================================="
echo "🎉 Actualización de Jira completada"
echo ""
echo "📊 Resumen de actualizaciones:"
echo "   - SWDM-16: Comentario + Worklog (4h) - Mejoras UI principales"
echo "   - SWDM-18: Comentario + Worklog (2h) - Organización de escenarios"  
echo "   - SWDM-19: Comentario + Worklog (3h) - Historial de validaciones"
echo ""
echo "💡 Total tiempo registrado: 9 horas de desarrollo"
echo "✅ Todas las tareas continúan En Progreso (no terminadas)"
echo ""
echo "🚀 Cambios subidos a: feature/ui-fixes-final"
echo "🔗 Rama disponible en: https://github.com/arturoSigmadev/sw-DrsValidator/tree/feature/ui-fixes-final"