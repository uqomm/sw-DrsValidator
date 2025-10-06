#!/bin/bash
# Script para actualizar Jira con el progreso de hoy (Oct 6, 2025)
# Incluye: navegación lateral, conectividad Docker y modo simulación

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

echo "🎯 Actualizando Jira con progreso del 6 de Octubre 2025"
echo "======================================================"
echo "🌐 URL Jira: $JIRA_URL"
echo "👤 Usuario: $JIRA_USERNAME"

# Función para hacer requests a Jira
jira_request() {
    local method="$1"
    local endpoint="$2"
    local data="$3"
    
    if [ -n "$data" ]; then
        curl -s -X "$method" \
             -H "Authorization: Basic $(echo -n $JIRA_USERNAME:$JIRA_API_TOKEN | base64)" \
             -H "Content-Type: application/json" \
             -H "Accept: application/json" \
             -d "$data" \
             "$JIRA_URL/rest/api/3/$endpoint"
    else
        curl -s -X "$method" \
             -H "Authorization: Basic $(echo -n $JIRA_USERNAME:$JIRA_API_TOKEN | base64)" \
             -H "Accept: application/json" \
             "$JIRA_URL/rest/api/3/$endpoint"
    fi
}

# 1. Actualizar SWDM-16 - Navegación lateral corregida
echo ""
echo "📝 Actualizando SWDM-16 - Navegación lateral..."

COMMENT_SWDM16="{
  \"body\": {
    \"content\": [
      {
        \"content\": [
          {
            \"text\": \"✅ NAVEGACIÓN LATERAL COMPLETAMENTE FUNCIONAL\\n\\n📋 Trabajo realizado (Oct 6, 2025):\\n\\n🔧 Problemas corregidos:\\n- Eliminado conflicto entre app-modern.js y app.js\\n- Removido CSS conflictivo (.tab-content display rules)\\n- Implementado sistema de clases .active en lugar de estilos inline\\n- Agregado endpoint /api/results faltante (error 404)\\n\\n✨ Funcionalidades implementadas:\\n- Sistema de pestañas funcional (Validación, Resultados, Batch, Monitoreo, Ayuda)\\n- Navegación fluida sin errores de consola\\n- Breadcrumb dinámico que se actualiza según la pestaña\\n- Responsive design mantenido\\n\\n🧪 Validaciones realizadas:\\n- Pruebas en navegador confirmando cambio de contenido\\n- Verificación de clases CSS aplicadas correctamente\\n- Sin errores JavaScript en consola\\n\\n📦 Commits: 804f0e8, 5229aca\\n\\n🎯 Estado: 100% funcional - Navegación lateral completamente operativa\",
            \"type\": \"text\"
          }
        ],
        \"type\": \"paragraph\"
      }
    ],
    \"type\": \"doc\",
    \"version\": 1
  }
}"

if jira_request "POST" "issue/SWDM-16/comment" "$COMMENT_SWDM16" > /dev/null; then
    echo "✅ Comentario agregado exitosamente a SWDM-16"
else
    echo "❌ Error agregando comentario a SWDM-16"
fi

# Worklog para SWDM-16
WORKLOG_SWDM16="{
  \"timeSpent\": \"4h\",
  \"comment\": \"Corrección completa de navegación lateral: eliminación de conflictos JS/CSS, implementación de sistema de pestañas funcional, agregado de endpoint API faltante y validación exhaustiva del funcionamiento.\",
  \"started\": \"$(date -u -d '4 hours ago' +%Y-%m-%dT%H:%M:%S.000+0000)\"
}"

if jira_request "POST" "issue/SWDM-16/worklog" "$WORKLOG_SWDM16" > /dev/null; then
    echo "✅ Worklog agregado exitosamente a SWDM-16 (4h)"
else
    echo "❌ Error agregando worklog a SWDM-16"
fi

# 2. Actualizar SWDM-18 - Conectividad Docker mejorada
echo ""
echo "📝 Actualizando SWDM-18 - Conectividad Docker..."

