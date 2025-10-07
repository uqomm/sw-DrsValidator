# 🚀 Deployment Rápido - DRS Validator

## Resumen de Cambios en esta versión

### ✅ Problemas Resueltos:
1. **Página de Resultados**: Ahora se visualiza correctamente al hacer click
2. **Modo LIVE**: Muestra logs detallados con tramas enviadas, recibidas y decodificadas
3. **Puerto**: Cambiado de 8080 a 8089
4. **UI**: Tema Icinga aplicado (colores azul #10263b y naranja #ff5000)
5. **Ansible**: Deshabilitada configuración de seguridad SSH

### 📦 Commits Recientes:
```
23caa21 Ansible: Disable SSH security hardening to preserve password access
b604f95 Add simple deployment script with sshpass support
45c009b Fix: Results tab visibility + Change port to 8089
a01b156 Fix: Load results automatically when switching to results tab
219bb5d Fix: Added async live mode with detailed WebSocket logging
8aedb32 UI: Icinga theme colors + removed topbar breadcrumb + improved sidebar spacing
```

---

## 🎯 Opciones de Deployment en 192.168.60.140

### **Opción 1: Script Rápido (RECOMENDADO)**

#### Con password en variable de entorno:
```bash
cd /home/arturo/sw-DrsValidator
export SSHPASS='tu_password_aqui'
./quick-deploy.sh
```

#### Sin password (te lo pedirá):
```bash
cd /home/arturo/sw-DrsValidator
./quick-deploy.sh
```

---

### **Opción 2: Comando SSH Directo**

```bash
ssh root@192.168.60.140 << 'EOF'
cd /opt
if [ -d drs-validation ]; then
    cd drs-validation && git pull origin feature/ui-fixes-final
else
    git clone -b feature/ui-fixes-final https://github.com/arturoSigmadev/sw-DrsValidator.git drs-validation && cd drs-validation
fi
docker-compose down
docker-compose up -d --build
docker-compose ps
curl -s http://localhost:8089/api/test
EOF
```

---

### **Opción 3: Ansible**

```bash
cd /home/arturo/sw-DrsValidator/ansible
ansible-playbook -i inventory/hosts.yml playbooks/site.yml --ask-pass --become
# Ingresa el password cuando te lo pida
```

---

### **Opción 4: Paso a Paso Manual**

```bash
# 1. Conectar al servidor
ssh root@192.168.60.140

# 2. Clonar o actualizar código
cd /opt
git clone -b feature/ui-fixes-final https://github.com/arturoSigmadev/sw-DrsValidator.git drs-validation
# O si ya existe:
cd drs-validation
git checkout feature/ui-fixes-final
git pull origin feature/ui-fixes-final

# 3. Verificar que el puerto está configurado
grep 8089 docker-compose.yml  # Debe mostrar "8089:8080"

# 4. Desplegar
docker-compose down
docker-compose up -d --build

# 5. Verificar
docker-compose ps
docker-compose logs --tail=20
curl http://localhost:8089/api/test

# 6. Salir
exit
```

---

## 🔍 Verificación del Deployment

### Desde tu máquina local:
```bash
# Verificar que el servicio responde
curl http://192.168.60.140:8089/api/test

# Debería responder:
# {"status": "success", "message": "DRS Validation API is running", ...}
```

### Desde el navegador:
```
http://192.168.60.140:8089
```

---

## 📊 Comandos Útiles Post-Deployment

### Ver logs en tiempo real:
```bash
ssh root@192.168.60.140 "cd /opt/drs-validation && docker-compose logs -f"
```

### Reiniciar servicio:
```bash
ssh root@192.168.60.140 "cd /opt/drs-validation && docker-compose restart"
```

### Ver estado de contenedores:
```bash
ssh root@192.168.60.140 "cd /opt/drs-validation && docker-compose ps"
```

### Detener servicio:
```bash
ssh root@192.168.60.140 "cd /opt/drs-validation && docker-compose down"
```

### Actualizar a la última versión:
```bash
ssh root@192.168.60.140 "cd /opt/drs-validation && git pull origin feature/ui-fixes-final && docker-compose restart"
```

---

## 🗑️ Eliminar Deployment en 192.168.60.142

Si necesitas eliminar el servicio viejo en 192.168.60.142:

```bash
ssh root@192.168.60.142 << 'EOF'
cd /opt/drs-validation
docker-compose down -v
# Opcional: eliminar directorio
# rm -rf /opt/drs-validation
EOF
```

---

## 🆘 Troubleshooting

### Error: Puerto 8089 ya en uso
```bash
ssh root@192.168.60.140 "docker ps | grep 8089"
# Detener el contenedor que lo usa
ssh root@192.168.60.140 "docker stop <container_id>"
```

### Error: No se puede conectar
```bash
# Verificar conectividad
ping 192.168.60.140
# Verificar SSH
ssh root@192.168.60.140 "echo 'SSH OK'"
```

### Ver logs completos:
```bash
ssh root@192.168.60.140 "cd /opt/drs-validation && docker-compose logs --tail=100"
```

---

## 📝 Notas

- **Puerto**: El servicio ahora corre en el puerto **8089** (8080 está libre)
- **Branch**: `feature/ui-fixes-final`
- **Directorio remoto**: `/opt/drs-validation`
- **Usuario**: `root`
- **Ansible**: Ya NO modifica configuración SSH

---

**Última actualización**: 2025-10-07
