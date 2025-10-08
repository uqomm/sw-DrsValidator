# -*- coding: utf-8 -*-
"""
Tramas hexadecimales pre-generadas para comandos DRS Santone Protocol.

Este archivo contiene todas las tramas hexadecimales necesarias para validar
comandos DRS usando el protocolo Santone. Las trif __name__ == "__main__":
    print("=== DRS Hex Frames Information ===")
    print(f"DRS Master Commands: {TOTAL_MASTER_COMMANDS}")
    print(f"DRS Remote Commands: {TOTAL_REMOTE_COMMANDS}")
    print(f"DRS Set Commands: {TOTAL_SET_COMMANDS}")
    print(f"Total Unique Commands: {TOTAL_UNIQUE_COMMANDS}")
    print()
    print("Sample Master Commands:")
    for i, (cmd, frame) in enumerate(list(DRS_MASTER_FRAMES.items())[:3]):
        print(f"  {cmd}: {frame}")
    print()
    print("Sample Remote Commands:")
    for i, (cmd, frame) in enumerate(list(DRS_REMOTE_FRAMES.items())[:3]):
        print(f"  {cmd}: {frame}")
    print()
    print("Sample Set Commands:")
    for i, (cmd, frame) in enumerate(list(DRS_SET_FRAMES.items())[:3]):
        print(f"  {cmd}: {frame}")eneradas usando
DigitalBoardProtocol con MODULE_FUNCTION=0x07.

Formato de trama: 7E + [ModFunc][ModAddr][DataType][CmdNum][Flag][Length][Data][CRC] + 7E
- 7E = START_FLAG
- 07 = MODULE_FUNCTION (DigitalBoard)
- 00 = MODULE_ADDRESS (0)
- 00 = DATA_INITIATION (0x00)
- XX = COMMAND_NUMBER (específico de cada comando)
- 00 = SUCCESS_FLAG (0x00)
- 00 = COMMAND_BODY_LENGTH (0 bytes - sin datos adicionales)
- XXXX = CRC checksum (calculado automáticamente)
- 7E = END_FLAG

Generado automáticamente el: 26/09/2025
"""

from typing import Dict, List

# Importar módulo de comandos de seteo
try:
    from .set_commands import SetCommands
    SET_COMMANDS_AVAILABLE = True
except ImportError:
    SET_COMMANDS_AVAILABLE = False

# Tramas para comandos DRS Master (15 comandos)
DRS_MASTER_FRAMES: Dict[str, str] = {
    # Comandos de puertos ópticos
    'optical_port_devices_connected_1': '7E070000F80000B2827E',
    'optical_port_devices_connected_2': '7E070000F9000082B57E', 
    'optical_port_devices_connected_3': '7E070000FA0000D2EC7E',
    'optical_port_devices_connected_4': '7E070000FB0000E2DB7E',
    
    # Comandos de potencia y canal
    'input_and_output_power': '7E070000F3000043727E',
    'channel_switch': '7E0700004200008CBB7E',
    'channel_frequency_configuration': '7E07000036000044BF7E',
    'central_frequency_point': '7E070000EB000081987E',
    'subband_bandwidth': '7E070000ED0000212A7E',
    
    # Comandos de configuración
    'broadband_switching': '7E0700008100002BC47E',
    'optical_port_switch': '7E07000091000048877E',
    'optical_port_status': '7E0700009A0000B9777E',
    
    # Comandos de identificación/estado
    'temperature': '7E07000002000021A67E',
    'device_id': '7E070000970000E8357E',
    'datt': '7E070000090000D0567E',
}

