# SW-DRS Validator

Sistema de validación completo para tarjetas digitales VHF, P25 y LC500 del proyecto DRS Monitoring.

## 📋 Descripción

Este proyecto contiene el framework de validación para el sistema de monitoreo DRS (Digital Radio System), diseñado para validar la conectividad y funcionalidad de tarjetas digitales VHF, P25 y LC500.

## 🚀 Características

- ✅ Validación TCP/IP puerto 65050
- ✅ Soporte para protocolos VHF, P25 y LC500
- ✅ Monitoreo de LNA/PA
- ✅ Reportes automatizados
- ✅ Interfaz web de monitoreo
- ✅ Tests automatizados
- ✅ API REST completa con documentación automática
- ✅ Despliegue automatizado con Ansible
- ✅ Contenedorización con Docker

## 🏗️ Arquitectura

```
sw-DrsValidator/
├── src/                    # Código fuente principal
│   ├── validation_app.py   # FastAPI application
│   ├── web/                # Interfaz web
│   │   ├── static/         # JavaScript & CSS
│   │   └── templates/      # HTML templates
│   └── config/             # Configuraciones
├── tests/                  # Suite de tests
├── docs/                   # Documentación técnica
├── scripts/                # Scripts de automatización
├── ansible/                # Configuración de despliegue
├── planning/               # Archivos de planificación y Jira
├── docker-compose.yml      # Orquestación de contenedores
└── requirements.txt        # Dependencias Python
```

## 🛠️ Instalación y Desarrollo

### Prerrequisitos
- Python 3.8+
- Docker & Docker Compose
- Git
- Ansible (para despliegue)

### 🚀 Desarrollo Rápido (Hot Reload)

```bash
# Clonar repositorio
git clone https://github.com/arturoSigmadev/sw-DrsValidator.git
cd sw-DrsValidator

# Modo desarrollo con hot reload
./dev.sh
```

### 🐳 Instalación con Docker

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar con Docker
docker-compose up -d
```

### 🔧 Instalación Manual

```bash
cd sw-DrsValidator
source .venv/bin/activate
export PYTHONPATH="$(pwd)/src"
python -m uvicorn validation_app:app --host 0.0.0.0 --port 8080 --reload --log-level info
```

## 🌐 Puntos de Acceso

### Desarrollo
- **Interfaz Web**: http://localhost:8080
- **Health Check**: http://localhost:8080/health
- **Documentación API**: http://localhost:8080/docs

### Producción (MiniPC)
- **Interfaz Web**: http://192.168.60.140:8080
- **API Endpoints**:
  - `POST /api/validation/run` - Ejecutar validación
  - `POST /api/validation/ping/{ip}` - Test de conectividad
  - `POST /api/validation/batch-commands` - Ejecutar comandos batch
  - `GET /api/validation/supported-commands` - Lista de comandos disponibles
  - `GET /api/validation/batch-commands/status` - Estado del sistema

## 🚀 Deployment

### 🔧 Prerequisitos del Servidor

El servidor remoto debe tener:
- Ubuntu/Debian (cualquier versión reciente)
- Acceso SSH configurado
- Usuario con permisos sudo

### 📦 Opción 1: Deploy Rápido con Python (Recomendado para Dev)

```bash
# Deploy a servidor por defecto (192.168.60.140)
python tools/deploy.py

# Deploy personalizado
python tools/deploy.py --host 192.168.11.22 --port 8089 --branch main

# Ver qué se ejecutaría (dry-run)
python tools/deploy.py --dry-run
```

**¿Qué hace `deploy.py`?**
- ✅ Verifica conectividad SSH
- ✅ Instala Git y Docker automáticamente (si no están)
- ✅ Clona/actualiza el repositorio desde GitHub
- ✅ Configura puerto en docker-compose.yml
- ✅ Construye e inicia contenedores
- ✅ Verifica que el servicio esté funcionando

### 🏭 Opción 2: Deploy con Ansible (Producción)

```bash
cd tools/ansible

# Primera vez (instala Docker, Git, usuarios, etc.)
ansible-playbook -i inventory.yml playbooks/setup.yml

# Despliegues posteriores
ansible-playbook -i inventory.yml playbooks/deploy.yml
```

### 🔄 ¿Cuál usar?

| Escenario | Herramienta |
|-----------|-------------|
| **Testing rápido** | `python tools/deploy.py` |
| **Desarrollo local** | `python tools/deploy.py` |
| **Primera instalación servidor** | Ansible `setup.yml` |
| **Deploy a producción** | Ansible `deploy.yml` o `deploy.py` |
| **Múltiples servidores** | Ansible |

### 🎯 Acceso Post-Deployment

Después del deployment, accede a:
- **Web UI**: `http://[servidor]:8089`
- **API Docs**: `http://[servidor]:8089/docs`
- **Health Check**: `http://[servidor]:8089/health`

