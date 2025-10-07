#!/usr/bin/env python3
"""
DRS Validation Tool - FastAPI Web Application
Provides web interface for technicians to validate device communications
"""

import os
import sys
import json
import yaml
import logging
import asyncio
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

from fastapi import FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

# Determine project root for correct path resolution
project_root = Path(__file__).parent  # This will be the 'src' directory
sys.path.insert(0, str(project_root))

# Import our validation logic
try:
    from validation.tcp_validator import TechnicianTCPValidator, validate_device
    VALIDATION_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import validation logic: {e}")
    try:
        # Fallback to standalone validator
        from validation.standalone_validator import validate_device_standalone as validate_device
        VALIDATION_AVAILABLE = True
        print("Using standalone validator as fallback")
    except ImportError as e2:
        print(f"Warning: Could not import standalone validator: {e2}")
        VALIDATION_AVAILABLE = False

# Import batch commands validator
try:
    from validation.batch_commands_validator import BatchCommandsValidator, CommandType
    BATCH_VALIDATION_AVAILABLE = True
    print("✅ Batch commands validator loaded successfully")
except ImportError as e:
    print(f"Warning: Could not import batch commands validator: {e}")
    BATCH_VALIDATION_AVAILABLE = False

# Alternative simple validation function if imports fail
def simple_validation(device_ip: str, device_type: str, hostname: str = None, live_mode: bool = False):
    """Simple validation function as fallback"""
    import subprocess
    import time
    
    results = {
        "status": "success" if not live_mode else "unknown",
        "device_ip": device_ip,
        "device_type": device_type,
        "hostname": hostname,
        "mode": "live" if live_mode else "mock",
        "timestamp": datetime.now().isoformat(),
        "tests": []
    }
    
    # Simple ping test
    try:
        if live_mode:
            ping_result = subprocess.run(['ping', '-n', '1', device_ip], 
                                       capture_output=True, text=True, timeout=5)
            ping_success = ping_result.returncode == 0
        else:
            ping_success = True  # Mock mode always succeeds
            
        results["tests"].append({
            "name": "ping_test",
            "status": "pass" if ping_success else "fail",
            "message": f"Ping to {device_ip} {'successful' if ping_success else 'failed'}"
        })
    except Exception as e:
        results["tests"].append({
            "name": "ping_test", 
            "status": "fail",
            "message": f"Ping test error: {str(e)}"
        })
    
    return results

async def generate_simulated_validation_results(request: Dict[str, Any]):
    """
    Generate realistic simulated validation results using BatchCommandsValidator.
    Uses real DRS command frames and mock responses from captured data.
    """
    import asyncio
    
    scenario_id = request.get("scenario_id", "remote_test")
    device_config = request.get("device_config", {})
    ip_address = device_config.get("ip_address", "192.168.11.22")
    device_type = device_config.get("device_type", "remote")
    
    # Simular procesamiento breve
    await asyncio.sleep(0.5)
    
    # Determinar tipo de comando basado en el escenario
    if scenario_id == "master_test" or device_type.lower() == "master":
        command_type = CommandType.MASTER
    elif scenario_id == "set_test" or device_type.lower() == "set":
        command_type = CommandType.SET
    else:
        command_type = CommandType.REMOTE
    
    # Ejecutar validación batch en modo mock
    validator = BatchCommandsValidator()
    result = await asyncio.to_thread(
        validator.validate_batch_commands,
        ip_address=ip_address,
        command_type=command_type,
        mode="mock",
        selected_commands=None
    )
    
    # Convertir resultados a formato compatible con la UI
    tests = []
    for cmd_result in result.get("results", []):
        # Determinar si es comando SET
        is_set_command = cmd_result['command'].startswith('set_') or cmd_result['command'].startswith('remote_set_')
        
        tests.append({
            "name": f"{command_type.value.title()} Command: {cmd_result['command']}",
            "status": cmd_result["status"],
            "message": cmd_result["message"],
            "duration_ms": cmd_result["duration_ms"],
            "details": cmd_result.get("details", ""),
            "response_data": cmd_result.get("response_data", ""),
            "decoded_values": cmd_result.get("decoded_values", {}),
            "is_set_command": is_set_command
        })
    
    return JSONResponse({
        "status": "completed",
        "overall_status": result["overall_status"],
        "message": f"Validation completed: {result['statistics']['passed']}/{result['statistics']['total_commands']} commands passed",
        "device_ip": ip_address,
        "scenario": scenario_id,
        "mode": "mock",
        "timestamp": result["timestamp"],
        "tests": tests,
        "simulation": True,
        "total_duration_ms": result["duration_ms"],
        "statistics": result["statistics"],
        "command_type": command_type.value
    })

