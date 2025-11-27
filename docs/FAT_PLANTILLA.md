# FAT - Factory Acceptance Test
## Pruebas de Aceptación de Tarjetas Digitales DRS

**Proyecto:** SW-DrsValidator  
**Issue:** ID-1267  
**Versión:** 1.0  
**Fecha de Prueba:** _____________  

---

## 📋 Información del Documento

| Campo | Valor |
|-------|-------|
| **Cliente** | _________________ |
| **Proyecto** | _________________ |
| **Sitio** | _________________ |
| **Fecha de Prueba** | _________________ |
| **Ingeniero Responsable** | _________________ |
| **Testigo del Cliente** | _________________ |

---

## 1. Información del Equipo Bajo Prueba

### 1.1 Datos del Dispositivo

| Parámetro | Valor |
|-----------|-------|
| **Tipo de Equipo** | ☐ VHF Master  ☐ VHF Remote  ☐ P25  ☐ LC500 |
| **Modelo** | _________________ |
| **Número de Serie** | _________________ |
| **Versión de Software** | _________________ |
| **Versión de Hardware** | _________________ |
| **Fecha de Fabricación** | _________________ |
| **Dirección IP** | _________________ |
| **Puerto TCP** | 65050 (default) |

### 1.2 Configuración de Red

```
IP Address:     _________________._________________._________________._________________ / ____
Subnet Mask:    _________________._________________._________________._________________ 
Default Gateway:_________________._________________._________________._________________ 
DNS Primary:    _________________._________________._________________._________________ 
```

---

## 2. Pre-Condiciones de Prueba

### 2.1 Checklist de Preparación

- [ ] Equipo energizado y estabilizado (mínimo 30 minutos)
- [ ] Conexión de red verificada (ping exitoso)
- [ ] Puerto TCP 65050 accesible
- [ ] Framework DRS Validator instalado y funcionando
- [ ] Documentación técnica disponible
- [ ] Ambiente de pruebas preparado
- [ ] Personal técnico presente

### 2.2 Condiciones Ambientales

| Parámetro | Valor Medido | Rango Aceptable | Estado |
|-----------|--------------|-----------------|--------|
| **Temperatura Ambiente** | ______°C | 0°C - 40°C | ☐ OK  ☐ NOK |
| **Humedad Relativa** | ______% | 10% - 90% | ☐ OK  ☐ NOK |
| **Voltaje de Alimentación** | ______V | ±10% nominal | ☐ OK  ☐ NOK |

---

## 3. Pruebas de Conectividad Básica

### 3.1 Test de Red

| Test | Comando | Resultado | Status |
|------|---------|-----------|--------|
| **Ping** | `ping [IP]` | _______ ms | ☐ PASS  ☐ FAIL |
| **Puerto TCP** | `telnet [IP] 65050` | ☐ Conectado  ☐ Rechazado | ☐ PASS  ☐ FAIL |
| **Traceroute** | `traceroute [IP]` | _______ hops | ☐ PASS  ☐ FAIL |

**Observaciones:**
```
_____________________________________________________________________________________
_____________________________________________________________________________________
```

---

## 4. Pruebas de Comandos Master

### 4.1 Comandos de Identificación

| # | Comando | Hex Frame | Resultado | Decoded Value | Response Time | Status |
|---|---------|-----------|-----------|---------------|---------------|--------|
| 1 | **device_id** | 7E070100970000E8357E | | | _____ ms | ☐ PASS ☐ FAIL |
| 2 | **software_version** | 7E07010001010032017E | | | _____ ms | ☐ PASS ☐ FAIL |
| 3 | **hardware_version** | 7E070100010200320F7E | | | _____ ms | ☐ PASS ☐ FAIL |
| 4 | **serial_number** | 7E0701000E000028517E | | | _____ ms | ☐ PASS ☐ FAIL |

**Criterio de Aceptación:** 100% de comandos PASS

**Resultados:**
- Total: ____
- PASS: ____
- FAIL: ____
- % Éxito: ____%

### 4.2 Comandos de Monitoreo

| # | Comando | Hex Frame | Resultado | Decoded Value | Rango Aceptable | Status |
|---|---------|-----------|-----------|---------------|-----------------|--------|
| 5 | **temperature** | 7E070100020002FA00D1267E | | _____°C | -10°C a 60°C | ☐ PASS ☐ FAIL |
| 6 | **voltage_monitor** | 7E070100020003FA00D03E7E | | _____V | 11V a 15V | ☐ PASS ☐ FAIL |
| 7 | **current_monitor** | 7E070100020004FA00CF467E | | _____A | 0A a 5A | ☐ PASS ☐ FAIL |
| 8 | **pa_temperature** | 7E070100020005FA00CE5E7E | | _____°C | -10°C a 80°C | ☐ PASS ☐ FAIL |

**Criterio de Aceptación:** 
- 100% de comandos PASS
- Valores dentro del rango aceptable

**Resultados:**
- Total: ____
- PASS: ____
- FAIL: ____
- % Éxito: ____%

### 4.3 Comandos de Estado

