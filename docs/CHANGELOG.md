# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.0] - 2025-10-07

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

## [2.0.0] - 2025-09-26

### Added
- Initial release of DRS Device Validation Tool
- FastAPI backend with WebSocket support
- Batch command validation for DRS protocol
- Real-time validation logging
- Docker containerization
- Modern web UI with validation controls
- Hex frame generation and validation
- Command response decoding
- Statistics and reporting

### Technical Stack
- **Backend**: FastAPI, Python 3.11
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Container**: Docker with development and production configs
- **Protocol**: Santone DRS protocol implementation
- **Testing**: pytest with asyncio support