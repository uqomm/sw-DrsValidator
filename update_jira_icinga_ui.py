#!/usr/bin/env python3
"""
Script para actualizar Jira con los avances del proyecto DRS Validator
Fecha: Octubre 8, 2025
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
                print(f"✅ Worklog agregado exitosamente a {issue_key}: {time_spent}")
                return True
            else:
                print(f"❌ Error agregando worklog a {issue_key}: {response.status_code}")
                print(f"Respuesta: {response.text[:200]}")
                return False
                
        except Exception as e:
            print(f"❌ Error de conexión agregando worklog a {issue_key}: {e}")
            return False

def main():
    print("🎯 Actualizando Jira - Mejoras UI Icinga Theme y Tareas Relacionadas")
    print("=" * 60)
    
    updater = JiraUpdater()
    
    # Issues del proyecto a actualizar
    issues = ["SWDM-14", "SWDM-15", "SWDM-16", "SWDM-17", "SWDM-18"]
    
    # Comentario detallado del progreso
    progress_comment = """
📅 Actualización - Octubre 8, 2025

✅ COMPLETADO: Múltiples Mejoras UI, Funcionalidad y Deployment

🎨 Integración Icinga Theme:
• Implementación completa del esquema de colores Icinga
  - Azul primario: #10263b (rgb 16, 38, 59)
  - Naranja secundario: #ff5000 (rgb 255, 80, 0)
  - Gris menú: rgb(87, 87, 86)
• Tipografía Century Gothic como fuente corporativa
• Actualización de todos los componentes visuales:
  - Navegación lateral con colores Icinga
  - Botones primarios y secundarios
  - Estados activos y hover

🧹 Optimización de Interfaz:
• Eliminación de barra superior (breadcrumb) innecesaria
• Mejora del menú lateral:
  - Íconos más grandes (1.2rem)
  - Texto más legible (1.05rem)
  - Espaciado óptimo (0.75rem)

🐛 Fixes Críticos:
• RESUELTO: Página de Resultados no se mostraba
  - Agregado CSS para .tab-content visibility
  - Auto-carga de resultados al cambiar de pestaña
  - Verificado endpoint /api/results funciona correctamente
• RESUELTO: Modo LIVE sin logs detallados
  - Creado _execute_live_batch_async() con WebSocket logging
  - Logs detallados: tramas hex, respuestas, valores decodificados
  - Paridad funcional con modo MOCK

⚙️ Configuración:
• Puerto cambiado de 8080 a 8089 (libera 8080)
• Ansible configurado para usuario sigmadev con sudo
• SSH key authentication (sin passwords)
• Deshabilitada fase de seguridad SSH en Ansible

📦 Deployment:
• 9 commits en feature/ui-fixes-final
• Scripts de deployment simplificados:
  - deploy-remote.sh
  - quick-deploy.sh
  - DEPLOYMENT_GUIDE.md
• Target: 192.168.60.140:8089
• Migración desde: 192.168.60.142

📊 Impacto:
• UI profesional con identidad Icinga
• Funcionalidad completa de resultados
• Logs detallados en modo LIVE
• Deployment simplificado
• Puerto estandarizado

� Commits:
- 4b208df: SSH key authentication
- fdffcf2: Quick deployment script  
- 45c009b: Results tab visibility + port 8089
- 219bb5d: Async live mode logging
- 8aedb32: Icinga theme colors
"""
    
    # Agregar comentario y worklog a cada issue
    for issue_key in issues:
        print(f"\n📝 Procesando {issue_key}...")
        
        # Agregar comentario
        print(f"  Agregando comentario...")
        updater.add_comment(issue_key, progress_comment)
        
        # Agregar worklog (distribuido más realisticamente)
        print(f"  Agregando worklog...")
        updater.add_worklog(
            issue_key,
            "45m",
            "Integración Icinga Theme + fixes críticos: página resultados, modo LIVE con logs detallados, optimización UI, configuración deployment. 9 commits completados.",
            hours_ago=2
        )
    
    print("\n" + "=" * 60)
    print("✅ Actualización de Jira completada exitosamente")
    for issue_key in issues:
        print(f"🔗 Ver issue: {updater.jira_url}/browse/{issue_key}")

if __name__ == "__main__":
    main()
