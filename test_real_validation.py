#!/usr/bin/env python3
"""
Test script para verificar la validación en tiempo real con comandos DRS reales
Usa BatchCommandsValidator con hex_frames y respuestas reales capturadas
"""

import asyncio
import websockets
import json
import requests
import sys
from pathlib import Path

# Add project paths
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

async def websocket_listener(client_id, timeout=30):
    """Escucha logs en tiempo real desde el WebSocket"""
    uri = f'ws://localhost:8080/ws/logs/{client_id}'
    print(f'🔌 Conectando al WebSocket: {uri}')
    
    try:
        async with websockets.connect(uri) as websocket:
            print('✅ WebSocket conectado, esperando mensajes...\n')
            
            start_time = asyncio.get_event_loop().time()
            while True:
                try:
                    # Timeout individual por mensaje
                    message = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                    print(message)
                    
                    if '---END_OF_LOG---' in message:
                        print('\n✅ Fin de logs recibido')
                        break
                        
                    # Timeout total
                    if asyncio.get_event_loop().time() - start_time > timeout:
                        print('\n⏱️ Timeout total alcanzado')
                        break
                        
                except asyncio.TimeoutError:
                    # No hay más mensajes
                    print('\n⏱️ No hay más mensajes (timeout)')
                    break
                    
    except Exception as e:
        print(f'❌ Error en WebSocket: {e}')

async def test_validation_mock():
    """Test de validación en modo mock con comandos Master"""
    print("=" * 60)
    print("🧪 TEST 1: Validación MASTER en modo MOCK")
    print("=" * 60)
    
    client_id = 'test-master-mock-001'
    
    # Conectar al WebSocket primero
    ws_task = asyncio.create_task(websocket_listener(client_id))
    await asyncio.sleep(1)
    
    # Datos de prueba
    validation_data = {
        'mode': 'mock',
        'scenario_id': 'master_test',
        'device_config': {
            'ip_address': '192.168.11.22',
            'device_type': 'master'
        },
        'client_id': client_id
    }
    
    print(f'\n📤 Enviando petición de validación...')
    response = requests.post('http://localhost:8080/api/validation/run', json=validation_data)
    print(f'📥 Respuesta HTTP: {response.status_code}')
    
    if response.status_code == 200:
        result = response.json()
        print(f'✅ Client ID: {result.get("client_id")}')
        print(f'📊 Estado: {result.get("status")}')
    else:
        print(f'❌ Error: {response.text}')
    
    # Esperar a que termine el WebSocket
    await ws_task

async def test_validation_remote():
    """Test de validación en modo mock con comandos Remote"""
    print("\n" + "=" * 60)
    print("🧪 TEST 2: Validación REMOTE en modo MOCK")
    print("=" * 60)
    
    client_id = 'test-remote-mock-001'
    
    # Conectar al WebSocket primero
    ws_task = asyncio.create_task(websocket_listener(client_id))
    await asyncio.sleep(1)
    
    # Datos de prueba
    validation_data = {
        'mode': 'mock',
        'scenario_id': 'remote_test',
        'device_config': {
            'ip_address': '192.168.11.22',
            'device_type': 'remote'
        },
        'client_id': client_id
    }
    
    print(f'\n📤 Enviando petición de validación...')
    response = requests.post('http://localhost:8080/api/validation/run', json=validation_data)
    print(f'📥 Respuesta HTTP: {response.status_code}')
    
    if response.status_code == 200:
        result = response.json()
        print(f'✅ Client ID: {result.get("client_id")}')
        print(f'📊 Estado: {result.get("status")}')
    else:
        print(f'❌ Error: {response.text}')
    
    # Esperar a que termine el WebSocket
    await ws_task

async def test_validation_live():
    """Test de validación en modo live (intentará conectar al dispositivo)"""
    print("\n" + "=" * 60)
    print("🧪 TEST 3: Validación REMOTE en modo LIVE")
    print("=" * 60)
    print("⚠️  NOTA: Esto intentará conectar a un dispositivo real")
    print("⚠️  Puede fallar si no hay dispositivo disponible\n")
    
    client_id = 'test-remote-live-001'
    
    # Conectar al WebSocket primero
    ws_task = asyncio.create_task(websocket_listener(client_id, timeout=60))
    await asyncio.sleep(1)
    
    # Datos de prueba
    validation_data = {
        'mode': 'live',
        'scenario_id': 'remote_test',
        'device_config': {
            'ip_address': '192.168.11.22',  # IP del dispositivo real
            'device_type': 'remote'
        },
        'client_id': client_id
    }
    
    print(f'\n📤 Enviando petición de validación...')
    response = requests.post('http://localhost:8080/api/validation/run', json=validation_data)
    print(f'📥 Respuesta HTTP: {response.status_code}')
    
    if response.status_code == 200:
        result = response.json()
        print(f'✅ Client ID: {result.get("client_id")}')
        print(f'📊 Estado: {result.get("status")}')
    else:
        print(f'❌ Error: {response.text}')
    
    # Esperar a que termine el WebSocket
    await ws_task

async def main():
    """Ejecuta todos los tests"""
    print("\n🚀 DRS Real-Time Validation Test Suite")
    print("=" * 60)
    print("Testing con BatchCommandsValidator + hex_frames + respuestas reales\n")
    
    try:
        # Test 1: Master commands en modo mock
        await test_validation_mock()
        
        await asyncio.sleep(2)
        
        # Test 2: Remote commands en modo mock
        await test_validation_remote()
        
        await asyncio.sleep(2)
        
        # Test 3: Remote commands en modo live (opcional)
        user_input = input("\n¿Ejecutar test en modo LIVE? (s/N): ").strip().lower()
        if user_input == 's':
            await test_validation_live()
        else:
            print("⏭️  Test en modo LIVE omitido")
        
        print("\n" + "=" * 60)
        print("✅ Suite de tests completada")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrumpidos por el usuario")
    except Exception as e:
        print(f"\n\n❌ Error durante los tests: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
