# SW-DRS Validator - AI Coding Assistant Instructions

## Project Overview

This is a **DRS (Digital Radio System) validation framework** for VHF, P25, and LC500 radio systems. The system validates device connectivity, monitors LNA/PA performance, and provides automated testing capabilities for telecommunications equipment.

**Key Characteristics:**
- **FastAPI-based web application** with real-time validation
- **Dual operation modes**: Mock (simulation) and Live (real hardware)
- **Protocol**: Custom Santone binary protocol over TCP port 65050
- **Architecture**: Master/Remote device topology with batch command validation
- **Deployment**: Docker + Ansible for production environments

## Core Architecture

### Service Boundaries
```
DRS Validator System
├── validation_app.py          # FastAPI web server (port 8089)
├── validation/               # Core validation logic
│   ├── batch_commands_validator.py    # Batch command execution
│   ├── tcp_validator.py               # TCP connectivity tests
│   ├── hex_frames.py                  # Santone protocol frames
│   ├── decoder_integration.py         # Response decoding
│   └── standalone_validator.py        # Legacy validation
├── web/                     # Frontend (Jinja2 templates + JS)
└── config/                  # YAML configuration files
```

### Data Flow
1. **Web Interface** → FastAPI endpoints
2. **Command Selection** → Batch validator
3. **Frame Generation** → Hex encoding (Santone protocol)
4. **TCP Transmission** → Device communication (65050)
5. **Response Decoding** → Santone protocol parsing
6. **Result Aggregation** → JSON/HTML reporting

## Critical Developer Workflows

### Local Development (Hot Reload)
```bash
# Start development server with auto-reload
cd /home/arturo/sw-DrsValidator
export PYTHONPATH="$(pwd)/src"
python -m uvicorn src.validation_app:app --host 0.0.0.0 --port 8089 --reload

# Access interfaces:
# Web UI: http://localhost:8089
# API Docs: http://localhost:8089/docs
# Health: http://localhost:8089/health
```

### Testing Commands
```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_comprehensive.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

### Docker Development
```bash
# Build and run development container
docker-compose -f docker-compose.dev.yml up --build

# Access container logs
docker-compose logs -f drs-validation
```

### Production Deployment
```bash
# Ansible deployment (recommended)
cd ansible/
ansible-playbook -i inventory/hosts.yml playbooks/site.yml

# Manual deployment
docker-compose up -d
```

## Project-Specific Patterns

### Command Types & Validation Logic

**Master vs Remote Commands:**
- **Master**: Device control, monitoring, configuration (23 commands)
- **Remote**: Remote unit monitoring, status (17 commands)
- **SET Commands**: Configuration commands (prefixed with `set_` or `remote_set_`)

**Validation Flow:**
```python
# Always use this pattern for new commands
validator = BatchCommandsValidator()
result = validator.validate_batch_commands(
    ip_address="192.168.1.100",
    command_type=CommandType.MASTER,  # or REMOTE
    mode="mock",  # or "live"
    selected_commands=["device_id", "temperature"]
)
```

### Hex Frame Protocol

**Frame Structure:**
- **Header**: `7E 07 00 00` (Santone protocol identifier)
- **Command**: 2-byte command code
- **Data**: Variable-length payload
- **CRC**: 2-byte checksum
- **Footer**: `7E`

**Example Frame:**
```
7E 07 00 00 97 00 00 E8 35 7E  # device_id command
```

### Response Decoding

**Integrated Decoder Pattern:**
```python
# Use CommandDecoderMapping for known commands
if CommandDecoderMapping.has_decoder(command):
    decoded = create_mock_decoder_response(command, raw_bytes)
    return {
        "decoded_value": decoded,
        "status": "mock_enhanced",
        "decoder_mapping": True
    }
