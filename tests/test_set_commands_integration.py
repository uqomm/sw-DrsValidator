#!/usr/bin/env python3
"""
Test de integración para comandos SET en el sistema de validación
"""

import sys
sys.path.insert(0, '/app')

from src.validation.batch_commands_validator import BatchCommandsValidator, CommandType

def test_master_set_commands():
    """Test de comandos SET para Master"""
    print("\n" + "="*80)
    print("TEST: Master SET Commands")
    print("="*80)

    validator = BatchCommandsValidator()

    result = validator.validate_batch_commands(
        ip_address="192.168.1.100",
        command_type=CommandType.MASTER,
        mode="mock",
        selected_commands=None  # Todos los comandos (GET + SET)
    )

    print(f"\n✅ Estado: {result['overall_status']}")
    print(f"📊 Total comandos: {result['statistics']['total_commands']}")
    print(f"🔍 Comandos GET: {len([c for c in result['results'] if not (c['command'].startswith('set_') or c['command'].startswith('remote_set_'))])}")
    print(f"⚙️ Comandos SET: {len([c for c in result['results'] if c['command'].startswith('set_') or c['command'].startswith('remote_set_')])}")
    print(f"✅ Exitosos: {result['statistics']['passed']}")
    print(f"❌ Fallidos: {result['statistics']['failed']}")

    # Mostrar comandos SET específicamente
    print("\n📋 Comandos SET ejecutados:")
    set_commands = [c for c in result['results'] if c['command'].startswith('set_')]
    for cmd in set_commands:
        print(f"  • {cmd['command']}: {cmd['status']}")

    # Assertions para pytest
    assert result['overall_status'] == 'PASS', "Master validation should pass"
    assert result['statistics']['total_commands'] > 0, "Should have commands"
    assert len(set_commands) > 0, "Should have SET commands"

def test_remote_set_commands():
    """Test de comandos SET para Remote (sin channel_frequencies y channel_activation)"""
    print("\n" + "="*80)
    print("TEST: Remote SET Commands")
    print("="*80)

    validator = BatchCommandsValidator()

    result = validator.validate_batch_commands(
        ip_address="192.168.1.200",
        command_type=CommandType.REMOTE,
        mode="mock",
        selected_commands=None
    )

    print(f"\n✅ Estado: {result['overall_status']}")
    print(f"📊 Total comandos: {result['statistics']['total_commands']}")
    print(f"🔍 Comandos GET: {len([c for c in result['results'] if not (c['command'].startswith('set_') or c['command'].startswith('remote_set_'))])}")
    print(f"⚙️ Comandos SET: {len([c for c in result['results'] if c['command'].startswith('set_') or c['command'].startswith('remote_set_')])}")

    # Verificar que NO hay comandos de canales
    set_commands = [c['command'] for c in result['results'] if c['command'].startswith('set_') or c['command'].startswith('remote_set_')]
    print("\n📋 Comandos SET ejecutados:")
    for cmd_name in set_commands:
        print(f"  • {cmd_name}")

    # Verificaciones
    has_channel_freq = any('channel_frequencies' in cmd for cmd in set_commands)
    has_channel_activation = any('channel_activation' in cmd for cmd in set_commands)

    if has_channel_freq:
        print("\n❌ ERROR: Remote tiene comandos de channel_frequencies")
    else:
        print("\n✅ Verificación: Remote NO tiene comandos de channel_frequencies (correcto)")

    if has_channel_activation:
        print("❌ ERROR: Remote tiene comandos de channel_activation")
    else:
        print("✅ Verificación: Remote NO tiene comandos de channel_activation (correcto)")

    # Assertions para pytest
    assert result['overall_status'] == 'PASS', "Remote validation should pass"
    assert result['statistics']['total_commands'] > 0, "Should have commands"
    assert not has_channel_freq, "Remote should NOT have channel_frequencies commands"
    assert not has_channel_activation, "Remote should NOT have channel_activation commands"

if __name__ == "__main__":
    print("🧪 Prueba de Integración: Comandos SET en Sistema de Validación")

    # Test Master
    print("\n" + "="*80)
    print("Ejecutando test_master_set_commands...")
    print("="*80)
    test_master_set_commands()

    # Test Remote
    print("\n" + "="*80)
    print("Ejecutando test_remote_set_commands...")
    print("="*80)
    test_remote_set_commands()

    print("\n" + "="*80)
    print("✅ TESTS COMPLETADOS")
    print("="*80)