# Tramas para comandos SET (configuración) - Generadas dinámicamente
def get_set_command_frames() -> Dict[str, str]:
    """
    Genera tramas para comandos de configuración usando SetCommands
    """
    if not SET_COMMANDS_AVAILABLE:
        return {}

    frames = {}

    try:
        # Comando: Cambiar a modo WideBand
        frames['set_working_mode_wideband'] = SetCommands.set_working_mode(True).hex().upper()

        # Comando: Cambiar a modo Channel
        frames['set_working_mode_channel'] = SetCommands.set_working_mode(False).hex().upper()

        # Comando: Configurar atenuación (ejemplo: 10dB uplink, 15dB downlink para DMU)
        frames['set_attenuation_10_15_dmu'] = SetCommands.set_attenuation(10, 15, "dmu").hex().upper()

        # Comando: Configurar atenuación (ejemplo: 5dB uplink, 20dB downlink para DRU)
        frames['set_attenuation_5_20_dru'] = SetCommands.set_attenuation(5, 20, "dru").hex().upper()

        # Comando: Activar todos los canales
        frames['set_channels_all_on'] = SetCommands.set_channel_activation([True] * 16).hex().upper()

        # Comando: Desactivar todos los canales
        frames['set_channels_all_off'] = SetCommands.set_channel_activation([False] * 16).hex().upper()

        # Comando: Activar canales 1-8, desactivar 9-16
        frames['set_channels_first_8_on'] = SetCommands.set_channel_activation([True] * 8 + [False] * 8).hex().upper()

        # Comando: Configurar frecuencia de canal único (ejemplo: canal 0 con frecuencia 0x12345678)
        frames['set_single_channel_freq_0'] = SetCommands.set_single_channel_frequency(0, "12345678").hex().upper()

        # Comando: Configurar todas las frecuencias de canal (ejemplo: frecuencias por defecto)
        default_frequencies = ["12345678"] * 16  # Misma frecuencia para todos los canales
        frames['set_channel_frequency_configuration'] = SetCommands.set_channel_frequencies(default_frequencies).hex().upper()

        # Comando: Configurar frecuencias VHF (145-160 MHz)
        frames['set_vhf_frequencies'] = SetCommands.set_channel_frequencies(SetCommands.generate_vhf_frequencies()).hex().upper()

        # Comando: Configurar frecuencias P25 (851-869 MHz)
        frames['set_p25_frequencies'] = SetCommands.set_channel_frequencies(SetCommands.generate_p25_frequencies()).hex().upper()

        # Comando: Configurar frecuencias TETRA 400 (427-430 MHz)
        frames['set_tetra400_frequencies'] = SetCommands.set_channel_frequencies(SetCommands.generate_tetra400_frequencies()).hex().upper()

    except Exception as e:
        print(f"Warning: Error generating set command frames: {e}")
        return {}

    return frames

# Obtener tramas de seteo dinámicamente
DRS_SET_FRAMES: Dict[str, str] = get_set_command_frames()

# Tramas para comandos DRS Remote (13 comandos)
DRS_REMOTE_FRAMES: Dict[str, str] = {
    # Comandos básicos
    'temperature': '7E07000002000021A67E',
    'device_id': '7E070000970000E8357E', 
    'datt': '7E070000090000D0567E',
    
    # Comandos de potencia y canal
    'input_and_output_power': '7E070000F3000043727E',
    'channel_switch': '7E0700004200008CBB7E',
    'channel_frequency_configuration': '7E07000036000044BF7E',
    'central_frequency_point': '7E070000EB000081987E',
    'subband_bandwidth': '7E070000ED0000212A7E',
    
    # Comandos de configuración
    'broadband_switching': '7E0700008100002BC47E',
    'optical_port_switch': '7E07000091000048877E',
    'optical_port_status': '7E0700009A0000B9777E',
    
    # Comandos de puertos ópticos específicos
    'optical_port_devices_connected_1': '7E070000F80000B2827E',
    'optical_port_devices_connected_2': '7E070000F9000082B57E',
}

# Mapeo de comando a número hexadecimal para referencia
COMMAND_HEX_MAP: Dict[str, int] = {
    'optical_port_devices_connected_1': 0xF8,
    'optical_port_devices_connected_2': 0xF9,
    'optical_port_devices_connected_3': 0xFA,
    'optical_port_devices_connected_4': 0xFB,
    'input_and_output_power': 0xF3,
    'channel_switch': 0x42,
    'channel_frequency_configuration': 0x36,
    'central_frequency_point': 0xEB,
    'broadband_switching': 0x81,
    'optical_port_switch': 0x91,
    'optical_port_status': 0x9A,
    'subband_bandwidth': 0xED,
    'temperature': 0x02,
    'device_id': 0x97,
    'datt': 0x09,
}

def get_all_master_commands() -> List[str]:
    """Retorna lista de todos los comandos DRS Master disponibles."""
    return list(DRS_MASTER_FRAMES.keys())