### 🔍 Comandos Útiles

```bash
# Ver logs
ssh usuario@servidor 'cd /opt/drs-validation && docker-compose logs -f'

# Reiniciar servicio
ssh usuario@servidor 'cd /opt/drs-validation && docker-compose restart'

# Estado de contenedores
ssh usuario@servidor 'cd /opt/drs-validation && docker-compose ps'
```

## 🧪 Testing y Validación

```bash
# Ejecutar tests completos
python -m pytest tests/

# Ejecutar validación específica
python src/main.py --validate-all

# Scripts de testing de API (en planning/)
./planning/test_api.ps1
./planning/test_ping.ps1
```

## 🔄 Flujo de Desarrollo

1. **Hacer cambios** a archivos Python en `src/` o JavaScript en `src/web/static/`
2. **Guardar el archivo** - hot reload reiniciará automáticamente el servidor
3. **Probar en navegador** - refrescar para ver cambios
4. **Revisar logs** en terminal para errores

## 📚 Documentación

- [Documentación Técnica](./docs/DOCUMENTACION_TECNICA.md)
- [Guía de Despliegue](./docs/GUIA_DEPLOYMENT.md)
- [Plan de Mejoras](./planning/PLAN_MEJORA_VALIDATOR_FRAMEWORK.md)
- [Guía de API](./planning/BATCH_COMMANDS_API_GUIDE.md)

## 🔄 CI/CD

Este proyecto utiliza GitHub Actions para:
- ✅ Tests automatizados
- ✅ Validación de código
- ✅ Build de contenedores
- ✅ Despliegue automático

## 📊 Estado del Proyecto

### Releases
- **v1.0.0** - Foundation ✅
- **v1.1.0** - Improvements ✅
- **v1.2.0** - Analytics 🚧
- **v2.0.0** - Production Ready 📋

### Compatibilidad de Tarjetas
- **VHF**: ✅ Compatible (versión 231016-BB1-145-15M-16C-OP8)
- **P25**: ✅ Compatible (versión 231115-BB1-806D851M-18M-16C-OP8)
- **LC500**: ❌ No compatible (FPGA:250529-16A, Software:250530-05)

### API Status
- ✅ `POST /api/validation/batch-commands` - Ejecutar batch de comandos DRS
- ✅ `GET /api/validation/supported-commands` - 28 comandos disponibles 
- ✅ `GET /api/validation/batch-commands/status` - Capacidades del sistema
- ✅ Documentación automática con FastAPI

## 🔧 Resolución de Problemas

### Errores Comunes

**"Module not found":**
```bash
export PYTHONPATH="$(pwd)/src"
```

**"Permission denied" en directorios:**
- Verificar que `results/`, `logs/`, `temp/` existen y son escribibles

**Hot reload no funciona:**
- Asegurar que se ejecuta con `--reload`
- Verificar que los archivos se guardan en directorios observados

**Errores API 404:**
- Verificar endpoints: `/api/validation/run`, no `/api/run-validation`
- Revisar consola del navegador para errores JavaScript

## 📁 Organización de Archivos

### docs/
Documentación técnica y procedimientos:
- **FAT_PLANTILLA.md** - ✅ **Factory Acceptance Test completo**
- **MOP_MANUAL_OPERACIONES.md** - ✅ **Manual de Operaciones y Procedimientos**
- **validation_results_template.csv** - ✅ **Plantilla CSV para tracking de resultados**
- `GUIA_TECNICA_COMPLETA.md` - Documentación técnica del framework
- `GUIA_DEPLOYMENT.md` - Guía de despliegue
- `JIRA_MANAGER_GUIDE.md` - Guía del gestor de Jira
- `brandbook.md` - Brandbook UQOMM con paleta de colores y tipografía

### planning/
Contiene archivos de planificación, Jira y APIs:
- `jira_manager.py` - ✅ **Script consolidado para gestión completa de Jira**
- `setup_jira_simple.sh` - Script de configuración inicial Jira
- `jira_issues_created.txt` - Lista de issues creados
- `REFACTOR_PLAN*.md` - Planes de refactorización
- `test_api.ps1` - Scripts de prueba de API

## 📖 Documentación de Pruebas (FAT + MOP)

### 🧪 Factory Acceptance Test (FAT)

El documento **FAT_PLANTILLA.md** proporciona un template completo para pruebas de aceptación:

