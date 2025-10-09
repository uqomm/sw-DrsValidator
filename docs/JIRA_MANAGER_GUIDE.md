# 🚀 Jira Manager - Guía Completa

## 📋 Descripción

`jira_manager.py` es el script consolidado y unificado para todas las operaciones de gestión de Jira en el proyecto SW-DRS Validator. Reemplaza todos los scripts individuales anteriores con una interfaz CLI consistente y completa.

## 🎯 Funcionalidades

### ✅ Comandos Disponibles

| Comando | Descripción | Parámetros |
|---------|-------------|------------|
| `test-connection` | Probar conectividad con Jira | Ninguno |
| `create-task` | Crear nueva tarea | `--type` (google-drive, custom) |
| `preview-task` | Preview de tarea sin crearla | `--type` (google-drive, custom) |
| `add-comment` | Agregar comentario a issue | `--issue`, `--comment` |
| `add-worklog` | Agregar tiempo trabajado | `--issue`, `--time`, `--comment` |
| `get-issue` | Obtener detalles de issue | `--issue` |
| `list-projects` | Listar proyectos disponibles | Ninguno |

## 🚀 Uso Básico

### 1. **Configuración Inicial**
```bash
# Asegurarse de que el archivo .env.jira esté configurado
# Ubicación: planning/.env.jira
```

### 2. **Script Wrapper (Recomendado)**
```bash
# El script ./jira facilita el uso desde cualquier directorio
cd /ruta/al/proyecto/sw-DrsValidator

# Testing de conexión
./jira test-connection

# Crear tareas
./jira create-task --type google-drive

# Gestionar issues
./jira add-comment --issue SWDM-19 --comment "Comentario de progreso"
./jira add-worklog --issue SWDM-19 --time "2h" --comment "Trabajo realizado"
```

### 3. **Uso Directo con Python**
```bash
# También puedes usar el script directamente
python jira_manager.py test-connection
python jira_manager.py create-task --type google-drive
```

## 📋 Parámetros Detallados

### `--type` (para create-task y preview-task)
- `google-drive`: Crea tarea de integración con Google Drive
- `custom`: Para tareas personalizadas (requiere configuración adicional)

### `--issue` (para add-comment, add-worklog, get-issue)
- Formato: `PROJECT-###` (ej: `SWDM-19`, `SW-123`)

### `--comment` (para add-comment, add-worklog)
- Texto del comentario o descripción del trabajo realizado

### `--time` (para add-worklog)
- Formatos aceptados: `"2h"`, `"30m"`, `"2h 30m"`, `"1d"`

## 🔧 Configuración

### Archivo `.env.jira`
Ubicación: `planning/.env.jira`

```bash
# URL de tu instancia de Jira
JIRA_URL=https://uqomm-teams.atlassian.net

# Tu email/username de Jira
JIRA_USERNAME=arturo@uqomm.com

# API Token (genera uno en: Account Settings > Security > API Tokens)
JIRA_API_TOKEN=ATATT3xFfGF00SCM6kJZ_uFyeLeUgIPTraJ9yqjS8XlaapB4u1IpvUFXq3kCEuroc-5kOWVr9O08ebzox3iZzqtLeS8cMYwIDT8vCylpVWGwJmMm3zTqjwOxbPTqDJ54Oa5vlcZNaYueJy3QfpSyCZpA5QSyR4XEq7K_MG8eR4-Z8ZDtTfmRBDg=5EF84D3B

# Tu nombre completo como aparece en Jira
JIRA_ASSIGNEE="Arturo Armando Veras Olivos"

# Configuración adicional
JIRA_PROJECT_KEY=SWDM
JIRA_PROJECT_URL=https://uqomm-teams.atlassian.net/jira/core/projects/SWDM/summary
```

## 📊 Ejemplos de Flujo de Trabajo

### **Flujo Completo para Nueva Tarea**
```bash
# 1. Verificar conexión
python planning/jira_manager.py test-connection

# 2. Preview de la tarea
python planning/jira_manager.py preview-task --type google-drive

# 3. Crear la tarea
python planning/jira_manager.py create-task --type google-drive

# 4. Agregar comentario inicial
python planning/jira_manager.py add-comment --issue SWDM-XX --comment "Tarea creada exitosamente"

# 5. Registrar tiempo inicial
python planning/jira_manager.py add-worklog --issue SWDM-XX --time "1h" --comment "Análisis y planificación"
```

### **Seguimiento de Progreso**
```bash
# Agregar actualizaciones periódicas
python planning/jira_manager.py add-comment --issue SWDM-XX --comment "Progreso: 50% completado"
python planning/jira_manager.py add-worklog --issue SWDM-XX --time "4h" --comment "Desarrollo de funcionalidad"

# Ver estado actual
python planning/jira_manager.py get-issue --issue SWDM-XX
```

## 🛠️ Troubleshooting

### **Error de Conexión**
```bash
# Verificar credenciales en .env.jira
python planning/jira_manager.py test-connection
```

### **Issue No Encontrado**
```bash
# Verificar el issue key
python planning/jira_manager.py list-projects
python planning/jira_manager.py get-issue --issue CORRECT-KEY
```

### **Permisos Insuficientes**
- Verificar que el usuario tenga permisos para el proyecto
- Revisar configuración de API Token

## 📚 Referencias

- [Jira REST API Documentation](https://developer.atlassian.com/cloud/jira/platform/rest/v3/)
- [API Tokens en Jira](https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/)

## 🔄 Migración desde Scripts Anteriores

Este script consolida la funcionalidad de:
- ❌ `create_jira_google_drive_task.py`
- ❌ `preview_jira_task.py`
- ❌ `update_jira_python.py`
- ❌ `add_worklogs.py`
- ❌ `test_jira_connection.py`
- ❌ `update_jira_icinga_ui.py`
- ❌ `update_jira_swdm18.py`

**Todos los scripts anteriores han sido eliminados.** Use únicamente `jira_manager.py` para todas las operaciones de Jira.