```

### Error Handling

**TCP Communication Errors:**
- **Timeout**: 3 seconds default per command
- **Connection Refused**: Device not reachable
- **Invalid Response**: Protocol parsing failures

**Validation Result States:**
- `PASS`: Command executed successfully
- `FAIL`: Command failed (no response/mock failure)
- `TIMEOUT`: TCP timeout exceeded
- `ERROR`: Frame generation or parsing error

## Integration Points

### External Dependencies
- **Jira Integration**: `jira_manager.py` for issue tracking
- **Ansible**: Infrastructure deployment
- **Docker**: Containerization
- **Santone Protocol**: Custom binary protocol

### Cross-Component Communication
- **WebSocket**: Real-time validation progress (`validation_app.py`)
- **JSON API**: RESTful endpoints for external integration
- **File Storage**: Results in `results/` directory
- **Logging**: Structured logging to `logs/` directory

## Development Conventions

### Code Organization
- **Imports**: Always use absolute imports with `src.` prefix
- **Constants**: Define in respective modules (e.g., `DRS_MASTER_FRAMES`)
- **Configuration**: Use YAML files in `src/config/`
- **Tests**: Mirror source structure in `tests/`

### Naming Patterns
- **Commands**: `snake_case` (e.g., `device_id`, `optical_port_status`)
- **Classes**: `PascalCase` (e.g., `BatchCommandsValidator`)
- **Files**: `snake_case.py` (e.g., `batch_commands_validator.py`)
- **SET Commands**: `set_*` or `remote_set_*` prefix

### Testing Patterns
```python
# Standard test structure
def test_feature_name(self):
    """Test description"""
    # Arrange
    validator = BatchCommandsValidator()
    
    # Act
    result = validator.validate_batch_commands(...)
    
    # Assert
    self.assertEqual(result["overall_status"], "PASS")
    self.assertGreater(result["statistics"]["passed"], 0)
```

## Key Files & Directories

### Essential Files
- `src/validation_app.py`: Main FastAPI application
- `src/validation/batch_commands_validator.py`: Core validation logic
- `src/validation/hex_frames.py`: Protocol frame definitions
- `src/config/validation_scenarios.yaml`: Test configurations
- `tests/test_comprehensive.py`: Main test suite

### Important Directories
- `src/web/`: Frontend templates and assets
- `ansible/`: Infrastructure deployment
- `docs/`: Technical documentation
- `results/`: Validation output storage
- `logs/`: Application logging

## Common Pitfalls

### Path Resolution
```python
# Always set PYTHONPATH for imports
export PYTHONPATH="$(pwd)/src"
```

### Port Configuration
- **Development**: Port 8089 (Docker) / 8080 (manual)
- **Production**: Port 8089 (MiniPC deployment)
- **TCP Device**: Port 65050 (Santone protocol)

### Mock vs Live Mode
- **Mock**: Use for development, testing, CI/CD
- **Live**: Only with real DRS hardware connected
- **Never mix modes** in production code

### Command Selection
```python
# Correct: Pass list of command names
selected_commands=["device_id", "temperature"]

# Incorrect: Pass dictionary (will cause AttributeError)
commands={"device_id": "frame_hex"}
```

## Performance Considerations

### Batch Validation
- **Timeout**: 3 seconds per command (configurable)
- **Parallelization**: Commands execute sequentially
- **Memory**: Results stored in memory until completion
- **Logging**: Extensive logging in development mode

### Database/Storage
- **No database**: File-based storage only
- **Results**: JSON files in `results/` directory
- **Retention**: Configurable cleanup (default: 30 days)
- **Threading**: Single-threaded execution

## Deployment Checklist

### Pre-deployment
- [ ] Update `requirements.txt`
- [ ] Run full test suite: `pytest tests/`
- [ ] Build Docker image: `docker build -t drs-validator .`
- [ ] Test container: `docker run --rm drs-validator --help`

### Production Deployment
- [ ] Configure Ansible inventory
- [ ] Set environment variables (SITE_ID, LOG_LEVEL)
- [ ] Verify network connectivity to DRS devices
- [ ] Test TCP port 65050 accessibility
- [ ] Configure log rotation and monitoring

### Post-deployment
- [ ] Verify web interface accessibility
- [ ] Test API endpoints: `/health`, `/docs`
- [ ] Validate device connectivity
- [ ] Check log files for errors

---

*This instruction file was generated by analyzing the SW-DRS Validator codebase. Last updated: November 13, 2025*