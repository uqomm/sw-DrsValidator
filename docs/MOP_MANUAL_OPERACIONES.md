# MOP - Manual de Operaciones y Procedimientos
## DRS Validator Framework - Pruebas de Tarjetas Digitales

**Versión:** 1.0  
**Fecha:** 27 de Noviembre, 2025  
**Proyecto:** SW-DrsValidator  
**Issue:** ID-1267  

---

## 📋 Tabla de Contenidos

1. [Introducción](#introducción)
2. [Requisitos Previos](#requisitos-previos)
3. [Procedimientos de Preparación](#procedimientos-de-preparación)
4. [Procedimientos de Validación](#procedimientos-de-validación)
5. [Plantillas de Pruebas](#plantillas-de-pruebas)
6. [Análisis de Resultados](#análisis-de-resultados)
7. [Troubleshooting](#troubleshooting)
8. [Anexos](#anexos)

---

## 1. Introducción

### 1.1 Objetivo del Manual

Este Manual de Operaciones y Procedimientos (MOP) describe los pasos necesarios para realizar pruebas de validación de tarjetas digitales DRS (Digital Radio System) utilizando el framework DRS Validator.

### 1.2 Alcance

El manual cubre:
- Configuración del entorno de pruebas
- Ejecución de validaciones de comandos DRS
- Interpretación de resultados
- Procedimientos de troubleshooting
- Plantillas de documentación de pruebas

### 1.3 Sistemas Soportados

| Sistema | Tipo | Comandos | Puerto |
|---------|------|----------|--------|
| VHF Radio | Master/Remote | 23/17 | 65050 |
| P25 Radio | Master/Remote | 23/17 | 65050 |
| LC500 | Master/Remote | 23/17 | 65050 |

---

## 2. Requisitos Previos

### 2.1 Hardware Requerido

✅ **Equipo de Pruebas:**
- PC con Windows/Linux/MacOS
- Conexión de red (Ethernet o WiFi)
- Acceso a dispositivos DRS en red

✅ **Dispositivos DRS:**
- Tarjetas digitales configuradas
- IP accesible desde el equipo de pruebas
- Puerto TCP 65050 abierto

### 2.2 Software Requerido

```bash
# Requisitos base
- Python 3.11+
- Docker (opcional, para entorno contenedorizado)
- Git
- Navegador web moderno (Chrome, Firefox, Edge)

# Dependencias Python
- FastAPI
- Uvicorn
- httpx
- PyYAML
```

### 2.3 Conocimientos Requeridos

| Nivel | Conocimiento | Descripción |
|-------|--------------|-------------|
| 🟢 Básico | Línea de comandos | Ejecutar comandos en terminal |
| 🟢 Básico | Redes TCP/IP | Entender IPs y puertos |
| 🟡 Intermedio | Protocolo Santone | Frames hexadecimales DRS |
| 🟡 Intermedio | Docker | Para deployment (opcional) |

### 2.4 Accesos Requeridos

- [ ] Acceso SSH/físico al dispositivo DRS (para configuración)
- [ ] Credenciales de red corporativa
- [ ] Acceso a Jira (para documentar resultados)
- [ ] Permisos de ejecución en el servidor de pruebas

---

## 3. Procedimientos de Preparación

### 3.1 Instalación del Framework

#### Opción A: Instalación con Docker (Recomendado)

```bash
# 1. Clonar repositorio
git clone https://github.com/uqomm/sw-DrsValidator.git
cd sw-DrsValidator

# 2. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus configuraciones

# 3. Construir y ejecutar contenedor
docker-compose up -d

# 4. Verificar instalación
curl http://localhost:8089/health
```

#### Opción B: Instalación Manual

```bash
# 1. Clonar repositorio
git clone https://github.com/uqomm/sw-DrsValidator.git
cd sw-DrsValidator

# 2. Configurar entorno Python
export PYTHONPATH="$(pwd)/src"

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar aplicación
python -m uvicorn src.validation_app:app --host 0.0.0.0 --port 8089 --reload

# 5. Verificar instalación
curl http://localhost:8089/health
```

### 3.2 Configuración de Dispositivos

#### 3.2.1 Verificar Conectividad

```bash
# Verificar que el dispositivo responde en la red
ping 192.168.11.22

# Verificar que el puerto TCP 65050 está abierto
telnet 192.168.11.22 65050
# O con netcat:
nc -zv 192.168.11.22 65050
```

#### 3.2.2 Configuración de IP Estática (Recomendado)

Para evitar cambios de IP durante las pruebas:

```bash
# En el dispositivo DRS, configurar IP estática
# Ejemplo para sistema Linux embebido:
ifconfig eth0 192.168.11.22 netmask 255.255.255.0
route add default gw 192.168.11.1
```

### 3.3 Preparación de Escenarios de Prueba

#### 3.3.1 Archivo de Configuración

Editar `src/config/validation_scenarios.yaml`:

```yaml
master_commands:
  connectivity:
    - device_id
    - software_version
    - serial_number
  
  performance:
    - temperature
    - voltage_monitor
    - current_monitor
  
  configuration:
    - transmitter_power
    - receiver_sensitivity
    - frequency_offset

remote_commands:
  status:
    - remote_status
    - remote_temperature
    - remote_signal_strength
```

### 3.4 Checklist Pre-Prueba

Antes de iniciar las pruebas, verificar:

- [ ] Framework instalado y funcionando
- [ ] Dispositivo DRS accesible en red
- [ ] Puerto 65050 abierto y respondiendo
- [ ] Escenarios de prueba configurados
- [ ] Documentación de pruebas preparada
- [ ] Jira configurado (si se usa tracking)

---

## 4. Procedimientos de Validación

### 4.1 Validación Básica (Mock Mode)

Para pruebas sin hardware real:

```bash
# Ejecutar validación en modo mock
curl -X POST "http://localhost:8089/api/validate/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "ip_address": "192.168.11.22",
    "command_type": "master",
    "mode": "mock",
    "selected_commands": ["device_id", "temperature", "software_version"]
  }'
```

**Resultado Esperado:**
```json
{
  "overall_status": "PASS",
  "statistics": {
    "total": 3,
    "passed": 3,
    "failed": 0,
    "timeout": 0,
    "error": 0
  }
}
```

### 4.2 Validación en Vivo (Live Mode)

Para pruebas con hardware real:

#### 4.2.1 Validación Individual

```bash
# Validar un solo comando
curl -X POST "http://localhost:8089/api/validate/single" \
  -H "Content-Type: application/json" \
  -d '{
    "ip_address": "192.168.11.22",
    "command": "device_id",
    "mode": "live"
  }'
```

#### 4.2.2 Validación por Lotes (Batch)

```bash
# Validar múltiples comandos Master
curl -X POST "http://localhost:8089/api/validate/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "ip_address": "192.168.11.22",
    "command_type": "master",
    "mode": "live",
    "selected_commands": [
      "device_id",
      "software_version",
      "temperature",
      "voltage_monitor"
    ]
  }'
```

#### 4.2.3 Validación de Comandos Remote

```bash
# Validar comandos Remote
curl -X POST "http://localhost:8089/api/validate/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "ip_address": "192.168.11.22",
    "command_type": "remote",
    "mode": "live",
    "selected_commands": [
      "remote_status",
      "remote_temperature",
      "remote_signal_strength"
    ]
  }'
```

### 4.3 Interfaz Web

#### 4.3.1 Acceso a la Interfaz

1. Abrir navegador: `http://localhost:8089`
2. Seleccionar tipo de comando (Master/Remote)
3. Ingresar IP del dispositivo
4. Seleccionar modo (Mock/Live)
5. Elegir comandos a validar
6. Hacer clic en "Iniciar Validación"

#### 4.3.2 Monitoreo en Tiempo Real

La interfaz web proporciona:
- ✅ Progreso en tiempo real de las validaciones
- 📊 Estadísticas actualizadas dinámicamente
- 🔍 Detalles de cada comando ejecutado
- 📥 Descarga de resultados en JSON

### 4.4 Validación Automatizada con Scripts

Crear script de pruebas automatizadas:

```python
#!/usr/bin/env python3
"""
Script de validación automatizada
"""
import requests
import json
from datetime import datetime

def run_validation_suite(ip_address):
    """Ejecutar suite completa de validaciones"""
    
    base_url = "http://localhost:8089"
    
    # 1. Validar comandos Master
    print("🔍 Validando comandos Master...")
    master_response = requests.post(
        f"{base_url}/api/validate/batch",
        json={
            "ip_address": ip_address,
            "command_type": "master",
            "mode": "live",
            "selected_commands": [
                "device_id",
                "software_version",
                "temperature"
            ]
        }
    )
    
    # 2. Validar comandos Remote
    print("🔍 Validando comandos Remote...")
    remote_response = requests.post(
        f"{base_url}/api/validate/batch",
        json={
            "ip_address": ip_address,
            "command_type": "remote",
            "mode": "live",
            "selected_commands": [
                "remote_status",
                "remote_temperature"
            ]
        }
    )
    
    # 3. Generar reporte
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"validation_report_{timestamp}.json"
    
    with open(report_file, 'w') as f:
        json.dump({
            "master_results": master_response.json(),
            "remote_results": remote_response.json()
        }, f, indent=2)
    
    print(f"✅ Reporte generado: {report_file}")

if __name__ == "__main__":
    run_validation_suite("192.168.11.22")
```

---

## 5. Plantillas de Pruebas

### 5.1 Plantilla de Caso de Prueba (Markdown)

```markdown
# Caso de Prueba: [ID-XXXX]

## Información General
- **ID:** TC-001
- **Fecha:** 2025-11-27
- **Tester:** [Nombre]
- **Dispositivo:** VHF Master Unit
- **IP:** 192.168.11.22

## Objetivo
Validar la correcta lectura del Device ID del dispositivo DRS.

## Pre-condiciones
- [ ] Dispositivo conectado a la red
- [ ] Framework DRS Validator ejecutándose
- [ ] Puerto 65050 accesible

## Pasos de Ejecución
1. Acceder a la interfaz web del validator
2. Seleccionar "Master Commands"
3. Ingresar IP: 192.168.11.22
4. Seleccionar comando: "device_id"
5. Modo: "Live"
6. Ejecutar validación

## Resultado Esperado
- Status: PASS
- Response: Frame hexadecimal válido
- Decoded Value: ID del dispositivo

## Resultado Obtenido
- Status: PASS ✅
- Response: 7E070100970000E8357E
- Decoded Value: Device ID: 0x0097

## Observaciones
Comando ejecutado correctamente. Device ID coincide con documentación.

## Evidencias
- Screenshot: test_device_id_20251127.png
- JSON Result: results/20251127_143025_master_192_168_11_22.json
```

### 5.2 Plantilla de Resultados (CSV)

Crear archivo `validation_results_template.csv`:

```csv
TestID,Fecha,Dispositivo,IP,Comando,Tipo,Modo,Status,ResponseTime,DecodedValue,Observaciones
TC-001,2025-11-27,VHF-Master,192.168.11.22,device_id,Master,Live,PASS,0.234s,0x0097,OK
TC-002,2025-11-27,VHF-Master,192.168.11.22,temperature,Master,Live,PASS,0.189s,25.5°C,Temperatura normal
TC-003,2025-11-27,VHF-Master,192.168.11.22,software_version,Master,Live,PASS,0.201s,v2.3.1,Versión actual
TC-004,2025-11-27,VHF-Remote,192.168.11.22,remote_status,Remote,Live,PASS,0.256s,Online,Conectado
TC-005,2025-11-27,VHF-Remote,192.168.11.22,remote_temperature,Remote,Live,PASS,0.198s,24.8°C,OK
```

### 5.3 Plantilla de Reporte FAT

Ver sección [Anexo A: Plantilla FAT](#anexo-a-plantilla-fat) para documento completo.

---

## 6. Análisis de Resultados

### 6.1 Interpretación de Estados

| Estado | Significado | Acción Requerida |
|--------|-------------|------------------|
| ✅ PASS | Comando exitoso | Continuar con siguiente prueba |
| ❌ FAIL | Comando falló | Verificar conectividad y configuración |
| ⏱️ TIMEOUT | Sin respuesta (>3s) | Revisar red, reintentar |
| ⚠️ ERROR | Error de protocolo | Verificar frame hexadecimal |

### 6.2 Métricas de Calidad

**Criterios de Aceptación:**
- ✅ **Pass Rate:** ≥ 95% de comandos exitosos
- ✅ **Response Time:** < 2 segundos promedio
- ✅ **Timeout Rate:** < 5%
- ✅ **Error Rate:** < 1%

### 6.3 Análisis de Performance

```python
# Script para analizar resultados
import json

def analyze_results(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    stats = data['statistics']
    
    pass_rate = (stats['passed'] / stats['total']) * 100
    avg_time = data.get('average_response_time', 0)
    
    print(f"📊 Análisis de Resultados:")
    print(f"   Pass Rate: {pass_rate:.2f}%")
    print(f"   Tiempo Promedio: {avg_time:.3f}s")
    print(f"   Total Comandos: {stats['total']}")
    
    if pass_rate >= 95:
        print("   ✅ APROBADO")
    else:
        print("   ❌ REPROBADO - Revisar fallos")

analyze_results("results/20251127_143025_master_192_168_11_22.json")
```

---

## 7. Troubleshooting

### 7.1 Problemas Comunes

#### 7.1.1 No se puede conectar al dispositivo

**Síntomas:**
```
ConnectionRefusedError: [Errno 111] Connection refused
```

**Soluciones:**
1. Verificar que el dispositivo está encendido
2. Verificar conectividad de red: `ping 192.168.11.22`
3. Verificar que puerto 65050 está abierto: `telnet 192.168.11.22 65050`
4. Revisar firewall del dispositivo
5. Verificar que no hay otro servicio usando el puerto

#### 7.1.2 Timeout en comandos

**Síntomas:**
```
Status: TIMEOUT
Response: null
```

**Soluciones:**
1. Aumentar timeout en configuración (default: 3s)
2. Verificar carga del dispositivo
3. Reiniciar dispositivo DRS
4. Verificar latencia de red: `ping -c 10 192.168.11.22`

#### 7.1.3 Frame hexadecimal inválido

**Síntomas:**
```
Status: ERROR
Message: Invalid frame format
```

**Soluciones:**
1. Verificar definición de frame en `hex_frames.py`
2. Revisar CRC del frame
3. Consultar documentación del protocolo Santone
4. Verificar versión de firmware del dispositivo

### 7.2 Logs de Diagnóstico

```bash
# Ver logs de la aplicación
tail -f logs/validation_app.log

# Ver logs de Docker
docker-compose logs -f drs-validation

# Nivel de detalle aumentado
LOG_LEVEL=debug python -m uvicorn src.validation_app:app
```

### 7.3 Contactos de Soporte

| Área | Contacto | Email |
|------|----------|-------|
| Framework | Arturo Veras | arturo@uqomm.com |
| Hardware DRS | Equipo Técnico | soporte@uqomm.com |
| Red/Infraestructura | IT Team | it@uqomm.com |

---

## 8. Anexos

### Anexo A: Plantilla FAT

Ver documento: [FAT_PLANTILLA.md](./FAT_PLANTILLA.md)

### Anexo B: Comandos DRS Completos

Ver documento: [GUIA_TECNICA_COMPLETA.md](./GUIA_TECNICA_COMPLETA.md)

### Anexo C: Protocolo Santone

Ver documento: [PROTOCOLO_VALIDACION_SOFTWARE_SIMPLE.md](./PROTOCOLO_VALIDACION_SOFTWARE_SIMPLE.md)

### Anexo D: Ejemplos de Automatización

```bash
# Script de pruebas nocturnas
#!/bin/bash
# nightly_tests.sh

DEVICES=(
    "192.168.11.22"
    "192.168.11.23"
    "192.168.11.24"
)

for device in "${DEVICES[@]}"; do
    echo "Testing device: $device"
    
    curl -X POST "http://localhost:8089/api/validate/batch" \
      -H "Content-Type: application/json" \
      -d "{
        \"ip_address\": \"$device\",
        \"command_type\": \"master\",
        \"mode\": \"live\",
        \"selected_commands\": [\"device_id\", \"temperature\", \"software_version\"]
      }" > "results/nightly_${device}_$(date +%Y%m%d).json"
    
    sleep 5
done

echo "✅ Nightly tests completed"
```

---

## Control de Versiones

| Versión | Fecha | Autor | Cambios |
|---------|-------|-------|---------|
| 1.0 | 2025-11-27 | Arturo Veras | Versión inicial |

---

**Última actualización:** 27 de Noviembre, 2025  
**Próxima revisión:** 27 de Diciembre, 2025
