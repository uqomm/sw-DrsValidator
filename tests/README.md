# DRS Validation Test Suite

Suite completa de pruebas para el sistema de validación DRS.

## 📋 Características

- ✅ Tests automatizados para comandos Master, Remote y Set
- ✅ Soporte para modo Mock y Live
- ✅ Validación de tramas hexadecimales reales
- ✅ Test de WebSocket logging en tiempo real
- ✅ Generación de reportes JSON
- ✅ Output colorizado y detallado
- ✅ Selección de tests individuales o suite completa

## 🚀 Uso Rápido

### Ejecutar todos los tests (mock)
```bash
python tests/test_drs_validation_suite.py
```

### Ejecutar test específico
```bash
# Solo test Master
python tests/test_drs_validation_suite.py --test master

# Solo test Remote
python tests/test_drs_validation_suite.py --test remote

# Solo test API endpoint
python tests/test_drs_validation_suite.py --test api

# Solo test WebSocket
python tests/test_drs_validation_suite.py --test websocket
```

### Tests con dispositivo real (modo live)
```bash
# Incluir tests live (requiere dispositivo DRS conectado)
python tests/test_drs_validation_suite.py --live

# Solo tests live de Remote commands
python tests/test_drs_validation_suite.py --test remote --live
```

### Output detallado
```bash
# Ver todos los comandos y valores decodificados
python tests/test_drs_validation_suite.py --verbose

# Verbose + guardar reporte
python tests/test_drs_validation_suite.py --verbose --save-report
```

### Servidor customizado
```bash
# Si el servidor está en otra URL
python tests/test_drs_validation_suite.py --url http://192.168.1.100:8080
```

## 📊 Tipos de Tests

### 1. Master Commands Mock
Valida los 15 comandos DRS Master en modo simulación:
- optical_port_devices_connected_1/2/3/4
- input_and_output_power
- channel_switch
- channel_frequency_configuration
- central_frequency_point
- subband_bandwidth
- broadband_switching
- optical_port_switch
- optical_port_status
- temperature
- device_id
- datt

### 2. Remote Commands Mock
Valida los 13 comandos DRS Remote en modo simulación.

### 3. Batch API Endpoint
Valida el endpoint directo `/api/validation/batch-commands`.

### 4. WebSocket Real-Time Logging
Valida la funcionalidad de logging en tiempo real vía WebSocket.

### 5. Live Validation (Opcional)
Valida comandos contra un dispositivo DRS real conectado.

## 📄 Reportes

Los reportes se guardan en `reports/test_report_YYYYMMDD_HHMMSS.json` y contienen:

```json
{
  "timestamp": "2025-10-07T12:30:45",
  "total_tests": 4,
  "passed": 4,
  "failed": 0,
  "duration_seconds": 12.5,
  "tests": [
    {
      "test_name": "Master Commands Mock",
      "success": true,
      "details": {
        "overall_status": "PASS",
        "statistics": {
          "total_commands": 15,
          "passed": 15,
          "failed": 0,
          "success_rate": 100.0
        }
      }
    }
  ]
}
```

## 🎨 Output de Ejemplo

```
======================================================================
🚀 DRS Validation Test Suite
======================================================================

Servidor: http://localhost:8080
Modo verbose: True
Tests live: False

======================================================================
🧪 TEST 1: Master Commands (Mock Mode)
======================================================================

ℹ️  Enviando petición de validación Master...
✅ Estado: PASS
✅ Mensaje: Validation completed: 15/15 commands passed

📈 Estadísticas:
   • Total comandos: 15
   • Exitosos: 15
   • Fallidos: 0
   • Timeouts: 0
   • Tasa de éxito: 100.0%
   • Duración promedio: 119.1ms

📋 Comandos ejecutados (15):

   1. ✅ Master Command: optical_port_devices_connected_1
      📝 ✅ Mock validation successful
      📤 Trama enviada: 7E070000F80000B2827E
      📥 Respuesta: 7E0701009700020A00E8357E
      🔍 Valores:
         • optical_port_devices_connected_1: 3
      ⏱️  113ms

======================================================================
📊 RESUMEN FINAL DE TESTS
======================================================================
Total de tests ejecutados: 4
Tests exitosos: 4
Tests fallidos: 0
Tasa de éxito: 100.0%

Detalles por test:
   ✅ PASS - Master Commands Mock
   ✅ PASS - Remote Commands Mock
   ✅ PASS - Batch API Endpoint
   ✅ PASS - WebSocket Logging

⏱️  Duración total: 12.45s

✅ 🎉 TODOS LOS TESTS PASARON
```

## 🔧 Requisitos

- Python 3.8+
- Servidor DRS Validator ejecutándose
- Dependencias: requests, websockets

```bash
pip install requests websockets
```

## 📝 Notas

1. **Modo Mock**: No requiere dispositivo físico, usa respuestas simuladas
2. **Modo Live**: Requiere dispositivo DRS conectado en 192.168.11.22:65050
3. **WebSocket Test**: Verifica logging en tiempo real
4. **Reportes**: Se guardan automáticamente con `--save-report`

## 🐛 Troubleshooting

### Test falla con "Connection refused"
- Verifica que el servidor esté ejecutándose: `docker-compose -f docker-compose.dev.yml up`
- Verifica la URL del servidor con `--url`

### Tests live fallan con timeout
- Verifica que el dispositivo DRS esté conectado y accesible
- Verifica la IP configurada (por defecto 192.168.11.22)
- Aumenta el timeout en el código si es necesario

### No se generan reportes
- Verifica permisos de escritura en el directorio `reports/`
- Usa el flag `--save-report` explícitamente

## 👨‍💻 Desarrollo

Para agregar nuevos tests:

1. Agrega un método `async def test_nuevo_test(self) -> bool` a la clase `DRSTestSuite`
2. Llama al método desde `main()`
3. El resultado se agregará automáticamente al resumen

Ejemplo:
```python
async def test_custom_validation(self) -> bool:
    self.print_header("🧪 TEST: Custom Validation")
    
    # Tu código de test aquí
    success = True  # o False según el resultado
    
    self.test_results.append({
        'test_name': 'Custom Validation',
        'success': success,
        'details': {}
    })
    
    return success
```

## 📚 Referencias

- [DRS Validator Documentation](../docs/README.md)
- [Batch Commands API Guide](../docs/BATCH_COMMANDS_API_GUIDE.md)
- [Hex Frames Reference](../src/hex_frames.py)