| # | Comando | Hex Frame | Resultado | Decoded Value | Status |
|---|---------|-----------|-----------|---------------|--------|
| 9 | **operational_status** | 7E070100020006FA00CD667E | | | ☐ PASS ☐ FAIL |
| 10 | **alarm_status** | 7E070100020007FA00CC7E7E | | | ☐ PASS ☐ FAIL |
| 11 | **lna_status** | 7E070100020008FA00CB867E | | | ☐ PASS ☐ FAIL |
| 12 | **pa_status** | 7E070100020009FA00CA9E7E | | | ☐ PASS ☐ FAIL |

**Criterio de Aceptación:** 
- 100% de comandos PASS
- Estados dentro de parámetros normales

**Resultados:**
- Total: ____
- PASS: ____
- FAIL: ____
- % Éxito: ____%

### 4.4 Comandos de Configuración (SET)

| # | Comando | Valor a Configurar | Resultado | Verificación | Status |
|---|---------|-------------------|-----------|--------------|--------|
| 13 | **set_transmitter_power** | _____ W | | ☐ Verificado | ☐ PASS ☐ FAIL |
| 14 | **set_frequency** | _____ MHz | | ☐ Verificado | ☐ PASS ☐ FAIL |
| 15 | **set_channel** | _____ | | ☐ Verificado | ☐ PASS ☐ FAIL |

**Criterio de Aceptación:**
- Comando SET ejecutado exitosamente
- Valor configurado verificado con comando GET

**Observaciones:**
```
_____________________________________________________________________________________
_____________________________________________________________________________________
```

---

## 5. Pruebas de Comandos Remote

### 5.1 Comandos de Estado Remote

| # | Comando | Hex Frame | Resultado | Decoded Value | Status |
|---|---------|-----------|-----------|---------------|--------|
| 16 | **remote_status** | 7E0701009A0000C81A7E | | | ☐ PASS ☐ FAIL |
| 17 | **remote_temperature** | 7E070100020002FA00D1267E | | _____°C | ☐ PASS ☐ FAIL |
| 18 | **remote_signal_strength** | 7E0701009C0000CA427E | | _____ dBm | ☐ PASS ☐ FAIL |
| 19 | **remote_link_quality** | 7E0701009D0000CB5A7E | | _____% | ☐ PASS ☐ FAIL |

**Criterio de Aceptación:** 100% de comandos PASS

**Resultados:**
- Total: ____
- PASS: ____
- FAIL: ____
- % Éxito: ____%

### 5.2 Comandos de Configuración Remote

| # | Comando | Valor a Configurar | Resultado | Verificación | Status |
|---|---------|-------------------|-----------|--------------|--------|
| 20 | **remote_set_power** | _____ W | | ☐ Verificado | ☐ PASS ☐ FAIL |
| 21 | **remote_set_frequency** | _____ MHz | | ☐ Verificado | ☐ PASS ☐ FAIL |

**Observaciones:**
```
_____________________________________________________________________________________
_____________________________________________________________________________________
```

---

## 6. Pruebas de Performance

### 6.1 Tiempo de Respuesta

| Métrica | Objetivo | Medición | Status |
|---------|----------|----------|--------|
| **Tiempo de Respuesta Promedio** | < 2.0 s | _______ s | ☐ PASS ☐ FAIL |
| **Tiempo de Respuesta Máximo** | < 3.0 s | _______ s | ☐ PASS ☐ FAIL |
| **Tiempo de Respuesta Mínimo** | > 0.1 s | _______ s | ☐ PASS ☐ FAIL |

### 6.2 Tasa de Éxito

| Métrica | Objetivo | Medición | Status |
|---------|----------|----------|--------|
| **Pass Rate** | ≥ 95% | _______% | ☐ PASS ☐ FAIL |
| **Timeout Rate** | < 5% | _______% | ☐ PASS ☐ FAIL |
| **Error Rate** | < 1% | _______% | ☐ PASS ☐ FAIL |

### 6.3 Prueba de Estrés

**Descripción:** Ejecutar 100 comandos consecutivos sin pausa

| Métrica | Resultado |
|---------|-----------|
| **Comandos Totales** | 100 |
| **Comandos Exitosos** | _______ |
| **Comandos Fallidos** | _______ |
| **Timeouts** | _______ |
| **Pass Rate** | _______% |

**Criterio de Aceptación:** Pass Rate ≥ 95%

**Status:** ☐ PASS  ☐ FAIL

---

## 7. Pruebas Funcionales Específicas

### 7.1 Test de LNA (Low Noise Amplifier)

| Test | Procedimiento | Resultado | Status |
|------|---------------|-----------|--------|
| **LNA Enable** | Activar LNA y verificar estado | | ☐ PASS ☐ FAIL |
| **LNA Disable** | Desactivar LNA y verificar estado | | ☐ PASS ☐ FAIL |
| **LNA Temperature** | Medir temperatura LNA | _____°C | ☐ PASS ☐ FAIL |
| **LNA Gain** | Verificar ganancia LNA | _____ dB | ☐ PASS ☐ FAIL |