# FastAPI app instance
app = FastAPI(
    title="DRS Device Validation Tool",
    description="Web interface for technicians to validate device communications",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Static files and templates
# Correctly locate web assets from the project root
app.mount("/static", StaticFiles(directory=Path(__file__).parent / "web/static"), name="static")
templates = Jinja2Templates(directory=Path(__file__).parent / "web/templates")

# Results storage directory - use absolute path for container
PROJECT_ROOT = Path("/app")  # Fixed path for container environment
RESULTS_DIR = PROJECT_ROOT / "results"
RESULTS_DIR.mkdir(exist_ok=True)


# Pydantic models for API
class DeviceConfig(BaseModel):
    ip_address: str
    device_type: str
    device_name: str
    serial_number: Optional[str] = None  # Número de serie del dispositivo
    optical_port: Optional[int] = 1
    command: Optional[int] = None


class ValidationThresholds(BaseModel):
    warning_downlink: Optional[int] = 38
    warning_temperature: Optional[int] = 45
    warning_uplink: Optional[int] = 38
    critical_downlink: Optional[int] = 41
    critical_temperature: Optional[int] = 50
    critical_uplink: Optional[int] = 31


class ValidationRequest(BaseModel):
    mode: str  # 'mock' or 'live'
    device_config: DeviceConfig
    thresholds: ValidationThresholds


class ValidationResult(BaseModel):
    status: str  # 'PASS', 'FAIL', 'WARNING'
    message: str
    details: Optional[Dict] = None
    action: Optional[str] = None
    timestamp: datetime


# New Pydantic models for Batch Commands API
class BatchCommandsRequest(BaseModel):
    """Request model for batch commands validation"""
    ip_address: str
    command_type: str  # 'master' or 'remote'
    mode: str = "mock"  # 'mock' or 'live'
    selected_commands: Optional[List[str]] = None
    timeout_seconds: Optional[int] = 3


class BatchCommandResult(BaseModel):
    """Individual command result model"""
    command: str
    command_type: str
    status: str  # 'PASS', 'FAIL', 'TIMEOUT', 'ERROR'
    message: str
    details: Optional[str] = None
    response_data: Optional[str] = None
    decoded_values: Optional[Dict[str, Any]] = None
    duration_ms: int
    error: Optional[str] = None


class BatchCommandsResponse(BaseModel):
    """Response model for batch commands validation"""
    overall_status: str
    command_type: str
    mode: str
    ip_address: str
    total_commands: int
    commands_tested: List[str]
    statistics: Dict[str, Any]
    results: List[Dict[str, Any]]  # List of command results
    duration_ms: int
    timestamp: str


class SupportedCommandsResponse(BaseModel):
    """Response model for supported commands list"""
    master_commands: List[str]
    remote_commands: List[str]
    set_commands: List[str] = []
    total_commands: Optional[int] = None
    decoder_mappings: Optional[Dict[str, bool]] = None


def save_validation_result(result: Dict[str, Any], request: ValidationRequest) -> str:
    """Save validation result to persistent storage"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        device_type = request.device_config.device_type
        ip_address = request.device_config.ip_address.replace(".", "_")
        
        filename = f"{timestamp}_{device_type}_{ip_address}.json"
        filepath = RESULTS_DIR / filename
        
        # Add metadata to result
        result_data = {
            "timestamp": datetime.now().isoformat(),
            "request": {
                "ip_address": request.device_config.ip_address,
                "device_type": request.device_config.device_type,
                "hostname": request.device_config.device_name,
                "serial_number": request.device_config.serial_number,
                "live_mode": request.mode == "live"
            },
            "result": result
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, indent=2, ensure_ascii=False)
        
        logging.info(f"💾 Resultado guardado: {filepath}")
        return str(filepath)
        
    except Exception as e:
        logging.error(f"❌ Error guardando resultado: {e}")
        return ""


# API Endpoints


# Global validation service
class ValidationService:
    """Service that wraps existing test logic for technician use"""
    
    def __init__(self):
        # The direct instantiation of test classes is removed as it's an anti-pattern.
        # This class can be repurposed or removed if not needed.
        pass
    
    async def validate_device(self, request: ValidationRequest) -> ValidationResult:
        """
        Main validation method that uses existing test patterns
        """
        try:
            if request.mode == 'mock':
                result = await self._validate_mock_mode(request)
            elif request.mode == 'live':
                result = await self._validate_live_mode(request)
            else:
                raise ValueError(f"Invalid mode: {request.mode}")
            
            # Save result to persistent storage
            saved_path = save_validation_result(result.dict(), request)
            if saved_path:
                logging.info(f"✅ Validation result saved to {saved_path}")
            
            return result
                
        except Exception as e:
            error_result = ValidationResult(
                status="FAIL",
                message=f"Validation error: {str(e)}",
                action="Check configuration and try again",
                timestamp=datetime.now()
            )
            
            # Save error result too
            save_validation_result(error_result.dict(), request)
            
            return error_result
    
    async def _validate_mock_mode(self, request: ValidationRequest) -> ValidationResult:
        """
        Mock validation using existing TCP transceiver test patterns
        """
        # TODO: Implement using test_tcp_transceiver.py patterns
        return ValidationResult(
            status="PASS",
            message=f"Mock validation successful for {request.device_config.device_type}",
            details={
                "mode": "mock",
                "device": request.device_config.device_type,
                "ip": request.device_config.ip_address
            },
            timestamp=datetime.now()
        )
    
    async def _validate_live_mode(self, request: ValidationRequest) -> ValidationResult:
        """
        Live validation using existing integration test patterns
        """
        # TODO: Implement using test_check_eth_integration.py patterns
        return ValidationResult(
            status="WARNING",
            message=f"Live validation not yet implemented for {request.device_config.device_type}",
            action="Use mock mode for now",
            timestamp=datetime.now()
        )


# Initialize validation service
validation_service = ValidationService()

# WebSocket Connection Manager for Real-time Logging
class ConnectionManager:
    """Manages active WebSocket connections for real-time logging"""
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        logging.info(f"📡 WebSocket client connected: {client_id}")

    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]
            logging.info(f"📡 WebSocket client disconnected: {client_id}")

    async def send_log(self, client_id: str, message: str):
        if client_id in self.active_connections:
            try:
                await self.active_connections[client_id].send_text(message)
            except Exception as e:
                logging.warning(f"Could not send log to client {client_id}: {e}")

# Global connection manager and task storage
manager = ConnectionManager()
active_tasks = {}

async def run_validation_with_logging(client_id: str, request_data: Dict[str, Any]):
    """Execute validation with detailed real-time logging"""
    print(f"DEBUG: run_validation_with_logging called with client_id: {client_id}")
    
    # Esperar a que el WebSocket se conecte (opcional para logging en tiempo real)
    max_wait = 2  # segundos máximo de espera
    waited = 0
    websocket_available = False
    
    while client_id not in manager.active_connections and waited < max_wait:
        print(f"DEBUG: Waiting for WebSocket connection... ({waited}s)")
        await asyncio.sleep(1)
        waited += 1
    
    if client_id in manager.active_connections:
        websocket_available = True
        print(f"DEBUG: WebSocket connected for client {client_id}")
    else:
        print(f"DEBUG: No WebSocket connection for client {client_id}, proceeding without real-time logging")
    
    try:
        if websocket_available:
            await manager.send_log(client_id, "[DEBUG] 🚀 Starting validation function")
        
        device_config = request_data  # Use request_data directly as device_config
        ip_address = device_config.get("ip_address", "N/A")
        command_type_str = device_config.get("command_type", "remote")  # Use command_type as device_type
        mode = request_data.get("mode", "mock")
        
        log_message = f"[INFO] 🚀 Iniciando validación {command_type_str} en {ip_address} (modo: {mode})"
        if websocket_available:
            await manager.send_log(client_id, log_message)
        print(log_message)
        
        # Crear callback de logging que funcione con o sin WebSocket
        async def log_callback(message: str):
            if websocket_available:
                await manager.send_log(client_id, message)
            else:
                print(message)  # Fallback to console logging
        
        # Crear instancia del validador con callback de logging
        validator = BatchCommandsValidator(log_callback=log_callback)
        
        # Determinar el tipo de comando basado en el command_type_str
        if command_type_str == "master":
            command_type = CommandType.MASTER
        elif command_type_str == "set":
            command_type = CommandType.SET
        else:
            command_type = CommandType.REMOTE  # default
        
        # Ejecutar validación de forma asíncrona con logs en tiempo real
        result = await validator.validate_batch_commands_async(
            ip_address=ip_address,
            command_type=command_type,
            mode=mode,
            selected_commands=None  # None means all commands
        )
        
        # Save the validation result to persistent storage
        try:
            # Create ValidationRequest object from request_data
            device_config_obj = DeviceConfig(
                ip_address=request_data.get("ip_address", "N/A"),
                device_type=request_data.get("command_type", "remote"),  # Use command_type as device_type
                device_name=request_data.get("scenario_id", "Unknown"),
                serial_number=request_data.get("serial_number", "N/A"),
                optical_port=request_data.get("port", 1)
            )
            thresholds_obj = ValidationThresholds(
                ping_timeout_ms=5000,
                tcp_timeout_ms=10000,
                max_retries=3
            )
            validation_request = ValidationRequest(
                mode=mode,
                device_config=device_config_obj,
                thresholds=thresholds_obj
            )
            
            saved_path = save_validation_result(result, validation_request)
            if saved_path:
                await log_callback(f"[INFO] 💾 Resultado guardado: {saved_path}")
                logging.info(f"✅ Validation result saved to {saved_path}")
            else:
                await log_callback("[WARNING] ⚠️ No se pudo guardar el resultado")
                logging.warning("Failed to save validation result")
        except Exception as save_error:
            await log_callback(f"[ERROR] ❌ Error guardando resultado: {str(save_error)}")
            logging.error(f"Error saving validation result: {save_error}")
        
        # Actualizar estado de la tarea
        overall_status = result.get("overall_status", "FAIL")
        stats = result.get("statistics", {})
        
        if overall_status == "PASS":
            success_msg = f"[SUCCESS] ✅ Validación completada: {stats.get('passed', 0)}/{stats.get('total_commands', 0)} comandos exitosos"
            await log_callback(success_msg)
            active_tasks[client_id] = {
                "status": "PASS",
                "message": "Validación completada exitosamente",
                "details": result
            }
        else:
            error_msg = f"[ERROR] ❌ Validación fallida: {stats.get('failed', 0)} comandos fallidos"
            await log_callback(error_msg)
            active_tasks[client_id] = {
                "status": "FAIL",
                "message": f"Validación fallida: {stats.get('failed', 0)} errores",
                "details": result
            }
        
        # Send validation_complete message via WebSocket if available
        if websocket_available:
            completion_message = json.dumps({
                "type": "validation_complete",
                "result": result,
                "client_id": client_id
            })
            await manager.send_log(client_id, completion_message)
        
    except Exception as e:
        error_msg = f"[ERROR] ❌ Error durante validación: {str(e)}"
        await log_callback(error_msg)
        active_tasks[client_id] = {"status": "ERROR", "message": str(e)}
    finally:
        if websocket_available:
            await manager.send_log(client_id, "---END_OF_LOG---")


# API Routes
@app.get("/health")
async def health_check():
    """Health check endpoint for Docker"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Main technician interface"""
    return templates.TemplateResponse("index-modern.html", {"request": request})


@app.get("/api/test")
async def test_endpoint():
    """Test endpoint to verify API functionality"""
    return {
        "status": "success",
        "message": "API is working",
        "simulation_mode": "configurable",  # Now configurable via UI
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/validation/scenarios")
async def get_validation_scenarios():
    """Get available validation scenarios for technicians"""
    return {
        "scenarios": [
            {
                "id": "remote_test",
                "name": "Remote Test",
                "description": "Executes batch validation of all remote DRS commands",
                "enabled": True,
                "device_type": "drs_remote",
                "default_ip": "192.168.11.22",
                "default_hostname": "drs-device"
            },
            {
                "id": "master_test",
                "name": "Master Test",
                "description": "Executes batch validation of all master DRS commands",
                "enabled": True,
                "device_type": "drs_master",
                "default_ip": "192.168.11.22",
                "default_hostname": "drs-master"
            }
        ]
    }


@app.post("/api/validation/run")
async def run_validation(request: Dict[str, Any], background_tasks: BackgroundTasks):
    """Execute device validation with current configuration and real-time logging"""
    try:
        # Check if request specifies simulation mode
        request_mode = request.get("mode", "mock")
        simulation_mode = request_mode.lower() == "mock"
        
        # Check if request wants WebSocket logging (new functionality)
        use_websockets = request.get("use_websockets", True)  # Default to new behavior
        
        if use_websockets:
            # WebSocket-based approach - works for both mock and live mode
            client_id = request.get("client_id", str(uuid.uuid4()))
            print(f"DEBUG: Starting WebSocket validation for client_id: {client_id}")
            active_tasks[client_id] = {"status": "STARTING", "message": "Iniciando validación..."}
            
            # Ejecutar la validación en background para no bloquear la respuesta HTTP
            background_tasks.add_task(run_validation_with_logging, client_id, request)
            
            return JSONResponse({
                "status": "started",
                "client_id": client_id,
                "message": "Validación iniciada. Conéctate al WebSocket para logs en tiempo real.",
                "websocket_url": f"/ws/logs/{client_id}"
            })
        
        if simulation_mode:
            # Fallback: Return simulated validation results immediately
            return await generate_simulated_validation_results(request)
        
        # Legacy approach (original logic) - keep for compatibility
        # Validate required fields
        required_fields = ["scenario_id", "ip_address", "hostname", "mode"]
        for field in required_fields:
            if field not in request:
                raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
        
        # Get scenario details to determine device_type
        scenario_id = request["scenario_id"]
        device_type_mapping = {
            "remote_test": "drs_remote",
            "master_test": "drs_master"
        }
        
        # Build validation config
        validation_config = {
            "device_type": device_type_mapping.get(scenario_id, "dmu_ethernet"),
            "ip_address": request["ip_address"],
            "hostname": request["hostname"],
            "mode": request["mode"]
        }
        
        # Add thresholds if provided
        if "thresholds" in request:
            validation_config.update(request["thresholds"])
        
        # Execute validation
        if scenario_id == "remote_test":
            # Special handling for remote test scenario
            if BATCH_VALIDATION_AVAILABLE:
                try:
                    validator = BatchCommandsValidator()
                    batch_result = validator.validate_batch_commands(
                        ip_address=validation_config["ip_address"],
                        command_type=CommandType.REMOTE,
                        mode=validation_config["mode"],
                        selected_commands=None  # None means all remote commands
                    )
                    
                    # Convert batch result to standard validation format
                    # Ensure status values are strings
                    results_list = batch_result["results"]
                    for cmd in results_list:
                        if hasattr(cmd["status"], 'value'):
                            cmd["status"] = cmd["status"].value
                    
                    result = {
                        "overall_status": batch_result["overall_status"],  # Use batch validator's overall status (80% threshold)
                        "message": f"Remote test validation completed. {len([c for c in results_list if c['status'] == 'PASS'])}/{len(results_list)} commands passed.",
                        "mode": validation_config["mode"],
                        "tests": [
                            {
                                "name": f"Remote Command: {cmd['command']}",
                                "status": cmd["status"],
                                "message": cmd.get("message", "Command executed"),
                                "details": f"Response: {cmd.get('response_data', 'N/A')}",
                                "duration_ms": cmd.get("duration_ms", 0)
                            }
                            for cmd in results_list
                        ],
                        "duration_ms": batch_result.get("duration_ms", 0),
                        "timestamp": datetime.now().isoformat(),
                        "command_type": "remote",
                        "total_commands": len(results_list)
                    }
                except Exception as e:
                    result = {
                        "overall_status": "FAIL",
                        "message": f"Remote test validation failed: {str(e)}",
                        "mode": validation_config["mode"],
                        "tests": [
                            {
                                "name": "Remote Test",
                                "status": "FAIL",
                                "message": f"Validation error: {str(e)}",
                                "details": "Failed to execute remote commands batch"
                            }
                        ],
                        "duration_ms": 0,
                        "timestamp": datetime.now().isoformat()
                    }
            else:
                result = {
                    "overall_status": "FAIL",
                    "message": "Batch commands validator not available",
                    "mode": validation_config["mode"],
                    "tests": [
                        {
                            "name": "Remote Test",
                            "status": "FAIL",
                            "message": "Batch commands validator not available",
                            "details": "Required dependencies not installed"
                        }
                    ],
                    "duration_ms": 0,
                    "timestamp": datetime.now().isoformat()
                }
        elif scenario_id == "master_test":
            # Special handling for master test scenario
            if BATCH_VALIDATION_AVAILABLE:
                try:
                    validator = BatchCommandsValidator()
                    batch_result = validator.validate_batch_commands(
                        ip_address=validation_config["ip_address"],
                        command_type=CommandType.MASTER,
                        mode=validation_config["mode"],
                        selected_commands=None  # None means all master commands
                    )
                    
                    # Convert batch result to standard validation format
                    # Ensure status values are strings
                    results_list = batch_result["results"]
                    for cmd in results_list:
                        if hasattr(cmd["status"], 'value'):
                            cmd["status"] = cmd["status"].value
                    
                    result = {
                        "overall_status": batch_result["overall_status"],  # Use batch validator's overall status (80% threshold)
                        "message": f"Master test validation completed. {len([c for c in results_list if c['status'] == 'PASS'])}/{len(results_list)} commands passed.",
                        "mode": validation_config["mode"],
                        "tests": [
                            {
                                "name": f"Master Command: {cmd['command']}",
                                "status": cmd["status"],
                                "message": cmd.get("message", "Command executed"),
                                "details": f"Response: {cmd.get('response_data', 'N/A')}",
                                "duration_ms": cmd.get("duration_ms", 0)
                            }
                            for cmd in results_list
                        ],
                        "duration_ms": batch_result.get("duration_ms", 0),
                        "timestamp": datetime.now().isoformat(),
                        "command_type": "master",
                        "total_commands": len(results_list)
                    }
                except Exception as e:
                    result = {
                        "overall_status": "FAIL",
                        "message": f"Master test validation failed: {str(e)}",
                        "mode": validation_config["mode"],
                        "tests": [
                            {
                                "name": "Master Test",
                                "status": "FAIL",
                                "message": f"Validation error: {str(e)}",
                                "details": "Failed to execute master commands batch"
                            }
                        ],
                        "duration_ms": 0,
                        "timestamp": datetime.now().isoformat()
                    }
            else:
                result = {
                    "overall_status": "FAIL",
                    "message": "Batch commands validator not available",
                    "mode": validation_config["mode"],
                    "tests": [
                        {
                            "name": "Master Test",
                            "status": "FAIL",
                            "message": "Batch commands validator not available",
                            "details": "Required dependencies not installed"
                        }
                    ],
                    "duration_ms": 0,
                    "timestamp": datetime.now().isoformat()
                }
        elif VALIDATION_AVAILABLE:
            result = validate_device(validation_config)
        else:
            # Fallback mock result if validation not available
            result = {
                "overall_status": "WARNING",
                "message": "Validation logic not available - returning mock result",
                "mode": validation_config["mode"],
                "tests": [
                    {
                        "name": "Mock Test",
                        "status": "WARNING",
                        "message": "Validation system not fully initialized",
                        "details": "Import dependencies missing"
                    }
                ],
                "duration_ms": 100,
                "timestamp": datetime.now().isoformat()
            }
        
        # Add request context to result
        result["scenario_id"] = scenario_id
        result["mode"] = validation_config["mode"]
        
        return {
            "status": "success",
            "result": result,
            "scenario_id": scenario_id,
            "mode": validation_config["mode"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        # Fallback: Return a client_id for WebSocket compatibility
        client_id = str(uuid.uuid4())
        active_tasks[client_id] = {"status": "ERROR", "message": f"Error: {str(e)}"}
        return JSONResponse({
            "status": "error",
            "client_id": client_id,
            "message": f"Error al iniciar validación: {str(e)}"
        })


# Remove duplicate endpoint - use the modified one above


@app.post("/api/validation/ping/{ip_address}")
async def ping_device_endpoint(ip_address: str, mode: str = "mock"):
    """Test basic network connectivity to device"""
    try:
        # Check if request specifies simulation mode
        simulation_mode = mode.lower() == "mock"
        
        if simulation_mode:
            # Simulate different responses based on IP for testing
            import random
            
            # Simulate different scenarios based on IP
            if ip_address.endswith('.22'):
                # Simulate successful Modbus device
                return {
                    "status": "PASS",
                    "ip_address": ip_address,
                    "message": f"✅ Device at {ip_address} is reachable (Simulated Modbus device)",
                    "timestamp": datetime.now().isoformat(),
                    "simulation": True,
                    "device_type": "Modbus RTU/TCP Gateway"
                }
            elif ip_address.endswith('.1') or ip_address == '127.0.0.1':
                # Simulate network gateway or localhost
                return {
                    "status": "PASS",
                    "ip_address": ip_address,
                    "message": f"✅ Device at {ip_address} is reachable (Simulated gateway)",
                    "timestamp": datetime.now().isoformat(),
                    "simulation": True,
                    "device_type": "Network Gateway"
                }
            elif random.choice([True, False]):
                # Random success for variety
                return {
                    "status": "PASS",
                    "ip_address": ip_address,
                    "message": f"✅ Device at {ip_address} is reachable (Simulated device)",
                    "timestamp": datetime.now().isoformat(),
                    "simulation": True,
                    "device_type": "Industrial Device"
                }
            else:
                # Simulate timeout/failure
                return {
                    "status": "FAIL",
                    "ip_address": ip_address,
                    "message": f"❌ Device at {ip_address} timeout (Simulated offline device)",
                    "timestamp": datetime.now().isoformat(),
                    "simulation": True
                }

        # Original logic for non-simulation mode
        # Check if running in Docker container
        is_docker = os.path.exists('/.dockerenv') or os.environ.get('DOCKER_CONTAINER', False)

        if VALIDATION_AVAILABLE and not is_docker:
            validator = TechnicianTCPValidator()
            result = validator.ping_device(ip_address)
            return result
        else:
            # Docker-friendly connectivity test using TCP connection
            import socket
            import asyncio

            try:
                # Try to connect to common device ports (502 for Modbus, 80 for HTTP, etc.)
                common_ports = [502, 80, 443, 23, 22]  # Modbus, HTTP, HTTPS, Telnet, SSH
                connected = False

                for port in common_ports:
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(5)
                        result = sock.connect_ex((ip_address, port))
                        sock.close()

                        if result == 0:
                            connected = True
                            break
                    except:
                        continue

                if connected:
                    return {
                        "status": "PASS",
                        "ip_address": ip_address,
                        "message": f"✅ Device at {ip_address} is reachable (TCP connection)",
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    # Fallback to ping if TCP fails
                    import subprocess
                    import platform

                    ping_cmd = ["ping", "-n", "1"] if platform.system() == "Windows" else ["ping", "-c", "1"]
                    ping_cmd.append(ip_address)

                    try:
                        result = subprocess.run(ping_cmd, capture_output=True, text=True, timeout=10)
                        if result.returncode == 0:
                            return {
                                "status": "PASS",
                                "ip_address": ip_address,
                                "message": f"✅ Device at {ip_address} is reachable (ping)",
                                "timestamp": datetime.now().isoformat()
                            }
                        else:
                            return {
                                "status": "FAIL",
                                "ip_address": ip_address,
                                "message": f"❌ Device at {ip_address} is not reachable",
                                "timestamp": datetime.now().isoformat()
                            }
                    except subprocess.TimeoutExpired:
                        return {
                            "status": "FAIL",
                            "ip_address": ip_address,
                            "message": f"❌ Ping timeout for {ip_address}",
                            "timestamp": datetime.now().isoformat()
                        }

            except Exception as e:
                return {
                    "status": "FAIL",
                    "ip_address": ip_address,
                    "message": f"❌ Connection test failed: {str(e)}",
                    "timestamp": datetime.now().isoformat()
                }
    except Exception as e:
        return {
            "status": "ERROR",
            "ip_address": ip_address,
            "message": f"❌ Ping test error: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }


# New endpoints for real-time logging
@app.get("/api/validation/task/{client_id}")
async def get_task_result(client_id: str):
    """Get the result of a validation task"""
    if client_id not in active_tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return JSONResponse(active_tasks[client_id])


@app.websocket("/ws/logs/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """WebSocket endpoint for real-time validation logs"""
    await manager.connect(websocket, client_id)
    try:
        while True:
            # Keep connection alive to send logs
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(client_id)


@app.get("/api/validation/report/{run_id}")
async def get_validation_report(run_id: str):
    """Get detailed validation report"""
    # TODO: Implement report storage and retrieval
    return {
        "run_id": run_id,
        "status": "not_implemented",
        "message": "Report storage system not yet implemented",
        "timestamp": datetime.now().isoformat()
    }


# New Batch Commands Endpoints
@app.post("/api/validation/batch-commands")
async def run_batch_commands(request: BatchCommandsRequest) -> BatchCommandsResponse:
    """
    Execute batch validation of DRS commands using Santone protocol.
    
    Supports both mock and live testing modes with comprehensive
    command validation and SantoneDecoder integration.
    """
    if not BATCH_VALIDATION_AVAILABLE:
        raise HTTPException(
            status_code=503, 
            detail="Batch commands validator not available"
        )
    
    try:
        # Validate command_type parameter
        if request.command_type.lower() not in ['master', 'remote', 'set']:
            raise HTTPException(
                status_code=400,
                detail="command_type must be 'master', 'remote', or 'set'"
            )
        
        # Convert command_type string to enum
        command_type_map = {
            'master': CommandType.MASTER,
            'remote': CommandType.REMOTE,
            'set': CommandType.SET
        }
        command_type = command_type_map[request.command_type.lower()]
        
        # Initialize batch validator
        validator = BatchCommandsValidator()
        
        # Execute batch validation
        result = validator.validate_batch_commands(
            ip_address=request.ip_address,
            command_type=command_type,
            mode=request.mode,
            selected_commands=request.selected_commands
        )
        
        # Return structured response
        return BatchCommandsResponse(
            overall_status=result["overall_status"],
            command_type=result["command_type"],
            mode=result["mode"],
            ip_address=result["ip_address"],
            total_commands=result["total_commands"],
            commands_tested=result["commands_tested"],
            statistics=result["statistics"],
            results=result["results"],
            duration_ms=result["duration_ms"],
            timestamp=result["timestamp"]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Batch commands validation failed: {str(e)}"
        )


@app.get("/api/validation/supported-commands")
async def get_supported_commands() -> SupportedCommandsResponse:
    """
    Get list of all supported DRS commands for batch validation.
    
    Returns both master and remote commands with decoder mapping information.
    """
    if not BATCH_VALIDATION_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="Batch commands validator not available"
        )
    
    try:
        # Import decoder integration for mapping info
        from validation.decoder_integration import CommandDecoderMapping
        from validation.hex_frames import DRS_MASTER_FRAMES, DRS_REMOTE_FRAMES, DRS_SET_FRAMES
        
        # Get available commands from hex frames
        master_commands = list(DRS_MASTER_FRAMES.keys())
        remote_commands = list(DRS_REMOTE_FRAMES.keys())
        set_commands = list(DRS_SET_FRAMES.keys())
        
        # Get decoder mapping info
        decoder_mappings = {}
        for cmd in master_commands + remote_commands + set_commands:
            decoder_mappings[cmd] = CommandDecoderMapping.has_decoder(cmd)
        
        return SupportedCommandsResponse(
            master_commands=master_commands,
            remote_commands=remote_commands,
            set_commands=set_commands,
            total_commands=len(master_commands) + len(remote_commands) + len(set_commands),
            decoder_mappings=decoder_mappings
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get supported commands: {str(e)}"
        )


@app.get("/api/validation/batch-commands/status")
async def get_batch_commands_status():
    """Get batch commands system status and capabilities"""
    return {
        "batch_validation_available": BATCH_VALIDATION_AVAILABLE,
        "decoder_integration": BATCH_VALIDATION_AVAILABLE,
        "supported_modes": ["mock", "live"],
        "supported_command_types": ["master", "remote", "set"],
        "features": {
            "santone_decoder_integration": True,
            "hex_frame_generation": True,
            "timeout_handling": True,
            "detailed_statistics": True,
            "mock_testing": True,
            "live_device_testing": True
        },
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/results")
async def get_results() -> Dict[str, Any]:
    """Get validation results (alias for history endpoint)"""
    return await get_results_history()

@app.get("/api/results/history")
async def get_results_history(limit: int = 50) -> Dict[str, Any]:
    """Get validation results history"""
    try:
        results = []
        
        if RESULTS_DIR.exists():
            # Get all JSON files sorted by modification time (newest first)
            result_files = sorted(
                RESULTS_DIR.glob("*.json"),
                key=lambda x: x.stat().st_mtime,
                reverse=True
            )[:limit]
            
            for filepath in result_files:
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        data['filename'] = filepath.name
                        results.append(data)
                except Exception as e:
                    logging.warning(f"Error reading result file {filepath}: {e}")
        
        return {
            "status": "success",
            "count": len(results),
            "results": results
        }
        
    except Exception as e:
        logging.error(f"Error getting results history: {e}")
        return {
            "status": "error",
            "message": f"Failed to get results history: {str(e)}",
            "results": []
        }


@app.get("/api/results/{filename}")
async def get_result_file(filename: str):
    """Get a specific result file by filename"""
    try:
        filepath = RESULTS_DIR / filename
        
        if not filepath.exists():
            raise HTTPException(status_code=404, detail=f"Result file not found: {filename}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return JSONResponse(content=data)
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error reading result file {filename}: {e}")
        raise HTTPException(status_code=500, detail=f"Error reading result file: {str(e)}")


@app.get("/api/results/{filename}/download")
async def download_result_file(filename: str):
    """Download a specific result file"""
    try:
        filepath = RESULTS_DIR / filename
        
        if not filepath.exists():
            raise HTTPException(status_code=404, detail=f"Result file not found: {filename}")
        
        from fastapi.responses import FileResponse
        return FileResponse(
            path=filepath,
            filename=filename,
            media_type='application/json'
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error downloading result file {filename}: {e}")
        raise HTTPException(status_code=500, detail=f"Error downloading result file: {str(e)}")


@app.get("/api/results/export/csv")
async def export_results_to_csv():
    """Export all validation results to a CSV file"""
    try:
        import csv
        import io
        from fastapi.responses import StreamingResponse
        
        # Get all result files
        result_files = sorted(
            RESULTS_DIR.glob("*.json"),
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )
        
        # Create CSV in memory
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow([
            'Timestamp',
            'IP Address',
            'Device Type',
            'Serial Number',
            'Scenario',
            'Mode',
            'Overall Status',
            'Total Commands',
            'Passed',
            'Failed',
            'Timeouts',
            'Success Rate (%)',
            'Duration (ms)',
            'Average Duration (ms)'
        ])
        
        # Write data rows
        for filepath in result_files:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                request = data.get('request', {})
                result = data.get('result', {})
                stats = result.get('statistics', {})
                
                writer.writerow([
                    data.get('timestamp', 'N/A'),
                    request.get('ip_address', 'N/A'),
                    request.get('device_type', 'N/A'),
                    request.get('serial_number', 'N/A'),
                    request.get('hostname', 'N/A'),
                    'Live' if request.get('live_mode') else 'Mock',
                    result.get('overall_status', 'N/A'),
                    stats.get('total_commands', 0),
                    stats.get('passed', 0),
                    stats.get('failed', 0),
                    stats.get('timeouts', 0),
                    stats.get('success_rate', 0),
                    result.get('duration_ms', 0),
                    stats.get('average_duration_ms', 0)
                ])
            except Exception as e:
                logging.warning(f"Error reading result file {filepath}: {e}")
                continue
        
        # Prepare response
        output.seek(0)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"drs_validation_results_{timestamp}.csv"
        
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
    except Exception as e:
        logging.error(f"Error exporting results to CSV: {e}")
        raise HTTPException(status_code=500, detail=f"Error exporting results: {str(e)}")


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "timestamp": datetime.now().isoformat()
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.validation_app:app-modern", 
        host="0.0.0.0", 
        port=8080, 
        reload=True,
        reload_dirs=["src"],
        log_level="info"
    )
