# DRS Validator - Ansible Deployment

Herramientas de automatización para despliegue de DRS Validator usando Ansible.

## 🚀 Quick Start

### Primera vez (setup del servidor):
```bash
cd tools/ansible
ansible-playbook -i inventory.yml playbooks/setup.yml
```

### Despliegues posteriores:
```bash
ansible-playbook -i inventory.yml playbooks/deploy.yml

# Con branch específica
ansible-playbook -i inventory.yml playbooks/deploy.yml -e "git_branch=feature/ui-fixes"

# Con puerto específico
ansible-playbook -i inventory.yml playbooks/deploy.yml -e "app_port=8090"
```

## 📊 ¿Cuándo usar cada herramienta?

| Situación | Herramienta |
|-----------|-------------|
| **Primera instalación servidor** | `ansible-playbook setup.yml` |
| **Desarrollo/testing rápido** | `python tools/deploy.py` |
| **Deploy a producción** | `ansible-playbook deploy.yml` |
| **Múltiples servidores** | Ansible |

## 🎯 Targets Disponibles

- **minipc**: Servidor de producción (192.168.60.140)
- **development**: Entorno local (localhost)

## 📁 Estructura

```
tools/ansible/
├── ansible.cfg          # Configuración Ansible
├── inventory.yml        # Definición de servidores
├── playbooks/
│   ├── setup.yml        # Setup inicial del servidor
│   └── deploy.yml       # Despliegue de aplicación
└── README.md           # Esta documentación
```

## 🔧 Requisitos

- Ansible 2.9+
- SSH configurado para acceso a servidores
- Usuario con permisos sudo en servidores remotos

## 📞 Troubleshooting

### Problemas comunes:
- **SSH Connection**: Verificar que las llaves SSH estén configuradas
- **Docker Build**: Revisar logs con `docker-compose logs`
- **Port Conflicts**: Asegurar que el puerto esté disponible
- **Permissions**: Verificar permisos en el directorio de la aplicación

## 🚀 Despliegue Rápido

### Prerequisitos
```bash
# Instalar Ansible
sudo apt update && sudo apt install ansible

# Configurar SSH keys para acceso sin contraseña
ssh-copy-id root@192.168.60.140
```

### Ejecución
```bash
# Desde el directorio ansible/
ansible-playbook -i inventory/hosts.yml playbooks/site.yml --limit minipc

# O ejecución específica por etapas
ansible-playbook -i inventory/hosts.yml playbooks/system-preparation.yml --limit minipc
ansible-playbook -i inventory/hosts.yml playbooks/app-deployment.yml --limit minipc
```

## 🎯 Targets Soportados

### MiniPC (Producción)
- **Host**: `192.168.60.140`
- **Usuario**: `root`
- **Propósito**: Despliegue para técnicos de campo
- **Acceso**: http://192.168.60.140:8080

### Development (Local)
- **Host**: `localhost`
- **Usuario**: `arturo`
- **Propósito**: Testing y desarrollo
- **Acceso**: http://localhost:8080

## 🔧 Configuración

### Variables de Inventario
```yaml
minipc:
  hosts:
    192.168.60.140:
      ansible_user: root
      app_user: drsadmin
      app_port: 8080
```

### Variables de Entorno
Las variables se configuran automáticamente a través de templates:
- **Docker Compose**: Servicios y volúmenes
- **Environment**: Variables de aplicación y logging

## 📦 Componentes Desplegados

1. **Sistema Base**:
   - Usuario `drsadmin` para la aplicación
   - Estructura de directorios en `/opt/drs-validation/`
   - Docker y docker-compose instalados

2. **Aplicación**:
   - DRS Validation Framework containerizado
   - Interfaz web en puerto 8080
   - Volúmenes persistentes para logs y datos

3. **Servicios**:
   - Contenedor con restart automático
   - Health checks configurados
   - Logs centralizados

## 🔍 Verificación

```bash
# Estado del servicio
ssh root@192.168.60.140 "docker ps"

# Health check
curl http://192.168.60.140:8080/health

# Logs
ssh root@192.168.60.140 "docker logs drs-validation-framework-service"
```

## 🚨 Troubleshooting

### Problemas Comunes
1. **SSH Access**: Verificar que las llaves SSH estén configuradas
2. **Docker Build**: Revisar logs con `docker logs <container>`
3. **Port Conflicts**: Asegurar que puerto 8080 esté disponible
4. **Permissions**: Verificar permisos en `/opt/drs-validation/`

### Logs Útiles
```bash
# Logs de despliegue Ansible
ansible-playbook ... -v

# Logs de aplicación
ssh root@192.168.60.140 "tail -f /opt/drs-validation/logs/*.log"
```

## 📚 Más Información

- [Documentación Principal](../../docs/README.md)
- [Guía WSL](../../WSL_WORKFLOW_GUIDE.md)
- [Setup MiniPC](../../docs/setup_master_debian.md)