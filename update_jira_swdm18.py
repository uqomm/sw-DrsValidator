#!/usr/bin/env python3
"""
Script para actualizar SWDM-18 específicamente con la nueva funcionalidad
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
    print("🎯 Actualizando SWDM-18 - Nueva Página de Resultados Detallados")
    print("=" * 60)
    
    updater = JiraUpdater()
    
    # Issue específica
    issue = "SWDM-18"
    
    # Comentario detallado del progreso
    progress_comment = """
📅 Actualización - Octubre 8, 2025

✅ COMPLETADO: Página Dedicada de Resultados Detallados

🎯 Problema Resuelto:
Anteriormente, al hacer clic en "Ver" en un resultado de validación, se mostraba un modal en la misma página, lo cual limitaba la visualización y dificultaba el análisis detallado.

🆕 Implementación:
• Creada nueva página dedicada: /result?id={resultId}
• Template: result-detail.html con diseño profesional
• Apertura en nueva pestaña/ventana para mejor UX
• Endpoint backend: GET /result

📋 Características de la Nueva Página:
• Diseño limpio y profesional con esquema Icinga
• Secciones organizadas:
  - Estadísticas generales (estado, total comandos, tasa éxito)
  - Información completa del dispositivo
  - Resultados detallados por comando con:
    * Tramas hexadecimales enviadas
    * Respuestas hexadecimales recibidas
    * Valores decodificados (JSON)
    * Duración de cada comando
    * Estado individual (PASS/FAIL)

🖨️ Funcionalidades Adicionales:
• Botón "Volver" para regresar a la interfaz principal
• Botón "Imprimir" con formato optimizado para impresión
• Diseño responsive para diferentes tamaños de pantalla
• Colores distintivos por estado (verde/rojo)

💻 Cambios Técnicos:
• Archivo: src/web/templates/result-detail.html (nuevo)
• Modificado: src/validation_app.py (nuevo endpoint)
• Modificado: src/web/static/app-modern.js (viewResult simplificado)
• Commit: cb91b18

📊 Beneficios:
• Mejor análisis de resultados de validación
• No interfiere con el flujo de trabajo principal
• Documentación imprimible de resultados
• Experiencia de usuario mejorada
• Facilita compartir resultados (URL única por resultado)

🔗 Integración:
La funcionalidad se integra perfectamente con el sistema existente de almacenamiento de resultados (JSON) y la API /api/results/{id}.

✨ Estado: Implementado, probado y desplegado en puerto 8089
"""
    
    # Agregar comentario
    print(f"\n📝 Agregando comentario a {issue}...")
    updater.add_comment(issue, progress_comment)
    
    # Agregar worklog
    print(f"\n⏱️  Agregando worklog a {issue}...")
    updater.add_worklog(
        issue,
        "30m",
        "Implementación de página dedicada de resultados detallados. Creación de template HTML, endpoint backend, modificación de JavaScript para abrir en nueva pestaña. Mejora significativa en UX para análisis de validaciones.",
        hours_ago=1
    )
    
    print("\n" + "=" * 60)
    print("✅ Actualización de Jira completada exitosamente")
    print(f"🔗 Ver issue: {updater.jira_url}/browse/{issue}")

if __name__ == "__main__":
    main()