def get_all_remote_commands() -> List[str]:
    """Retorna lista de todos los comandos DRS Remote disponibles.""" 
    return list(DRS_REMOTE_FRAMES.keys())

def get_all_set_commands() -> List[str]:
    """
    Obtiene lista de todos los comandos SET disponibles.
    
    Returns:
        Lista de nombres de comandos SET
    """
    return list(DRS_SET_FRAMES.keys())

def get_master_command_frame(command: str) -> str:
    """Obtiene la trama hexadecimal de un comando Master específico."""
    return DRS_MASTER_FRAMES.get(command, "")

def get_remote_command_frame(command: str) -> str:
    """Obtiene la trama hexadecimal de un comando Remote específico."""
    return DRS_REMOTE_FRAMES.get(command, "")

def get_set_command_frame(command: str) -> str:
    """Obtiene la trama hexadecimal de un comando SET específico."""
    return DRS_SET_FRAMES.get(command, "")

def get_all_master_set_commands() -> Dict[str, str]:
    """
    Retorna todos los comandos SET disponibles para Master
    
    Returns:
        dict: Diccionario con nombre_comando -> trama_hex
    """
    if not SET_COMMANDS_AVAILABLE:
        return {}
        
    commands = {}
    
    try:
        # SET Working Mode - WideBand
        commands['set_working_mode_wideband'] = SetCommands.set_working_mode(wideband=True).hex().upper()
        
        # SET Working Mode - Channel
        commands['set_working_mode_channel'] = SetCommands.set_working_mode(wideband=False).hex().upper()
        
        # SET Attenuation - Varios valores para probar
        commands['set_attenuation_10_15'] = SetCommands.set_attenuation(
            uplink_db=10,
            downlink_db=15,
            device_type="dmu"
        ).hex().upper()
        
        commands['set_attenuation_5_20'] = SetCommands.set_attenuation(
            uplink_db=5,
            downlink_db=20,
            device_type="dmu"
        ).hex().upper()
        
        # SET Channel Activation - Varios patrones
        commands['set_channels_all_on'] = SetCommands.set_channel_activation([True] * 16).hex().upper()
        commands['set_channels_all_off'] = SetCommands.set_channel_activation([False] * 16).hex().upper()
        commands['set_channels_first_8_on'] = SetCommands.set_channel_activation([True] * 8 + [False] * 8).hex().upper()
        
        # SET Channel Frequencies - VHF
        vhf_freqs = SetCommands.generate_vhf_frequencies()
        commands['set_channel_frequencies_vhf'] = SetCommands.set_channel_frequencies(vhf_freqs).hex().upper()
        
    except Exception as e:
        print(f"Error generating master SET commands: {e}")
        return {}
    
    return commands

def get_all_remote_set_commands() -> Dict[str, str]:
    """
    Retorna todos los comandos SET disponibles para Remote
    (SIN set_channel_frequencies y set_channel_activation)
    
    Returns:
        dict: Diccionario con nombre_comando -> trama_hex
    """
    if not SET_COMMANDS_AVAILABLE:
        return {}
        
    commands = {}
    
    try:
        # SET Working Mode - WideBand
        commands['remote_set_working_mode_wideband'] = SetCommands.set_working_mode(wideband=True).hex().upper()
        
        # SET Working Mode - Channel
        commands['remote_set_working_mode_channel'] = SetCommands.set_working_mode(wideband=False).hex().upper()
        
        # SET Attenuation - Varios valores para probar
        commands['remote_set_attenuation_12_18'] = SetCommands.set_attenuation(
            uplink_db=12,
            downlink_db=18,
            device_type="dru"
        ).hex().upper()
        
        commands['remote_set_attenuation_8_16'] = SetCommands.set_attenuation(
            uplink_db=8,
            downlink_db=16,
            device_type="dru"
        ).hex().upper()
        
    except Exception as e:
        print(f"Error generating remote SET commands: {e}")
        return {}
    
    return commands

def get_master_set_command_frame(command_name: str) -> str:
    """
    Obtiene la trama hexadecimal de un comando SET master específico
    
    Args:
        command_name: Nombre del comando SET
        
    Returns:
        str: Trama hexadecimal o cadena vacía si no existe
    """
    commands = get_all_master_set_commands()
    return commands.get(command_name, "")