### 7.2 Test de PA (Power Amplifier)

| Test | Procedimiento | Resultado | Status |
|------|---------------|-----------|--------|
| **PA Enable** | Activar PA y verificar estado | | ☐ PASS ☐ FAIL |
| **PA Disable** | Desactivar PA y verificar estado | | ☐ PASS ☐ FAIL |
| **PA Temperature** | Medir temperatura PA | _____°C | ☐ PASS ☐ FAIL |
| **PA Output Power** | Verificar potencia de salida | _____ W | ☐ PASS ☐ FAIL |

### 7.3 Test de Alarmas

| Alarma | Trigger | Detección | Resolución | Status |
|--------|---------|-----------|------------|--------|
| **High Temperature** | Simular alta temp. | | | ☐ PASS ☐ FAIL |
| **Low Voltage** | Simular bajo voltaje | | | ☐ PASS ☐ FAIL |
| **Communication Loss** | Desconectar red | | | ☐ PASS ☐ FAIL |

---

## 8. Resultados de Archivos Generados

### 8.1 Archivos JSON de Resultados

| Archivo | Timestamp | Comandos | Pass Rate | Ubicación |
|---------|-----------|----------|-----------|-----------|
| | | | | results/ |
| | | | | results/ |
| | | | | results/ |

### 8.2 Logs de Sistema

| Log File | Tamaño | Errores | Warnings | Ubicación |
|----------|--------|---------|----------|-----------|
| | | | | logs/ |
| | | | | logs/ |

---

## 9. Resumen Ejecutivo

### 9.1 Resultado Global

| Categoría | Total | PASS | FAIL | % Éxito |
|-----------|-------|------|------|---------|
| **Comandos de Identificación** | | | | % |
| **Comandos de Monitoreo** | | | | % |
| **Comandos de Estado** | | | | % |
| **Comandos de Configuración** | | | | % |
| **Comandos Remote** | | | | % |
| **Pruebas de Performance** | | | | % |
| **Pruebas Funcionales** | | | | % |
| **TOTAL GENERAL** | | | | **______%** |

### 9.2 Criterio de Aceptación Final

**Pass Rate Requerido:** ≥ 95%  
**Pass Rate Obtenido:** ______%

**RESULTADO DEL FAT:**  
☐ **APROBADO** - El equipo cumple con todos los criterios de aceptación  
☐ **APROBADO CON OBSERVACIONES** - Ver sección 9.4  
☐ **RECHAZADO** - Ver sección 9.5

### 9.3 Issues Críticos

| ID | Descripción | Severidad | Estado |
|----|-------------|-----------|--------|
| | | ☐ Alta ☐ Media ☐ Baja | ☐ Abierto ☐ Resuelto |
| | | ☐ Alta ☐ Media ☐ Baja | ☐ Abierto ☐ Resuelto |
| | | ☐ Alta ☐ Media ☐ Baja | ☐ Abierto ☐ Resuelto |

### 9.4 Observaciones y Recomendaciones

```
_____________________________________________________________________________________
_____________________________________________________________________________________
_____________________________________________________________________________________
_____________________________________________________________________________________
_____________________________________________________________________________________
```

### 9.5 No Conformidades (si aplica)

| # | Descripción | Causa Raíz | Acción Correctiva | Responsable | Fecha Límite |
|---|-------------|------------|-------------------|-------------|--------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |

---

## 10. Firmas de Aprobación

### 10.1 Equipo Técnico

| Rol | Nombre | Firma | Fecha |
|-----|--------|-------|-------|
| **Ingeniero de Pruebas** | | | |
| **Supervisor Técnico** | | | |
| **QA Engineer** | | | |

### 10.2 Cliente

| Rol | Nombre | Firma | Fecha |
|-----|--------|-------|-------|
| **Representante del Cliente** | | | |
| **Project Manager** | | | |

---

## 11. Anexos

### Anexo A: Evidencias Fotográficas

- [ ] Foto del equipo bajo prueba
- [ ] Foto de la placa de identificación
- [ ] Foto de las conexiones de red
- [ ] Screenshots de resultados de validación

### Anexo B: Documentos de Referencia

- [ ] Manual técnico del equipo
- [ ] Especificaciones del protocolo Santone
- [ ] Guía de instalación
- [ ] MOP - Manual de Operaciones y Procedimientos

### Anexo C: Archivos Digitales

- [ ] Resultados JSON de validaciones
- [ ] Logs de sistema
- [ ] Reportes de performance
- [ ] Script de automatización usado

---

## Control de Versiones del Documento

| Versión | Fecha | Autor | Cambios |
|---------|-------|-------|---------|
| 1.0 | 2025-11-27 | Arturo Veras | Versión inicial |
| | | | |
| | | | |

---

**Documento Generado por:** DRS Validator Framework  
**Issue Relacionado:** ID-1267  
**Última Actualización:** 27 de Noviembre, 2025  

**NOTA:** Este documento debe ser completado durante la ejecución del FAT. Todos los campos marcados con _____ deben ser llenados. Los checkboxes ☐ deben ser marcados según corresponda.
