#!/usr/bin/env python3
"""
Script para agregar solo los worklogs que fallaron
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
                print(f"Respuesta: {response.text[:300]}")
                return False
                
        except Exception as e:
            print(f"❌ Error de conexión agregando worklog a {issue_key}: {e}")
            return False

def main():
    print("⏰ Agregando worklogs faltantes - Oct 6, 2025")
    print("=" * 50)
    
    updater = JiraUpdater()
    
    # Agregar worklogs
    print("📝 Agregando worklogs...")
    
    # SWDM-16 - Navegación lateral
    updater.add_worklog("SWDM-16", "4h", 
                       "Corrección completa de navegación lateral: eliminación de conflictos JS/CSS, implementación de sistema de pestañas funcional, agregado de endpoint API faltante y validación exhaustiva del funcionamiento.", 
                       hours_ago=4)
    
    # SWDM-18 - Conectividad Docker  
    updater.add_worklog("SWDM-18", "3h",
                       "Optimización de conectividad Docker: implementación de detección de entorno, TCP port scanning, configuración de red WSL/Windows y script helper para desarrollo.",
                       hours_ago=7)
    
    # SWDM-16 - Modo simulación
    updater.add_worklog("SWDM-16", "3h",
                       "Implementación de sistema de simulación completo: variables de entorno, respuestas simuladas para conectividad, datos realistas y configuración flexible para desarrollo sin dispositivos físicos.",
                       hours_ago=3)
    
    print("\n✅ Proceso de worklogs completado")

if __name__ == "__main__":
    main()