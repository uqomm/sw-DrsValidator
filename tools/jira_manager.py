#!/usr/bin/env python3
"""
Jira Manager - Herramienta consolidada para gestión de Jira
Gestión completa de issues, worklogs, comentarios y testing de conexión

Uso:
    python jira_manager.py <comando> [opciones]

Comandos disponibles:
    test-connection          - Probar conectividad con Jira
    create-task              - Crear nueva tarea
    preview-task             - Mostrar preview de tarea sin crearla
    add-comment              - Agregar comentario a issue
    add-worklog              - Agregar worklog a issue
    get-issue                - Obtener detalles de issue
    list-projects            - Listar proyectos disponibles

Ejemplos:
    python jira_manager.py test-connection
    python jira_manager.py create-task --type google-drive
    python jira_manager.py add-comment --issue SWDM-19 --comment "Comentario de prueba"
    python jira_manager.py add-worklog --issue SWDM-19 --time "2h" --comment "Trabajo realizado"
"""
import os
import sys
import requests
import base64
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path

def load_env():
    """Cargar variables de entorno desde .env.jira"""
    env_path = Path(__file__).parent / "planning" / ".env.jira"
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

class JiraManager:
    def __init__(self):
        self.env = load_env()
        self.jira_url = self.env.get('JIRA_URL', '')
        self.username = self.env.get('JIRA_USERNAME', '')
        self.api_token = self.env.get('JIRA_API_TOKEN', '')
        self.assignee = self.env.get('JIRA_ASSIGNEE', '')
        self.project_key = self.env.get('JIRA_PROJECT_KEY', 'SWDM')

        if not all([self.jira_url, self.username, self.api_token]):
            raise ValueError("❌ Configuración de Jira incompleta. Revisa planning/.env.jira")

        # Configurar sesión con retry
        self.session = requests.Session()
        retry = requests.adapters.Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = requests.adapters.HTTPAdapter(max_retries=retry)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

        auth_string = f"{self.username}:{self.api_token}"
        encoded_auth = base64.b64encode(auth_string.encode()).decode()

        self.headers = {
            'Authorization': f'Basic {encoded_auth}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def test_connection(self):
        """Probar conectividad con Jira"""
        print("🔍 Probando conectividad con Jira API...")
        print(f"URL: {self.jira_url}")
        print(f"Usuario: {self.username}")
        print(f"Proyecto: {self.project_key}")

        try:
            # Probar obtener información del usuario actual
            response = self.session.get(
                f"{self.jira_url}/rest/api/3/myself",
                headers=self.headers,
                timeout=30
            )

            if response.status_code == 200:
                user_data = response.json()
                print(f"✅ Conexión exitosa - Usuario: {user_data.get('displayName', 'N/A')}")
                print(f"📧 Email: {user_data.get('emailAddress', 'N/A')}")

                # Probar acceso al proyecto
                response = self.session.get(
                    f"{self.jira_url}/rest/api/3/project/{self.project_key}",
                    headers=self.headers,
                    timeout=30
                )

                if response.status_code == 200:
                    project_data = response.json()
                    print(f"✅ Proyecto accesible: {project_data.get('name', 'N/A')}")
                else:
                    print(f"⚠️ Proyecto no accesible: {response.status_code}")

                return True
            else:
                print(f"❌ Error de autenticación: {response.status_code}")
                print(f"Respuesta: {response.text[:200]}")
                return False

        except Exception as e:
            print(f"❌ Error de conexión: {e}")
            return False

    def create_google_drive_task(self):
        """Crear tarea específica para integración con Google Drive"""
        return self.create_task("google-drive")

    def create_task(self, task_type="custom", **kwargs):
        """Crear nueva tarea en Jira"""

        if task_type == "google-drive":
            issue_data = self._get_google_drive_task_data()
        else:
            # Tarea personalizada
            summary = kwargs.get('summary', 'Nueva tarea')
            description = kwargs.get('description', 'Descripción de la tarea')

            issue_data = {
                "fields": {
                    "project": {"key": self.project_key},
                    "summary": summary,
                    "description": {
                        "content": [{
                            "content": [{"text": description, "type": "text"}],
                            "type": "paragraph"
                        }],
                        "type": "doc",
                        "version": 1
                    },
                    "issuetype": {"name": "Task"},
                    "labels": kwargs.get('labels', [])
                }
            }

        # Agregar assignee si está configurado
        if self.assignee:
            issue_data["fields"]["assignee"] = {"name": self.assignee}

        try:
            response = self.session.post(
                f"{self.jira_url}/rest/api/3/issue",
                headers=self.headers,
                json=issue_data,
                timeout=30
            )

            if response.status_code == 201:
                issue = response.json()
                issue_key = issue.get('key')
                print(f"✅ Tarea creada exitosamente: {issue_key}")
                print(f"🔗 URL: {self.jira_url}/browse/{issue_key}")

                # Agregar comentario inicial
                comment_text = f"🎯 Tarea creada el {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                if task_type == "google-drive":
                    comment_text += "\n\nEsta integración permitirá mantener sincronizados los cambios del repositorio con la carpeta compartida del equipo en Google Drive, facilitando la colaboración y backup automático."

                self.add_comment(issue_key, comment_text)

                return issue_key
            else:
                print(f"❌ Error creando tarea: {response.status_code}")
                print(f"Respuesta: {response.text[:500]}")
                return None

        except Exception as e:
            print(f"❌ Error de conexión creando tarea: {e}")
            return None

    def _get_google_drive_task_data(self):
        """Obtener datos de tarea para Google Drive"""
        return {
            "fields": {
                "project": {"key": self.project_key},
                "summary": "🔗 Integración con Google Drive - Sincronización automática de cambios",
                "description": {
                    "content": [
                        {
                            "content": [{"text": "Implementar conexión con Google Drive para sincronizar automáticamente los cambios del repositorio a una carpeta compartida en Google Drive.", "type": "text"}],
                            "type": "paragraph"
                        },
                        {
                            "content": [{"text": "h3. 🎯 Objetivos", "type": "text"}],
                            "type": "paragraph"
                        },
                        {
                            "content": [{"text": "• Configurar API de Google Drive\n• Implementar autenticación OAuth2\n• Crear script de sincronización automática\n• Integrar con Git hooks (post-commit)\n• Manejar conflictos de archivos\n• Configurar carpeta compartida del equipo", "type": "text"}],
                            "type": "paragraph"
                        },
                        {
                            "content": [{"text": "h3. ⏱️ Estimación", "type": "text"}],
                            "type": "paragraph"
                        },
                        {
                            "content": [{"text": "• Desarrollo: 3 días\n• Testing: 1 día\n• Documentación: 0.5 días\n• *Total estimado: 4.5 días*", "type": "text"}],
                            "type": "paragraph"
                        }
                    ],
                    "type": "doc",
                    "version": 1
                },
                "issuetype": {"name": "Task"},
                "labels": ["integration", "google-drive", "automation", "ci-cd", "python"]
            }
        }

    def preview_task(self, task_type="google-drive"):
        """Mostrar preview de tarea sin crearla"""
        print("🔍 PREVIEW DE TAREA JIRA" + (" - INTEGRACIÓN GOOGLE DRIVE" if task_type == "google-drive" else ""))
        print("=" * 70)

        if task_type == "google-drive":
            task_data = self._get_google_drive_task_data()
        else:
            print("❌ Tipo de tarea no soportado para preview")
            return

        print("📋 METADATA DE LA TAREA:")
        print(f"   Tipo: {task_data['fields']['issuetype']['name']}")
        print(f"   Proyecto: {task_data['fields']['project']['key']}")
        print(f"   Labels: {', '.join(task_data['fields']['labels'])}")
        print()

        print("📝 TÍTULO:")
        print(f"   {task_data['fields']['summary']}")
        print()

        print("📖 DESCRIPCIÓN:")
        for content_block in task_data['fields']['description']['content']:
            for text_block in content_block['content']:
                if text_block['type'] == 'text':
                    text = text_block['text']
                    if text.startswith('h3. '):
                        print(f"   🔹 {text[4:]}")
                    elif text.startswith('• '):
                        lines = text.split('\n')
                        for line in lines:
                            if line.strip():
                                print(f"      • {line.strip('• ')}")
                    else:
                        print(f"   {text}")
        print()

        print("📅 FECHA DE CREACIÓN PREVISTA:")
        print(f"   {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print()

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
                print(f"✅ Comentario agregado a {issue_key}")
                return True
            else:
                print(f"❌ Error agregando comentario: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Error de conexión: {e}")
            return False

    def add_worklog(self, issue_key, time_spent, description="", hours_ago=1):
        """Agregar worklog a una issue"""
        # Calcular tiempo de inicio
        start_time = datetime.now() - timedelta(hours=hours_ago)
        started = start_time.strftime("%Y-%m-%dT%H:%M:%S.000+0000")

        worklog_data = {
            "timeSpent": time_spent,
            "started": started,
            "comment": {
                "content": [
                    {
                        "content": [
                            {
                                "text": description or f"Worklog: {time_spent}",
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
                f"{self.jira_url}/rest/api/3/issue/{issue_key}/worklog",
                headers=self.headers,
                json=worklog_data,
                timeout=30
            )

            if response.status_code == 201:
                print(f"✅ Worklog agregado a {issue_key}: {time_spent}")
                return True
            else:
                print(f"❌ Error agregando worklog: {response.status_code}")
                print(f"Respuesta: {response.text[:200]}")
                return False

        except Exception as e:
            print(f"❌ Error de conexión: {e}")
            return False

    def get_issue(self, issue_key):
        """Obtener detalles de una issue"""
        try:
            response = self.session.get(
                f"{self.jira_url}/rest/api/3/issue/{issue_key}",
                headers=self.headers,
                timeout=30
            )

            if response.status_code == 200:
                issue = response.json()
                print(f"📋 Issue: {issue_key}")
                print(f"📝 Título: {issue['fields']['summary']}")
                print(f"📊 Estado: {issue['fields']['status']['name']}")
                print(f"👤 Asignado: {issue['fields'].get('assignee', {}).get('displayName', 'No asignado') if issue['fields'].get('assignee') else 'No asignado'}")
                print(f"🔗 URL: {self.jira_url}/browse/{issue_key}")

                # Mostrar descripción si existe
                description = issue['fields'].get('description')
                if description and 'content' in description:
                    print("📖 Descripción:")
                    for block in description['content'][:2]:  # Solo primeros 2 bloques
                        if 'content' in block:
                            for text_block in block['content']:
                                if text_block.get('type') == 'text':
                                    text = text_block['text'][:100]
                                    print(f"   {text}{'...' if len(text_block['text']) > 100 else ''}")
                return True
            else:
                print(f"❌ Error obteniendo issue: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Error de conexión: {e}")
            return False

    def list_projects(self):
        """Listar proyectos disponibles"""
        try:
            response = self.session.get(
                f"{self.jira_url}/rest/api/3/project",
                headers=self.headers,
                timeout=30
            )

            if response.status_code == 200:
                projects = response.json()
                print("📂 PROYECTOS DISPONIBLES:")
                print("-" * 50)
                for project in projects:
                    print(f"🔑 {project['key']:8} - {project['name']}")
                return True
            else:
                print(f"❌ Error listando proyectos: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Error de conexión: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(
        description="Jira Manager - Herramienta consolidada para gestión de Jira",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python jira_manager.py test-connection
  python jira_manager.py create-task --type google-drive
  python jira_manager.py add-comment --issue SWDM-19 --comment "Comentario de prueba"
  python jira_manager.py add-worklog --issue SWDM-19 --time "2h" --comment "Trabajo realizado"
  python jira_manager.py get-issue --issue SWDM-19
  python jira_manager.py list-projects
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Comandos disponibles')

    # Comando test-connection
    subparsers.add_parser('test-connection', help='Probar conectividad con Jira')

    # Comando create-task
    create_parser = subparsers.add_parser('create-task', help='Crear nueva tarea')
    create_parser.add_argument('--type', choices=['google-drive', 'custom'],
                              default='google-drive', help='Tipo de tarea a crear')
    create_parser.add_argument('--summary', help='Título de la tarea (para tipo custom)')
    create_parser.add_argument('--description', help='Descripción de la tarea (para tipo custom)')
    create_parser.add_argument('--labels', nargs='*', help='Labels para la tarea (para tipo custom)')

    # Comando preview-task
    preview_parser = subparsers.add_parser('preview-task', help='Mostrar preview de tarea')
    preview_parser.add_argument('--type', choices=['google-drive'],
                               default='google-drive', help='Tipo de tarea a previsualizar')

    # Comando add-comment
    comment_parser = subparsers.add_parser('add-comment', help='Agregar comentario a issue')
    comment_parser.add_argument('--issue', required=True, help='Issue key (ej: SWDM-19)')
    comment_parser.add_argument('--comment', required=True, help='Texto del comentario')

    # Comando add-worklog
    worklog_parser = subparsers.add_parser('add-worklog', help='Agregar worklog a issue')
    worklog_parser.add_argument('--issue', required=True, help='Issue key (ej: SWDM-19)')
    worklog_parser.add_argument('--time', required=True, help='Tiempo gastado (ej: 2h, 30m, 1d)')
    worklog_parser.add_argument('--comment', help='Comentario del worklog')
    worklog_parser.add_argument('--hours-ago', type=int, default=1,
                               help='Horas atrás para el worklog (default: 1)')

    # Comando get-issue
    issue_parser = subparsers.add_parser('get-issue', help='Obtener detalles de issue')
    issue_parser.add_argument('--issue', required=True, help='Issue key (ej: SWDM-19)')

    # Comando list-projects
    subparsers.add_parser('list-projects', help='Listar proyectos disponibles')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    try:
        manager = JiraManager()

        if args.command == 'test-connection':
            success = manager.test_connection()

        elif args.command == 'create-task':
            if args.type == 'google-drive':
                issue_key = manager.create_google_drive_task()
            else:
                issue_key = manager.create_task(
                    task_type='custom',
                    summary=args.summary,
                    description=args.description,
                    labels=args.labels or []
                )
            success = issue_key is not None

        elif args.command == 'preview-task':
            manager.preview_task(args.type)
            success = True

        elif args.command == 'add-comment':
            success = manager.add_comment(args.issue, args.comment)

        elif args.command == 'add-worklog':
            success = manager.add_worklog(args.issue, args.time, args.comment, args.hours_ago)

        elif args.command == 'get-issue':
            success = manager.get_issue(args.issue)

        elif args.command == 'list-projects':
            success = manager.list_projects()

        if success:
            print("\n✅ Operación completada exitosamente")
        else:
            print("\n❌ Operación fallida")
            sys.exit(1)

    except ValueError as e:
        print(f"❌ Error de configuración: {e}")
        print("💡 Asegúrate de que planning/.env.jira esté correctamente configurado")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()