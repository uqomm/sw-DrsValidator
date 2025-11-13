#!/usr/bin/env python3
"""
Scenarios - Gestión de escenarios de validación basados en launch.json
"""

import yaml
import sys
from pathlib import Path
from typing import Dict, List, Any

# Configurar paths
current_dir = Path(__file__).parent
config_dir = current_dir.parent / "config"

class ValidationScenarios:
    """Gestiona los escenarios de validación para técnicos."""
    
    def __init__(self, config_file: str = "validation_scenarios.yaml"):
        self.config_file = config_dir / config_file
        self.scenarios = self._load_scenarios()
    
    def _load_scenarios(self) -> Dict[str, Any]:
        """Cargar escenarios desde archivo YAML."""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                # Si el archivo está vacío, yaml.safe_load retorna None
                return data if data else self._get_default_scenarios()
        except FileNotFoundError:
            # Devolver configuraciones por defecto basadas en launch.json
            return self._get_default_scenarios()
        except yaml.YAMLError as e:
            print(f"Error loading scenarios: {e}")
            return self._get_default_scenarios()
    
    def _get_default_scenarios(self) -> Dict[str, Any]:
        """Configuraciones por defecto basadas en launch.json."""
        return {
            "validation_scenarios": [
                {
                    "id": "dru_remote_check",
                    "name": "DRU Remote Device Test",
                    "description": "Verificar dispositivo DRU remoto",
                    "device_config": {
                        "device_type": "dru_ethernet",
                        "default_ip": "192.168.11.100",
                        "default_hostname": "dru34132",
                        "cmd_type": "group_query",
                        "command": 155,
                        "optical_port": 1,
                        "thresholds": {
                            "warning_downlink": 38,
                            "warning_temperature": 45,
                            "warning_uplink": 38,
                            "critical_downlink": 41,
                            "critical_temperature": 50,
                            "critical_uplink": 31
                        }
                    },
                    "modes": {"mock": True, "live": True},
                    "enabled": True
                },
                {
                    "id": "device_discovery",
                    "name": "Device Discovery Process",
                    "description": "Proceso de descubrimiento automático de dispositivos",
                    "device_config": {
                        "device_type": "discovery_ethernet",
                        "default_ip": "192.168.11.22",
                        "default_hostname": "dmu",
                        "cmd_type": "group_query"
                    },
                    "modes": {"mock": True, "live": True},
                    "enabled": True
                }
            ]
        }
    
    def get_all_scenarios(self) -> List[Dict[str, Any]]:
        """Obtener todos los escenarios de validación."""
        return self.scenarios.get("validation_scenarios", [])
    
    def get_scenario(self, scenario_id: str) -> Dict[str, Any]:
        """Obtener escenario específico por ID."""
        scenarios = self.get_all_scenarios()
        for scenario in scenarios:
            if scenario.get("id") == scenario_id:
                return scenario
        return {}
    
    def get_enabled_scenarios(self) -> List[Dict[str, Any]]:
        """Obtener solo escenarios habilitados."""
        scenarios = self.get_all_scenarios()
        return [s for s in scenarios if s.get("enabled", False)]

# Instancia global para usar en la API
validation_scenarios = ValidationScenarios()
