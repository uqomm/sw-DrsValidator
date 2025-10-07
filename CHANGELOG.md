# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.3.0] - 2025-10-07

### Added
- **Real-Time Detailed Logging**: Validation now shows comprehensive command execution details:
  - 📤 Command name and index (e.g., `[1/13] Comando: remote_read_band`)
  - 📋 Hex frames sent to device
  - 📥 Hex response frames received
  - 🔍 Decoded parameter values (frequency, power, etc.)
  - ✅ Individual command status and duration
- **CSV Export Functionality**: New endpoint `/api/results/export/csv` for exporting all validation results to CSV format
  - Includes: Timestamp, IP Address, Device Type, Serial Number, Scenario, Mode, Status, Commands, Success Rate, Duration
  - Automatic download with timestamped filename
  - Export button in Results tab
- **Device Serial Number Tracking**: Added serial number field to device configuration
  - Optional field in validation form with barcode icon
  - Included in saved results (JSON)
  - Displayed in results table as badge
  - Shown in result detail modal
  - Exported in CSV reports
- **Async Batch Validation**: Complete rewrite of validation execution for real-time WebSocket logging
  - New `validate_batch_commands_async()` method for non-blocking execution
  - Direct async execution instead of `asyncio.to_thread()`
  - Proper async/await pattern for WebSocket message streaming
  - Eliminates event loop conflicts

### Changed
- **UI Simplification**: Cleaned up interface to only show functional features
  - Removed "Comandos Batch" tab (unused)
  - Removed "Monitoreo" tab (fake data)
  - Removed "Ayuda" tab (no useful content)
  - Removed "Sistema Activo" static indicator from topbar
  - Final menu: **Validación** and **Resultados** only
- **Results Table Enhancement**: Added "Serial" column to results history table
  - Displays serial numbers as Bootstrap badges
  - Updated colspan from 6 to 7 for empty state
- **Keyboard Shortcuts Update**:
  - `Ctrl+1`: Validación
  - `Ctrl+2`: Resultados
  - `Ctrl+B`: Toggle Sidebar
  - Removed `Ctrl+3` (Help tab eliminated)

### Fixed
- **WebSocket Logging Issues**: Resolved async callback problems that prevented detailed logs from appearing
  - Fixed `asyncio.run()` creating conflicting event loops
  - Removed thread-based execution that broke async callbacks
  - Logs now properly stream via WebSocket to frontend
- **CSV Export Implementation**: Connected export button to backend endpoint
  - Added missing event listener for `exportResultsBtn`
  - Proper `StreamingResponse` handling with blob download
  - Filename extraction from `Content-Disposition` header
- **DeviceConfig Model**: Added `serial_number: Optional[str]` field to Pydantic model
- **Result Persistence**: Updated `save_validation_result()` to include serial number in saved JSON

### Technical Details
- **Logging Architecture**: Dual logging methods
  - `async def _log()`: For async contexts with WebSocket streaming
  - `def _log_sync()`: For sync contexts (fallback)
- **Validation Execution**: Two entry points
  - `validate_batch_commands()`: Sync version (no WebSocket)
  - `validate_batch_commands_async()`: Async version with real-time logs
- **CSV Generation**: In-memory CSV writer with `io.StringIO` for efficient streaming
- **Frontend**: Bootstrap 5 modals, WebSocket message parsing, async result loading
- **Docker**: Volume mount `/app/results` for persistent result storage

### Removed
- Batch commands upload functionality (`uploadBatchFile()`)
- Monitoring tab with fake CPU/Memory/Network stats
- Help tab with basic user guide
- Static "Sistema Activo" status indicator
- All references to removed tabs in breadcrumb and keyboard shortcuts

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