#!/usr/bin/env python3
"""
DRS Validation Test Suite - Completo y Reutilizable
====================================================

Suite de pruebas para validación DRS con comandos reales.
Incluye tests para Master, Remote y Set commands usando:
- hex_frames.py (tramas hexadecimales reales)
- batch_commands_validator.py (validador batch)
- real_drs_responses_*.py (respuestas capturadas del dispositivo real)

Uso:
    python tests/test_drs_validation_suite.py                 # Ejecuta todos los tests
    python tests/test_drs_validation_suite.py --test master   # Solo test Master
    python tests/test_drs_validation_suite.py --test remote   # Solo test Remote
    python tests/test_drs_validation_suite.py --test api      # Solo test API
    python tests/test_drs_validation_suite.py --live          # Incluye tests live
    python tests/test_drs_validation_suite.py --verbose       # Output detallado

Autor: DRS Validator Team
Fecha: 2025-10-07
"""

import asyncio
import websockets
import json
import requests
import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import time

# Add project paths
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

# Colores para terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class DRSTestSuite:
    """Suite de pruebas para validación DRS"""
    
    def __init__(self, base_url: str = "http://localhost:8080", verbose: bool = False):
        self.base_url = base_url
        self.verbose = verbose
        self.test_results = []
        self.start_time = None
        self.end_time = None
    
    def print_header(self, text: str):
        """Imprime un encabezado formateado"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.CYAN}{text}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.ENDC}\n")
    
    def print_success(self, text: str):
        """Imprime mensaje de éxito"""
        print(f"{Colors.GREEN}✅ {text}{Colors.ENDC}")
    
    def print_error(self, text: str):
        """Imprime mensaje de error"""
        print(f"{Colors.RED}❌ {text}{Colors.ENDC}")
    
    def print_info(self, text: str):
        """Imprime mensaje informativo"""
        print(f"{Colors.BLUE}ℹ️  {text}{Colors.ENDC}")
    
    def print_warning(self, text: str):
        """Imprime mensaje de advertencia"""
        print(f"{Colors.YELLOW}⚠️  {text}{Colors.ENDC}")
    
    async def test_master_commands_mock(self) -> bool:
        """Test de comandos Master en modo mock"""
        self.print_header("🧪 TEST 1: Master Commands (Mock Mode)")
        
        validation_data = {
            'mode': 'mock',
            'scenario_id': 'master_test',
            'device_config': {
                'ip_address': '192.168.11.22',
                'device_type': 'master'
            },
            'ip_address': '192.168.11.22',
            'port': 65050,
            'timeout': 10
        }
        
        self.print_info("Enviando petición de validación Master...")
        
        try:
            response = requests.post(
                f'{self.base_url}/api/validation/run',
                json=validation_data,
                timeout=30
            )
            
            if response.status_code != 200:
                self.print_error(f"HTTP {response.status_code}: {response.text}")
                return False
            
            result = response.json()
            
            # Verificar resultado
            success = result.get('overall_status') == 'PASS'
            
            if success:
                self.print_success(f"Estado: {result.get('overall_status')}")
                self.print_success(f"Mensaje: {result.get('message')}")
            else:
                self.print_error(f"Estado: {result.get('overall_status')}")
                self.print_error(f"Mensaje: {result.get('message')}")
            
            # Mostrar estadísticas
            if 'statistics' in result:
                stats = result['statistics']
                print(f"\n📈 Estadísticas:")
                print(f"   • Total comandos: {stats.get('total_commands', 0)}")
                print(f"   • Exitosos: {Colors.GREEN}{stats.get('passed', 0)}{Colors.ENDC}")
                print(f"   • Fallidos: {Colors.RED}{stats.get('failed', 0)}{Colors.ENDC}")
                print(f"   • Timeouts: {Colors.YELLOW}{stats.get('timeouts', 0)}{Colors.ENDC}")
                print(f"   • Tasa de éxito: {stats.get('success_rate', 0)}%")
                print(f"   • Duración promedio: {stats.get('average_duration_ms', 0):.1f}ms")
            
            # Mostrar comandos en modo verbose
            if self.verbose and 'tests' in result:
                print(f"\n📋 Comandos ejecutados ({len(result['tests'])}):")
                for i, test in enumerate(result['tests'], 1):
                    status_icon = '✅' if test['status'] == 'PASS' else '❌'
                    print(f"\n   {i}. {status_icon} {test['name']}")
                    print(f"      📝 {test.get('message', 'N/A')}")
                    
                    # Mostrar tramas hex
                    if 'details' in test and test['details']:
                        print(f"      📤 {test['details']}")
                    if 'response_data' in test and test['response_data']:
                        print(f"      📥 Respuesta: {test['response_data']}")
                    
                    # Mostrar valores decodificados
                    if 'decoded_values' in test and test['decoded_values']:
                        decoded = test['decoded_values']
                        relevant = {k: v for k, v in decoded.items() 
                                   if k not in ['status', 'mock_source', 'raw_bytes', 'decoder_mapping', 'mock_enhanced']}
                        if relevant:
                            print(f"      🔍 Valores:")
                            for key, value in list(relevant.items())[:3]:
                                print(f"         • {key}: {value}")
                    
                    print(f"      ⏱️  {test.get('duration_ms', 0)}ms")
            
            self.test_results.append({
                'test_name': 'Master Commands Mock',
                'success': success,
                'details': result
            })
            
            return success
            
        except Exception as e:
            self.print_error(f"Exception: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    async def test_remote_commands_mock(self) -> bool:
        """Test de comandos Remote en modo mock"""
        self.print_header("🧪 TEST 2: Remote Commands (Mock Mode)")
        
        validation_data = {
            'mode': 'mock',
            'scenario_id': 'remote_test',
            'device_config': {
                'ip_address': '192.168.11.22',
                'device_type': 'remote'
            },
            'ip_address': '192.168.11.22',
            'port': 65050,
            'timeout': 10
        }
        
        self.print_info("Enviando petición de validación Remote...")
        
        try:
            response = requests.post(
                f'{self.base_url}/api/validation/run',
                json=validation_data,
                timeout=30
            )
            
            if response.status_code != 200:
                self.print_error(f"HTTP {response.status_code}: {response.text}")
                return False
            
            result = response.json()
            success = result.get('overall_status') == 'PASS'
            
            if success:
                self.print_success(f"Estado: {result.get('overall_status')}")
            else:
                self.print_error(f"Estado: {result.get('overall_status')}")
            
            # Estadísticas resumidas
            if 'statistics' in result:
                stats = result['statistics']
                print(f"\n📈 Resumen: {stats.get('passed', 0)}/{stats.get('total_commands', 0)} exitosos ({stats.get('success_rate', 0)}%)")
            
            self.test_results.append({
                'test_name': 'Remote Commands Mock',
                'success': success,
                'details': result
            })
            
            return success
            
        except Exception as e:
            self.print_error(f"Exception: {str(e)}")
            return False
    
    async def test_batch_api_endpoint(self) -> bool:
        """Test del endpoint directo de batch commands"""
        self.print_header("🧪 TEST 3: Batch Commands API Endpoint")
        
        request_data = {
            'ip_address': '192.168.11.22',
            'command_type': 'master',
            'mode': 'mock',
            'selected_commands': None
        }
        
        self.print_info("Testing endpoint /api/validation/batch-commands...")
        
        try:
            response = requests.post(
                f'{self.base_url}/api/validation/batch-commands',
                json=request_data,
                timeout=30
            )
            
            if response.status_code != 200:
                self.print_error(f"HTTP {response.status_code}")
                return False
            
            result = response.json()
            success = result.get('overall_status') == 'PASS'
            
            if success:
                self.print_success(f"API endpoint funcionando correctamente")
                self.print_info(f"Comandos procesados: {result.get('total_commands', 0)}")
            else:
                self.print_error("API endpoint retornó estado FAIL")
            
            self.test_results.append({
                'test_name': 'Batch API Endpoint',
                'success': success,
                'details': result
            })
            
            return success
            
        except Exception as e:
            self.print_error(f"Exception: {str(e)}")
            return False
    
    async def test_live_validation(self, command_type: str = 'remote') -> bool:
        """Test de validación en modo live (requiere dispositivo real)"""
        self.print_header(f"🧪 TEST LIVE: {command_type.upper()} Commands (Live Mode)")
        self.print_warning("Este test requiere un dispositivo DRS conectado en 192.168.11.22")
        
        validation_data = {
            'mode': 'live',
            'scenario_id': f'{command_type}_test',
            'device_config': {
                'ip_address': '192.168.11.22',
                'device_type': command_type
            },
            'ip_address': '192.168.11.22',
            'port': 65050,
            'timeout': 10
        }
        
        self.print_info(f"Enviando petición de validación {command_type.upper()} en modo LIVE...")
        
        try:
            response = requests.post(
                f'{self.base_url}/api/validation/run',
                json=validation_data,
                timeout=60  # Timeout más largo para conexión real
            )
            
            if response.status_code != 200:
                self.print_error(f"HTTP {response.status_code}: {response.text}")
                return False
            
            result = response.json()
            
            # En modo live, algunos comandos pueden fallar por timeout
            stats = result.get('statistics', {})
            passed = stats.get('passed', 0)
            total = stats.get('total_commands', 0)
            
            # Considerar éxito si al menos 50% de comandos pasan
            success = (passed / total) >= 0.5 if total > 0 else False
            
            if success:
                self.print_success(f"Validación live completada: {passed}/{total} exitosos")
            else:
                self.print_warning(f"Validación live con problemas: {passed}/{total} exitosos")
            
            # Mostrar timeouts
            timeouts = stats.get('timeouts', 0)
            if timeouts > 0:
                self.print_warning(f"Timeouts detectados: {timeouts}")
            
            self.test_results.append({
                'test_name': f'{command_type.upper()} Commands Live',
                'success': success,
                'details': result
            })
            
            return success
            
        except Exception as e:
            self.print_error(f"Exception: {str(e)}")
            self.print_warning("Dispositivo DRS no disponible o no accesible")
            return False
    
    async def test_websocket_logging(self) -> bool:
        """Test de logging en tiempo real vía WebSocket"""
        self.print_header("🧪 TEST 4: WebSocket Real-Time Logging")
        
        client_id = f'test-ws-{int(time.time())}'
        
        self.print_info(f"Client ID: {client_id}")
        
        try:
            # Conectar al WebSocket
            ws_url = f"ws://localhost:8080/ws/logs/{client_id}"
            self.print_info(f"Conectando a {ws_url}...")
            
            async with websockets.connect(ws_url) as websocket:
                self.print_success("WebSocket conectado")
                
                # Enviar validación en paralelo
                validation_data = {
                    'mode': 'mock',
                    'scenario_id': 'master_test',
                    'device_config': {
                        'ip_address': '192.168.11.22',
                        'device_type': 'master'
                    },
                    'client_id': client_id,
                    'ip_address': '192.168.11.22',
                    'port': 65050,
                    'timeout': 10
                }
                
                # Iniciar validación
                response = requests.post(
                    f'{self.base_url}/api/validation/run',
                    json=validation_data
                )
                
                # Recibir logs
                log_count = 0
                while True:
                    try:
                        message = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                        log_count += 1
                        
                        if self.verbose:
                            print(f"   📨 {message}")
                        
                        if '---END_OF_LOG---' in message:
                            break
                            
                    except asyncio.TimeoutError:
                        break
                
                success = log_count > 0
                
                if success:
                    self.print_success(f"Recibidos {log_count} mensajes de log")
                else:
                    self.print_error("No se recibieron mensajes de log")
                
                self.test_results.append({
                    'test_name': 'WebSocket Logging',
                    'success': success,
                    'details': {'log_count': log_count}
                })
                
                return success
                
        except Exception as e:
            self.print_error(f"Exception: {str(e)}")
            return False
    
    def print_summary(self):
        """Imprime resumen final de todos los tests"""
        self.print_header("📊 RESUMEN FINAL DE TESTS")
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if r['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"Total de tests ejecutados: {total_tests}")
        print(f"{Colors.GREEN}Tests exitosos: {passed_tests}{Colors.ENDC}")
        print(f"{Colors.RED}Tests fallidos: {failed_tests}{Colors.ENDC}")
        
        if total_tests > 0:
            success_rate = (passed_tests / total_tests) * 100
            print(f"Tasa de éxito: {success_rate:.1f}%")
        
        print(f"\n{Colors.BOLD}Detalles por test:{Colors.ENDC}")
        for result in self.test_results:
            status = f"{Colors.GREEN}✅ PASS{Colors.ENDC}" if result['success'] else f"{Colors.RED}❌ FAIL{Colors.ENDC}"
            print(f"   {status} - {result['test_name']}")
        
        # Duración total
        if self.start_time and self.end_time:
            duration = self.end_time - self.start_time
            print(f"\n⏱️  Duración total: {duration:.2f}s")
        
        # Resultado final
        print()
        if passed_tests == total_tests:
            self.print_success("🎉 TODOS LOS TESTS PASARON")
            return 0
        else:
            self.print_error("⚠️  ALGUNOS TESTS FALLARON")
            return 1
    
    def save_report(self, filename: Optional[str] = None):
        """Guarda reporte de tests en archivo JSON"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"test_report_{timestamp}.json"
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_tests': len(self.test_results),
            'passed': sum(1 for r in self.test_results if r['success']),
            'failed': sum(1 for r in self.test_results if not r['success']),
            'duration_seconds': self.end_time - self.start_time if self.start_time and self.end_time else 0,
            'tests': self.test_results
        }
        
        output_path = project_root / 'reports' / filename
        output_path.parent.mkdir(exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        self.print_success(f"Reporte guardado en: {output_path}")

async def main():
    """Función principal"""
    parser = argparse.ArgumentParser(
        description='DRS Validation Test Suite',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python tests/test_drs_validation_suite.py                    # Ejecutar todos los tests
  python tests/test_drs_validation_suite.py --test master      # Solo test Master
  python tests/test_drs_validation_suite.py --test remote      # Solo test Remote
  python tests/test_drs_validation_suite.py --live             # Incluir tests live
  python tests/test_drs_validation_suite.py --verbose          # Output detallado
  python tests/test_drs_validation_suite.py --save-report      # Guardar reporte JSON
        """
    )
    
    parser.add_argument(
        '--test',
        choices=['master', 'remote', 'api', 'websocket', 'all'],
        default='all',
        help='Tipo de test a ejecutar'
    )
    
    parser.add_argument(
        '--live',
        action='store_true',
        help='Incluir tests en modo live (requiere dispositivo conectado)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Mostrar output detallado'
    )
    
    parser.add_argument(
        '--save-report',
        action='store_true',
        help='Guardar reporte en archivo JSON'
    )
    
    parser.add_argument(
        '--url',
        default='http://localhost:8080',
        help='URL base del servidor DRS Validator'
    )
    
    args = parser.parse_args()
    
    # Crear suite de tests
    suite = DRSTestSuite(base_url=args.url, verbose=args.verbose)
    
    print(f"\n{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.HEADER}🚀 DRS Validation Test Suite{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.ENDC}")
    print(f"\n{Colors.BLUE}Servidor: {args.url}{Colors.ENDC}")
    print(f"{Colors.BLUE}Modo verbose: {args.verbose}{Colors.ENDC}")
    print(f"{Colors.BLUE}Tests live: {args.live}{Colors.ENDC}\n")
    
    suite.start_time = time.time()
    
    try:
        # Ejecutar tests según selección
        if args.test in ['master', 'all']:
            await suite.test_master_commands_mock()
        
        if args.test in ['remote', 'all']:
            await suite.test_remote_commands_mock()
        
        if args.test in ['api', 'all']:
            await suite.test_batch_api_endpoint()
        
        if args.test in ['websocket', 'all']:
            await suite.test_websocket_logging()
        
        # Tests live (opcionales)
        if args.live:
            await suite.test_live_validation('remote')
            await suite.test_live_validation('master')
        
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚠️  Tests interrumpidos por el usuario{Colors.ENDC}")
    except Exception as e:
        print(f"\n{Colors.RED}❌ Error crítico: {str(e)}{Colors.ENDC}")
        import traceback
        traceback.print_exc()
    finally:
        suite.end_time = time.time()
        
        # Mostrar resumen
        exit_code = suite.print_summary()
        
        # Guardar reporte si se solicitó
        if args.save_report:
            suite.save_report()
        
        return exit_code

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
