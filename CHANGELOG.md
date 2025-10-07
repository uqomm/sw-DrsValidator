# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.2.0] - 2025-10-07

### Added
- **SET Command Validation**: Integrated SET commands (configuration) into the batch validation system for both Master and Remote tests.
  - Master: 5 SET commands (working mode, attenuation, channel activation, channel frequencies)
  - Remote: 3 SET commands (working mode, attenuation only - no channel commands)
- **Hex Frame Display**: The validation output now displays the exact hexadecimal frames sent (📤) and received (📥) for each command.
- **Visual Command Differentiation**: UI now visually differentiates between GET (🔍) and SET (⚙️) commands with appropriate icons and messages.
- **Comprehensive Testing Framework**:
  - `test_drs_validation_suite.py`: Full CLI test suite with colored output and JSON reports
  - `run_tests.sh`: Interactive bash menu for test selection
  - `test_set_commands_integration.py`: SET command integration tests
  - `SISTEMA_TESTING_COMPLETO.md`: Complete testing documentation
- **CRC Calculation Dependency**: Added `crccheck==1.3.0` for proper SET command frame generation.
- **Validation Images**: Added band_system_validation.png, digital_board_validation_2.png, digital_board_validation_3.png
- **Documentation Translation**: Translated connectivity questions to English

### Changed
- **Batch Validation Engine**: Updated to handle both GET and SET commands in the same validation run.
- **API Response Format**: Added `is_set_command` flag to distinguish command types in UI.
- **UI Output**: Enhanced command display with hex frames and type-specific formatting.

### Fixed
- **JSON Serialization**: Corrected bug where hex frames and command details were not being included in API responses.
- **Command Frame Generation**: Fixed SET command frame generation with proper CRC calculation.

### Technical Details
- **Master Commands**: 15 GET + 5 SET = 20 total commands
- **Remote Commands**: 13 GET + 3 SET = 16 total commands
- **SET Commands Excluded from Remote**: `set_channel_frequencies_vhf` and `set_channel_activation` (as requested)
- **Mock Responses**: Implemented realistic ACK responses for SET commands
- **UI Integration**: Frontend properly handles and displays SET vs GET command differences

## [3.1.0] - 2025-09-26

### Added
- **Enhanced Logging System**: Implemented detailed logging for commands sent and responses received.
- **Persistent Result Storage**: Validation results are now saved persistently in `/app/results`.
- **Results History API**: New endpoint `/api/results/history` to query past validation results.

### Fixed
- **Device Port Correction**: Changed default device port to 65050 for TCP validation.
- **Container Path Compatibility**: Corrected all hardcoded paths (e.g., `/src/plugins/`) to be compatible with the Docker environment (`/app/plugins/`).

## [3.0.0] - 2025-09-26

### Added
- **Real Device Response Integration**: The system now uses authentic responses captured from a physical DRS Master device (`real_drs_responses_20250926_194004.py`).
- **"Batch Commands" Web Interface**: A new UI tab for executing and monitoring batch command validation.
- **SantoneDecoder Integration**: Professional parsing for 5 key commands.
- **TCP Response Collector**: `drs_response_collector.py` - System for capturing authentic DRS device responses.

### Fixed
- **Pydantic Validation Error**: Corrected the `commands_tested` field in the API schema from `int` to `List[str]`.
- **Ansible Deployment Fixes**: Resolved issues with template paths, port allocation, and removed obsolete configurations like UFW and Fail2ban.

### Technical Details
- **Command Coverage**: 28 DRS commands (15 Master + 13 Remote)
- **Test Success Rate**: 100% (6/6 test suites passed)
- **Real Device Integration**: 28 authentic responses captured from physical hardware

## [2.0.0] - 2025-09-25

### Added
- **Ansible Deployment Automation**: Complete migration to Ansible for automated, one-command deployment (`ansible-playbook site.yml`).
- **Repository Reorganization**: Structured the project with `docs/`, `scripts/`, and `ansible/` folders for better organization.

### Removed
- **Obsolete Deployment Scripts**: Removed old bash scripts (`install_minipc.sh`, `deploy_minipc.sh`, etc.) now replaced by Ansible.

## [1.0.0] - 2025-09-24

### Added
- **Initial Release**: First functional version of the DRS Validation Framework.
- **Core Validation Engine**: `TechnicianTCPValidator` with mock and live modes.
- **FastAPI Backend**: Full API with endpoints for scenarios, validation runs, and health checks.
- **Web Interface**: Initial UI with tabs for configuration and validation.
- **Docker Infrastructure**: `Dockerfile` and `docker-compose.yml` for easy setup.
- **Configuration System**: YAML-based scenarios in `config/validation_scenarios.yaml`.
- **Automated Test Suite**: PowerShell script (`test_framework.ps1`) for end-to-end testing.

### Technical Stack
- **Backend**: FastAPI, Python 3.11
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Container**: Docker with development and production configs
- **Protocol**: Santone DRS protocol implementation
- **Testing**: pytest with asyncio support