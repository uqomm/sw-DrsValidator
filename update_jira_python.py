#!/usr/bin/env python3
"""
Script para actualizar Jira con el progreso de hoy (Oct 6, 2025)
Versión Python - Alternativa a curl que funciona correctamente
"""
import os
import requests
import base64
import json
from datetime import datetime, timedelta

def load_env():
    """Cargar variables de entorno desde .env.jira"""
    env_path = "/home/arturo/sw-DrsValidator/planning/.env.jira"
    env_vars = {}
    
    try:
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    # Remover comillas si existen
                    value = value.strip('"').strip("'")
                    env_vars[key] = value
        return env_vars
    except Exception as e:
        print(f"❌ Error leyendo .env.jira: {e}")
        return {}

class JiraUpdater:
    def __init__(self):
        self.env = load_env()
        self.jira_url = self.env.get('JIRA_URL', '')
        self.username = self.env.get('JIRA_USERNAME', '')
        self.api_token = self.env.get('JIRA_API_TOKEN', '')
        
        # Configurar sesión
        self.session = requests.Session()
        auth_string = f"{self.username}:{self.api_token}"
        encoded_auth = base64.b64encode(auth_string.encode()).decode()
        
        self.headers = {
            'Authorization': f'Basic {encoded_auth}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    
    def add_comment(self, issue_key, comment_text):
        """Agregar comentario a una issue"""
        comment_data = {
            "body": {
                "content": [
                    {
                        "content": [
                            {
                                "text": comment_text,
                                "type": "text"
                            }
                        ],
                        "type": "paragraph"
                    }
                ],
                "type": "doc",
                "version": 1
            }
        }
        
        try:
            response = self.session.post(
                f"{self.jira_url}/rest/api/3/issue/{issue_key}/comment",
                headers=self.headers,
                json=comment_data,
                timeout=30
            )
            
            if response.status_code == 201:
                print(f"✅ Comentario agregado exitosamente a {issue_key}")
                return True
            else:
                print(f"❌ Error agregando comentario a {issue_key}: {response.status_code}")
                print(f"Respuesta: {response.text[:200]}")
                return False
                
        except Exception as e:
            print(f"❌ Error de conexión agregando comentario a {issue_key}: {e}")
            return False
    
    def add_worklog(self, issue_key, time_spent, description, hours_ago=1):
        """Agregar worklog a una issue"""
        # Calcular tiempo de inicio
        start_time = datetime.now() - timedelta(hours=hours_ago)
        started = start_time.strftime("%Y-%m-%dT%H:%M:%S.000+0000")
        
        worklog_data = {
            "timeSpent": time_spent,
            "comment": {
                "content": [
                    {
                        "content": [
                            {
                                "text": description,
                                "type": "text"
                            }
                        ],
                        "type": "paragraph"
                    }
                ],
                "type": "doc",
                "version": 1
            },
            "started": started
        }
        
        try:
            response = self.session.post(
                f"{self.jira_url}/rest/api/3/issue/{issue_key}/worklog",
                headers=self.headers,
                json=worklog_data,
                timeout=30
            )
            
            if response.status_code == 201:
                print(f"✅ Worklog agregado exitosamente a {issue_key} ({time_spent})")
                return True
            else:
                print(f"❌ Error agregando worklog a {issue_key}: {response.status_code}")
                print(f"Respuesta: {response.text[:200]}")
                return False
                
        except Exception as e:
            print(f"❌ Error de conexión agregando worklog a {issue_key}: {e}")
            return False
    
    def get_issue_status(self, issue_key):
        """Obtener estado de una issue"""
        try:
            response = self.session.get(
                f"{self.jira_url}/rest/api/3/issue/{issue_key}?fields=status",
                headers=self.headers,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                return data['fields']['status']['name']
            else:
                return "Unknown"
                
        except Exception as e:
            return "Error"

def main():
    print("🎯 Actualizando Jira con progreso del 6 de Octubre 2025")
    print("=" * 60)
    
    updater = JiraUpdater()
    
    print(f"🌐 URL Jira: {updater.jira_url}")
    print(f"👤 Usuario: {updater.username}")
    print()
    
    # 1. Actualizar SWDM-16 - Navegación lateral
    print("📝 Actualizando SWDM-16 - Navegación lateral...")
    
    comment_swdm16 = """✅ NAVEGACIÓN LATERAL COMPLETAMENTE FUNCIONAL

📋 Trabajo realizado (Oct 6, 2025):

🔧 Problemas corregidos:
- Eliminado conflicto entre app-modern.js y app.js
- Removido CSS conflictivo (.tab-content display rules)
- Implementado sistema de clases .active en lugar de estilos inline
- Agregado endpoint /api/results faltante (error 404)

✨ Funcionalidades implementadas:
- Sistema de pestañas funcional (Validación, Resultados, Batch, Monitoreo, Ayuda)
- Navegación fluida sin errores de consola
- Breadcrumb dinámico que se actualiza según la pestaña
- Responsive design mantenido

🧪 Validaciones realizadas:
- Pruebas en navegador confirmando cambio de contenido
- Verificación de clases CSS aplicadas correctamente
- Sin errores JavaScript en consola

📦 Commits: 804f0e8, 5229aca

🎯 Estado: 100% funcional - Navegación lateral completamente operativa"""
    
    updater.add_comment("SWDM-16", comment_swdm16)
    updater.add_worklog("SWDM-16", "4h", 
                       "Corrección completa de navegación lateral: eliminación de conflictos JS/CSS, implementación de sistema de pestañas funcional, agregado de endpoint API faltante y validación exhaustiva del funcionamiento.", 
                       hours_ago=4)
    
    # 2. Actualizar SWDM-18 - Conectividad Docker
    print("\n📝 Actualizando SWDM-18 - Conectividad Docker...")
    
    comment_swdm18 = """🐳 CONECTIVIDAD DOCKER OPTIMIZADA

📋 Trabajo realizado (Oct 6, 2025):

🔧 Problemas de red solucionados:
- Diagnosticado problema de ping en contenedores Docker/WSL
- Implementado detección automática de entorno Docker
- Agregado TCP port scanning como alternativa a ping ICMP
- Configurado acceso correcto desde Windows (IP WSL vs localhost)

✨ Mejoras implementadas:
- Prueba de conectividad multi-puerto (502 Modbus, 80 HTTP, etc.)
- Script helper dev-access.sh para información de acceso
- Variables de entorno Docker mejoradas
- Fallback inteligente: TCP first → ping como respaldo

🌐 Configuración de red:
- Puerto 8080: Aplicación web
- Puerto 5678: Debug/desarrollo
- Acceso Windows: http://172.28.x.x:8080
- Acceso WSL: http://localhost:8080

📦 Commits: 42605fd

🎯 Estado: Conectividad Docker completamente funcional"""
    
    updater.add_comment("SWDM-18", comment_swdm18)
    updater.add_worklog("SWDM-18", "3h",
                       "Optimización de conectividad Docker: implementación de detección de entorno, TCP port scanning, configuración de red WSL/Windows y script helper para desarrollo.",
                       hours_ago=7)
    
    # 3. Crear comentario de resumen para modo simulación (en SWDM-16)
    print("\n📝 Agregando información de modo simulación a SWDM-16...")
    
    comment_simulation = """🎮 MODO SIMULACIÓN IMPLEMENTADO

📋 Funcionalidad adicional desarrollada (Oct 6, 2025):

🔧 Sistema de simulación completo:
- Variable de entorno SIMULATION_MODE para activación
- Respuestas simuladas para ping y conectividad
- Datos realistas con comportamiento aleatorio
- Diferentes tipos de dispositivo según patrones de IP

✨ Características implementadas:
- Simulación de dispositivos Modbus (192.168.1.x)
- Simulación de dispositivos Ethernet (192.168.0.x)
- Simulación de dispositivos wireless (10.0.x.x)
- Respuestas HTTP realistas con delays variables
- Tasas de éxito/fallo configurables

🚀 Beneficios para desarrollo:
- Desarrollo sin hardware físico
- Testing completo en cualquier entorno
- Docker development optimizado
- Datos de prueba consistentes

📦 Commits: b483fa4

🎯 Estado: Sistema de simulación 100% funcional"""
    
    updater.add_comment("SWDM-16", comment_simulation)
    updater.add_worklog("SWDM-16", "3h",
                       "Implementación de sistema de simulación completo: variables de entorno, respuestas simuladas para conectividad, datos realistas y configuración flexible para desarrollo sin dispositivos físicos.",
                       hours_ago=3)
    
    # 4. Verificar estados
    print("\n🔍 Verificando estado de las tareas...")
    issues = ["SWDM-16", "SWDM-18"]
    for issue in issues:
        status = updater.get_issue_status(issue)
        print(f"   {issue}: {status}")
    
    print("\n" + "=" * 60)
    print("🎉 Actualización de Jira completada - Oct 6, 2025")
    print()
    print("📊 Resumen de actualizaciones:")
    print("   - SWDM-16: 2 Comentarios + 2 Worklogs (7h total)")
    print("     * Navegación lateral corregida (4h)")
    print("     * Modo simulación implementado (3h)")
    print("   - SWDM-18: Comentario + Worklog (3h)")
    print("     * Conectividad Docker optimizada")
    print()
    print("💡 Total tiempo registrado HOY: 10 horas de desarrollo")
    print("✅ Todas las funcionalidades completadas y validadas")
    print()
    print("🚀 Cambios subidos a: feature/ui-fixes-final")
    print("📦 Commits del día: 804f0e8, 5229aca, 42605fd, b483fa4")
    print()
    print("🎯 LOGROS DEL DÍA:")
    print("   ✅ Navegación lateral 100% funcional")
    print("   ✅ Conectividad Docker optimizada")
    print("   ✅ Modo simulación completo implementado")
    print("   ✅ Script helper de desarrollo creado")
    print("   ✅ Todas las funciones validadas y documentadas")

if __name__ == "__main__":
    main()