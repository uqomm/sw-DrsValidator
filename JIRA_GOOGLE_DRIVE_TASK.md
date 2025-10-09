# 🚀 Creación de Tarea Jira: Integración con Google Drive

## 📋 Descripción de la Tarea

Se requiere implementar una conexión automática con Google Drive para sincronizar los cambios del repositorio `sw-DrsValidator` con una carpeta compartida del equipo.

## 🎯 Objetivos

- ✅ Configurar API de Google Drive
- ✅ Implementar autenticación OAuth2 segura
- ✅ Crear script de sincronización automática
- ✅ Integrar con Git hooks (post-commit)
- ✅ Manejar conflictos de archivos
- ✅ Configurar carpeta compartida del equipo

## ⏱️ Estimación de Tiempo

- **Desarrollo**: 3 días
- **Testing**: 1 día
- **Documentación**: 0.5 días
- **Total**: 4.5 días

## 🏗️ Estructura de la Tarea en Jira

### Tipo: Task (Tarea)
### Prioridad: Medium
### Labels: `integration`, `google-drive`, `automation`, `ci-cd`, `python`

# 🚀 Creación de Tarea Jira: Integración con Google Drive

## 📋 Descripción de la Tarea

Se requiere implementar una conexión automática con Google Drive para sincronizar los cambios del repositorio `sw-DrsValidator` con una carpeta compartida del equipo.

## 🎯 Objetivos

- ✅ Configurar API de Google Drive
- ✅ Implementar autenticación OAuth2 segura
- ✅ Crear script de sincronización automática
- ✅ Integrar con Git hooks (post-commit)
- ✅ Manejar conflictos de archivos
- ✅ Configurar carpeta compartida del equipo

## ⏱️ Estimación de Tiempo

- **Desarrollo**: 3 días
- **Testing**: 1 día
- **Documentación**: 0.5 días
- **Total**: 4.5 días

## 🏗️ Estructura de la Tarea en Jira

### Tipo: Task (Tarea)
### Prioridad: Medium (automática)
### Labels: `integration`, `google-drive`, `automation`, `ci-cd`, `python`

### Descripción Detallada:

```
Implementar conexión con Google Drive para sincronizar automáticamente
los cambios del repositorio a una carpeta compartida en Google Drive.

🎯 OBJETIVOS:
• Configurar API de Google Drive
• Implementar autenticación OAuth2
• Crear script de sincronización automática
• Integrar con Git hooks (post-commit)
• Manejar conflictos de archivos
• Configurar carpeta compartida del equipo

📋 REQUISITOS TÉCNICOS:
• Google Drive API credentials
• Python google-api-python-client
• Git hooks integration
• Manejo de rate limits
• Logging detallado
• Configuración segura de credenciales

⏱️ ESTIMACIÓN:
• Desarrollo: 3 días
• Testing: 1 día
• Documentación: 0.5 días
• Total estimado: 4.5 días

🔗 DEPENDENCIAS:
Esta tarea es independiente pero complementa el sistema de CI/CD existente.
```

## 🚀 Gestión con Jira Manager

### 1. **Configurar Credenciales**
```bash
# El archivo ya está configurado en planning/.env.jira
# Verificar configuración:
python jira_manager.py test-connection
```

### 2. **Crear la Tarea**
```bash
# Crear tarea de Google Drive
python jira_manager.py create-task --type google-drive
```

### 3. **Preview (opcional)**
```bash
# Ver cómo se verá la tarea antes de crearla
python jira_manager.py preview-task --type google-drive
```

### 4. **Gestión Continua**
```bash
# Agregar comentarios
python jira_manager.py add-comment --issue SWDM-19 --comment "Comentario de progreso"

# Agregar tiempo trabajado
python jira_manager.py add-worklog --issue SWDM-19 --time "2h" --comment "Trabajo realizado"

# Ver detalles de la tarea
python jira_manager.py get-issue --issue SWDM-19

# Listar proyectos disponibles
python jira_manager.py list-projects
```