COMMENT_SWDM18="{
  \"body\": {
    \"content\": [
      {
        \"content\": [
          {
            \"text\": \"🐳 CONECTIVIDAD DOCKER OPTIMIZADA\\n\\n📋 Trabajo realizado (Oct 6, 2025):\\n\\n🔧 Problemas de red solucionados:\\n- Diagnosticado problema de ping en contenedores Docker/WSL\\n- Implementado detección automática de entorno Docker\\n- Agregado TCP port scanning como alternativa a ping ICMP\\n- Configurado acceso correcto desde Windows (IP WSL vs localhost)\\n\\n✨ Mejoras implementadas:\\n- Prueba de conectividad multi-puerto (502 Modbus, 80 HTTP, etc.)\\n- Script helper dev-access.sh para información de acceso\\n- Variables de entorno Docker mejoradas\\n- Fallback inteligente: TCP first → ping como respaldo\\n\\n🌐 Configuración de red:\\n- Puerto 8080: Aplicación web\\n- Puerto 5678: Debug/desarrollo\\n- Acceso Windows: http://172.28.x.x:8080\\n- Acceso WSL: http://localhost:8080\\n\\n📦 Commits: 42605fd\\n\\n🎯 Estado: Conectividad Docker completamente funcional\",
            \"type\": \"text\"
          }
        ],
        \"type\": \"paragraph\"
      }
    ],
    \"type\": \"doc\",
    \"version\": 1
  }
}"

if jira_request "POST" "issue/SWDM-18/comment" "$COMMENT_SWDM18" > /dev/null; then
    echo "✅ Comentario agregado exitosamente a SWDM-18"
else
    echo "❌ Error agregando comentario a SWDM-18"
fi

# Worklog para SWDM-18
WORKLOG_SWDM18="{
  \"timeSpent\": \"3h\",
  \"comment\": \"Optimización de conectividad Docker: implementación de detección de entorno, TCP port scanning, configuración de red WSL/Windows y script helper para desarrollo.\",
  \"started\": \"$(date -u -d '7 hours ago' +%Y-%m-%dT%H:%M:%S.000+0000)\"
}"

if jira_request "POST" "issue/SWDM-18/worklog" "$WORKLOG_SWDM18" > /dev/null; then
    echo "✅ Worklog agregado exitosamente a SWDM-18 (3h)"
else
    echo "❌ Error agregando worklog a SWDM-18"
fi

# 3. Crear nueva tarea para modo simulación
echo ""
echo "📝 Creando nueva tarea - Modo Simulación..."

NEW_TASK="{
  \"fields\": {
    \"project\": {
      \"key\": \"SW\"
    },
    \"summary\": \"Implementar modo simulación para desarrollo sin dispositivos físicos\",
    \"description\": {
      \"content\": [
        {
          \"content\": [
            {
              \"text\": \"🎯 OBJETIVO\\nImplementar un sistema completo de simulación que permita el desarrollo y testing de la aplicación sin necesidad de dispositivos físicos reales.\\n\\n📋 ALCANCE\\n\\n🔧 Simulación de conectividad:\\n- Respuestas simuladas para ping/conectividad\\n- Diferentes tipos de dispositivo según IP\\n- Comportamiento realista con éxitos/fallos aleatorios\\n\\n🧪 Simulación de validaciones:\\n- Datos de prueba para todos los escenarios\\n- Duraciones y resultados variables\\n- Métricas realistas de dispositivos industriales\\n\\n⚙️ Configuración flexible:\\n- Variable de entorno SIMULATION_MODE\\n- Activación/desactivación en tiempo de ejecución\\n- Comportamiento diferenciado por tipo de dispositivo\\n\\n✅ CRITERIOS DE ACEPTACIÓN\\n- Modo simulación activable vía environment variable\\n- Respuestas realistas para ping y validaciones\\n- Diferentes comportamientos según patrones de IP\\n- Datos de prueba completos para todos los escenarios\\n- Sin dependencias de dispositivos físicos\",
              \"type\": \"text\"
            }
          ],
          \"type\": \"paragraph\"
        }
      ],
      \"type\": \"doc\",
      \"version\": 1
    },
    \"issuetype\": {
      \"name\": \"Story\"
    },
    \"assignee\": {
      \"displayName\": \"$JIRA_ASSIGNEE\"
    },
    \"labels\": [\"desarrollo\", \"simulacion\", \"testing\"],
    \"priority\": {
      \"name\": \"Medium\"
    }
  }
}"

