#!/usr/bin/env python3
"""
Script para actualizar Jira con los avances de UI - Icinga Theme y Optimización
Fecha: Octubre 7, 2025
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
    print("🎯 Actualizando Jira - Mejoras UI Icinga Theme")
    print("=" * 60)
    
    updater = JiraUpdater()
    
    # Issues del proyecto (SW-2: CI/CD, SW-3: Verificación)
    # Actualizamos SW-3 que es sobre verificación de funcionalidad
    ui_issue = "SW-3"
    
    # Comentario detallado del progreso
    progress_comment = """
📅 Actualización - Octubre 7, 2025

✅ COMPLETADO: Integración Icinga Theme y Optimización UI

🎨 Cambios de Diseño Icinga:
• Implementación completa del esquema de colores Icinga
  - Azul primario: #10263b (rgb 16, 38, 59)
  - Naranja secundario: #ff5000 (rgb 255, 80, 0)
  - Gris menú: rgb(87, 87, 86)
• Tipografía Century Gothic como fuente corporativa
• Actualización de todos los componentes visuales:
  - Navegación lateral con colores Icinga
  - Botones primarios y secundarios
  - Estados activos y hover
  - Brand y elementos de UI

🧹 Optimización de Interfaz:
• Eliminación de barra superior (breadcrumb) innecesaria
• Mejora del menú lateral:
  - Íconos más grandes (1.2rem)
  - Texto más legible (1.05rem)
  - Espaciado óptimo entre ícono y texto (0.75rem)
• Interfaz más limpia y profesional

📦 Deployment:
• Cambios commiteados y pusheados a feature/ui-fixes-final
• Deployment en progreso via Ansible a 192.168.60.140:8089
• Migración desde servidor anterior (192.168.60.142)

📊 Impacto:
• Consistencia visual con identidad corporativa Icinga
• Mejor experiencia de usuario con interfaz optimizada
• Reducción de elementos visuales innecesarios
• Mayor profesionalismo en la presentación

🔄 Próximos Pasos:
• Validación del deployment en nuevo servidor
• Pruebas de usuario final
• Documentación de cambios visuales
"""
    
    # Agregar comentario
    print(f"\n📝 Agregando comentario a {ui_issue}...")
    updater.add_comment(ui_issue, progress_comment)
    
    # Agregar worklog
    print(f"\n⏱️  Agregando worklog a {ui_issue}...")
    updater.add_worklog(
        ui_issue,
        "2h",
        "Integración completa de Icinga Theme: colores corporativos, tipografía Century Gothic, optimización UI (eliminación breadcrumb, mejora menú lateral). Deployment en progreso.",
        hours_ago=2
    )
    
    print("\n" + "=" * 60)
    print("✅ Actualización de Jira completada exitosamente")
    print(f"🔗 Ver issue: {updater.jira_url}/browse/{ui_issue}")

if __name__ == "__main__":
    main()
