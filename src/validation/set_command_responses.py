#!/usr/bin/env python3
"""
Mock responses para comandos SET de DRS
Estas son respuestas de éxito/confirmación simuladas
"""

# Respuesta estándar de éxito para comandos SET
SET_SUCCESS_RESPONSE = "7E0700000000007E"  # ACK genérico

MASTER_SET_RESPONSES = {
    "set_working_mode_wideband": "7E070000800000C2D37E",
    "set_working_mode_channel": "7E070000800000C2D37E",
    "set_attenuation_10_15": "7E07000000E700002F427E",
    "set_attenuation_5_20": "7E07000000E700002F427E",
    "set_channels_all_on": "7E070000410000A1CA7E",
    "set_channels_all_off": "7E070000410000A1CA7E",
    "set_channels_first_8_on": "7E070000410000A1CA7E",
    "set_channel_frequencies_vhf": "7E070000350000D5EE7E",
}

REMOTE_SET_RESPONSES = {
    "remote_set_working_mode_wideband": "7E070000800000C2D37E",
    "remote_set_working_mode_channel": "7E070000800000C2D37E",
    "remote_set_attenuation_12_18": "7E07000000E700002F427E",
    "remote_set_attenuation_8_16": "7E07000000E700002F427E",
}

def get_master_set_mock_response(command_name: str) -> str:
    """Obtiene respuesta mock para comando SET master"""
    return MASTER_SET_RESPONSES.get(command_name, SET_SUCCESS_RESPONSE)

def get_remote_set_mock_response(command_name: str) -> str:
    """Obtiene respuesta mock para comando SET remote"""
    return REMOTE_SET_RESPONSES.get(command_name, SET_SUCCESS_RESPONSE)