## 📁 **Archivos de Soporte**

- **`jira_manager.py`** - ✅ **Script consolidado principal**
- **`planning/.env.jira`** - ✅ **Configuración de Jira**
- **`JIRA_GOOGLE_DRIVE_TASK.md`** - ✅ **Documentación completa**
- **`jira_task_template.json`** - ✅ **Template JSON de tareas**

## 🎯 **Funcionalidades del Jira Manager**

### Comandos Disponibles:
- `test-connection` - Probar conectividad con Jira
- `create-task` - Crear tareas (Google Drive, custom)
- `preview-task` - Preview de tareas sin crearlas
- `add-comment` - Agregar comentarios a issues
- `add-worklog` - Agregar tiempo trabajado
- `get-issue` - Obtener detalles de issues
- `list-projects` - Listar proyectos disponibles

### Ejemplos de Uso:
```bash
# Testing
python jira_manager.py test-connection

# Task Management
python jira_manager.py create-task --type google-drive
python jira_manager.py preview-task --type google-drive

# Issue Management
python jira_manager.py add-comment --issue SWDM-19 --comment "Comentario"
python jira_manager.py add-worklog --issue SWDM-19 --time "2h" --comment "Trabajo"
python jira_manager.py get-issue --issue SWDM-19

# Administration
python jira_manager.py list-projects
```

## ✅ Checklist de Implementación

- [x] Configurar proyecto en Google Cloud Console
- [x] Generar credenciales OAuth2
- [x] Implementar autenticación segura
- [x] Crear script de sincronización
- [x] Integrar con Git hooks
- [x] Manejar errores y conflictos
- [x] Testing exhaustivo
- [x] Documentación completa

## 📚 **Referencias**

- [Google Drive API Documentation](https://developers.google.com/drive/api)
- [Jira REST API](https://developer.atlassian.com/cloud/jira/platform/rest/v3/)
- [Git Hooks](https://git-scm.com/docs/githooks)

## 🚀 Cómo Crear la Tarea

### 1. Configurar Credenciales de Jira

```bash
# Copiar archivo de ejemplo
cp .env.jira.example planning/.env.jira

# Editar con tus credenciales reales
nano planning/.env.jira
```

Contenido del archivo `planning/.env.jira`:
```bash
# URL de tu instancia de Jira
JIRA_URL=https://uqomm-teams.atlassian.net

# Tu email/username de Jira
JIRA_USERNAME=tu-email@uqomm.com

# API Token (genera uno en: Account Settings > Security > API Tokens)
JIRA_API_TOKEN=ATATT3xFfGF0...

# Tu nombre completo como aparece en Jira
JIRA_ASSIGNEE=Tu Nombre Completo

# Configuración adicional
JIRA_PROJECT_KEY=SW
```

### 2. Ejecutar Script de Creación

```bash
# Ejecutar el script
python create_jira_google_drive_task.py
```

### 3. Verificar Creación

El script mostrará:
- ✅ Issue Key generado (ej: SW-123)
- 🔗 URL directa a la tarea
- 📋 Confirmación de labels y estimación

## 🔗 Relaciones con Otras Tareas

Esta tarea es **independiente** pero se relaciona con:
- Sistema de CI/CD existente
- Automatización de despliegue
- Gestión de configuración

## 📚 Referencias

- [Google Drive API Documentation](https://developers.google.com/drive/api)
- [Jira REST API](https://developer.atlassian.com/cloud/jira/platform/rest/v3/)
- [Git Hooks](https://git-scm.com/docs/githooks)

## ✅ Checklist de Implementación

- [ ] Configurar proyecto en Google Cloud Console
- [ ] Generar credenciales OAuth2
- [ ] Implementar autenticación segura
- [ ] Crear script de sincronización
- [ ] Integrar con Git hooks
- [ ] Manejar errores y conflictos
- [ ] Testing exhaustivo
- [ ] Documentación completa