def get_remote_set_command_frame(command_name: str) -> str:
    """
    Obtiene la trama hexadecimal de un comando SET remote específico
    
    Args:
        command_name: Nombre del comando SET
        
    Returns:
        str: Trama hexadecimal o cadena vacía si no existe
    """
    commands = get_all_remote_set_commands()
    return commands.get(command_name, "")


def get_master_frame(command: str) -> str:
    """
    Obtiene la trama hexadecimal para un comando DRS Master.
    
    Args:
        command: Nombre del comando (ej: 'device_id', 'temperature')
        
    Returns:
        Trama hexadecimal completa o cadena vacía si no existe
    """
    return DRS_MASTER_FRAMES.get(command, '')

def get_remote_frame(command: str) -> str:
    """
    Obtiene la trama hexadecimal para un comando DRS Remote.
    
    Args:
        command: Nombre del comando (ej: 'device_id', 'temperature')
        
    Returns:
        Trama hexadecimal completa o cadena vacía si no existe
    """
    return DRS_REMOTE_FRAMES.get(command, '')

def get_set_frame(command: str) -> str:
    """
    Obtiene la trama hexadecimal de un comando SET.
    
    Args:
        command: Nombre del comando SET
        
    Returns:
        Trama hexadecimal completa o cadena vacía si no existe
    """
    return DRS_SET_FRAMES.get(command, '')


def get_command_hex_code(command: str) -> int:
    """
    Obtiene el código hexadecimal de un comando.
    
    Args:
        command: Nombre del comando
        
    Returns:
        Código hexadecimal del comando o 0 si no existe
    """
    return COMMAND_HEX_MAP.get(command, 0)

def validate_frame_format(frame: str) -> bool:
    """
    Valida que una trama tenga el formato Santone correcto.
    
    Args:
        frame: Trama hexadecimal a validar
        
    Returns:
        True si la trama es válida, False en caso contrario
    """
    # Accept frames of various lengths: 20 (master/remote), 22/24 (set working/attenuation), 52 (set channels), 148/159 (set frequencies)
    if not frame or len(frame) not in [20, 22, 24, 52, 148, 159]:
        return False
    
    # Verificar START y END flags
    if not (frame.startswith('7E') and frame.endswith('7E')):
        return False
        
    # Verificar MODULE_FUNCTION (posición 2-3)
    if frame[2:4] != '07':
        return False
        
    # Verificar MODULE_ADDRESS (posición 4-5)
    if frame[4:6] != '00':
        return False
        
    # Verificar DATA_INITIATION (posición 6-7)  
    if frame[6:8] != '00':
        return False
        
    return True

# Estadísticas de tramas generadas
TOTAL_MASTER_COMMANDS = len(DRS_MASTER_FRAMES)
TOTAL_REMOTE_COMMANDS = len(DRS_REMOTE_FRAMES)
TOTAL_SET_COMMANDS = len(DRS_SET_FRAMES)
TOTAL_UNIQUE_COMMANDS = len(set(list(DRS_MASTER_FRAMES.keys()) + list(DRS_REMOTE_FRAMES.keys()) + list(DRS_SET_FRAMES.keys())))

if __name__ == "__main__":
    print("=== DRS Hex Frames Information ===")
    print(f"DRS Master Commands: {TOTAL_MASTER_COMMANDS}")
    print(f"DRS Remote Commands: {TOTAL_REMOTE_COMMANDS}")
    print(f"DRS Set Commands: {TOTAL_SET_COMMANDS}")
    print(f"Total Unique Commands: {TOTAL_UNIQUE_COMMANDS}")
    print()
    print("Sample Master Commands:")
    for i, (cmd, frame) in enumerate(list(DRS_MASTER_FRAMES.items())[:3]):
        print(f"  {cmd}: {frame}")
    print()
    print("Sample Remote Commands:")
    for i, (cmd, frame) in enumerate(list(DRS_REMOTE_FRAMES.items())[:3]):
        print(f"  {cmd}: {frame}")
    print()
    if DRS_SET_FRAMES:
        print("Sample Set Commands:")
        for i, (cmd, frame) in enumerate(list(DRS_SET_FRAMES.items())[:3]):
            print(f"  {cmd}: {frame}")
    else:
        print("No Set Commands available (SetCommands module not found)")