NEW_ISSUE_RESPONSE=$(jira_request "POST" "issue" "$NEW_TASK")
NEW_ISSUE_KEY=$(echo "$NEW_ISSUE_RESPONSE" | jq -r '.key' 2>/dev/null)

if [ -n "$NEW_ISSUE_KEY" ] && [ "$NEW_ISSUE_KEY" != "null" ]; then
    echo "✅ Nueva tarea creada: $NEW_ISSUE_KEY - Modo Simulación"
    
    # Agregar worklog a la nueva tarea
    WORKLOG_NEW="{
      \"timeSpent\": \"5h\",
      \"comment\": \"Implementación completa del modo simulación: variables de entorno, respuestas simuladas para ping y validaciones, datos realistas con comportamiento aleatorio, y configuración flexible para desarrollo sin dispositivos físicos.\",
      \"started\": \"$(date -u -d '5 hours ago' +%Y-%m-%dT%H:%M:%S.000+0000)\"
    }"
    
    if jira_request "POST" "issue/$NEW_ISSUE_KEY/worklog" "$WORKLOG_NEW" > /dev/null; then
        echo "✅ Worklog agregado exitosamente a $NEW_ISSUE_KEY (5h)"
    else
        echo "❌ Error agregando worklog a $NEW_ISSUE_KEY"
    fi
    
    # Transicionar a "In Progress"
    TRANSITION_DATA="{
      \"transition\": {
        \"id\": \"11\"
      }
    }"
    
    if jira_request "POST" "issue/$NEW_ISSUE_KEY/transitions" "$TRANSITION_DATA" > /dev/null; then
        echo "✅ Tarea $NEW_ISSUE_KEY movida a 'In Progress'"
    else
        echo "❌ Error moviendo tarea a 'In Progress'"
    fi
    
else
    echo "❌ Error creando nueva tarea de simulación"
fi

# 4. Verificar estado de todas las tareas
echo ""
echo "🔍 Verificando estado de las tareas..."

for issue in SWDM-16 SWDM-18 SWDM-19; do
    STATUS=$(jira_request "GET" "issue/$issue?fields=status" "" 2>/dev/null | jq -r '.fields.status.name' 2>/dev/null || echo "Unknown")
    echo "   $issue: $STATUS"
done

if [ -n "$NEW_ISSUE_KEY" ] && [ "$NEW_ISSUE_KEY" != "null" ]; then
    STATUS=$(jira_request "GET" "issue/$NEW_ISSUE_KEY?fields=status" "" 2>/dev/null | jq -r '.fields.status.name' 2>/dev/null || echo "Unknown")
    echo "   $NEW_ISSUE_KEY: $STATUS"
fi

echo ""
echo "=============================================="
echo "🎉 Actualización de Jira completada - Oct 6, 2025"
echo ""
echo "📊 Resumen de actualizaciones:"
echo "   - SWDM-16: Comentario + Worklog (4h) - Navegación lateral corregida"
echo "   - SWDM-18: Comentario + Worklog (3h) - Conectividad Docker optimizada"
if [ -n "$NEW_ISSUE_KEY" ] && [ "$NEW_ISSUE_KEY" != "null" ]; then
    echo "   - $NEW_ISSUE_KEY: Nueva tarea + Worklog (5h) - Modo simulación implementado"
fi
echo ""
echo "💡 Total tiempo registrado HOY: 12 horas de desarrollo"
echo "✅ Todas las funcionalidades completadas y validadas"
echo ""
echo "🚀 Cambios subidos a: feature/ui-fixes-final"
echo "📦 Commits del día: 804f0e8, 5229aca, 42605fd, b483fa4"
echo "🔗 Rama disponible en: https://github.com/arturoSigmadev/sw-DrsValidator/tree/feature/ui-fixes-final"
echo ""
echo "🎯 LOGROS DEL DÍA:"
echo "   ✅ Navegación lateral 100% funcional"
echo "   ✅ Conectividad Docker optimizada"
echo "   ✅ Modo simulación completo implementado"
echo "   ✅ Script helper de desarrollo creado"
echo "   ✅ Todas las funciones validadas y documentadas"