**Incluye:**
- ✅ Checklist pre-prueba y condiciones ambientales
- ✅ Pruebas de comandos Master (identificación, monitoreo, estado, configuración)
- ✅ Pruebas de comandos Remote (estado, señal, configuración)
- ✅ Tests de performance (tiempo de respuesta, tasa de éxito, pruebas de estrés)
- ✅ Pruebas funcionales específicas (LNA, PA, alarmas)
- ✅ Secciones de firmas y aprobación
- ✅ Anexos para evidencias y documentación

**Ejemplo de uso:**
```bash
# 1. Copiar plantilla
cp docs/FAT_PLANTILLA.md results/FAT_SITE_001_20251127.md

# 2. Ejecutar validaciones según plantilla
# 3. Completar resultados en el documento
# 4. Anexar archivos JSON generados
# 5. Obtener firmas de aprobación
```

### 📋 Manual de Operaciones (MOP)

El documento **MOP_MANUAL_OPERACIONES.md** es la guía completa para operadores:

**Secciones principales:**
1. **Requisitos Previos** - Hardware, software, conocimientos y accesos necesarios
2. **Procedimientos de Preparación** - Instalación (Docker/manual), configuración de dispositivos
3. **Procedimientos de Validación** - Mock mode, Live mode, interfaz web, scripts automatizados
4. **Plantillas de Pruebas** - Templates en Markdown y CSV para documentar casos de prueba
5. **Análisis de Resultados** - Interpretación de estados, métricas de calidad, scripts de análisis
6. **Troubleshooting** - Problemas comunes y soluciones, logs de diagnóstico
7. **Anexos** - Referencias a FAT, protocolos, ejemplos de automatización

**Ejemplo de seguimiento:**
```bash
# Seguir el MOP paso a paso:
# 1. Verificar requisitos (Sección 2)
# 2. Instalar framework (Sección 3.1)
# 3. Configurar dispositivos (Sección 3.2)
# 4. Ejecutar validaciones (Sección 4)
# 5. Analizar resultados (Sección 6)
# 6. Documentar en CSV (Sección 5)
```

### 📊 Template de Resultados CSV

El archivo **validation_results_template.csv** proporciona:
- 📝 25 casos de prueba de ejemplo con datos realistas
- 📦 Cobertura de dispositivos VHF, P25 y LC500
- ⏱️ Métricas de performance (response time, status)
- 🔍 Observaciones y análisis detallado

**Campos incluidos:**
- TestID, Fecha, Hora, Dispositivo, IP
- Comando, Tipo, Modo, Status
- ResponseTime_ms, HexFrame, DecodedValue
- RangoAceptable, Observaciones, Tester

**Uso recomendado:**
```bash
# 1. Copiar template
cp docs/validation_results_template.csv results/test_results_$(date +%Y%m%d).csv

# 2. Ejecutar validaciones y registrar resultados
# 3. Analizar datos con scripts Python o Excel
# 4. Generar reportes para stakeholders
```

### Gestión de Jira con jira_manager.py

El script `tools/jira_manager.py` es la herramienta unificada para todas las operaciones de Jira:

**Comandos disponibles:**
```bash
# Probar conexión con Jira
python tools/jira_manager.py test-connection

# Buscar issues por JQL
python tools/jira_manager.py search-issues --jql "key=ID-1267"
python tools/jira_manager.py search-issues --jql "project=SWDM AND status='En curso'"

# Obtener detalles de un issue
python tools/jira_manager.py get-issue --issue SWDM-20

# Agregar comentario
python tools/jira_manager.py add-comment --issue SWDM-20 --comment "Actualización de progreso"

# Agregar worklog
python tools/jira_manager.py add-worklog --issue SWDM-20 --time "2h" --comment "Desarrollo de feature"

# Crear tarea
python tools/jira_manager.py create-task --type custom --summary "Nueva tarea" --description "Descripción"

# Listar proyectos
python tools/jira_manager.py list-projects
```

**Ver guía completa:** [docs/JIRA_MANAGER_GUIDE.md](docs/JIRA_MANAGER_GUIDE.md)

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📞 Contacto

**Proyecto:** SW (DRS Monitoring)  
**Jira:** [https://uqomm-teams.atlassian.net/jira/core/projects/SW/summary](https://uqomm-teams.atlassian.net/jira/core/projects/SW/summary)  
**Responsable:** Arturo Armando Veras Olivos  
**Email:** arturo@uqomm.com

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

---

*Última actualización: Noviembre 2025*  
*Issue Relacionado: ID-1267 (Documentación FAT + MOP)*