# DRS Validator Test Suite

Comprehensive test suite for the DRS validation system using pytest framework.

## 📋 Test Structure

The test suite is organized into multiple specialized test files:

```
tests/
├── test_comprehensive.py      # Core validation logic tests
├── test_deployment.py         # Deployment tools and scripts tests
├── test_configuration.py      # Configuration management tests
├── test_e2e.py               # End-to-end workflow tests
├── test_set_commands_integration.py  # SET commands integration tests
├── README.md                 # This documentation
└── __pycache__/              # Python cache files
```

### Test Categories

| Test File | Purpose | Coverage |
|-----------|---------|----------|
| `test_comprehensive.py` | Core validation logic, hex frames, decoders | Unit tests for BatchCommandsValidator |
| `test_deployment.py` | Deployment scripts, SSH, Docker operations | Tools/deploy.py functionality |
| `test_configuration.py` | YAML config loading, scenario management | Configuration system validation |
| `test_e2e.py` | Complete API workflows, integration tests | End-to-end validation flows |
| `test_set_commands_integration.py` | SET commands validation | Command type integration |

## 🚀 Quick Start

### Run All Tests
```bash
# From project root
python -m pytest tests/ -v

# With coverage report
python -m pytest tests/ --cov=src --cov-report=html
```

### Run Specific Test Files
```bash
# Core validation tests
python -m pytest tests/test_comprehensive.py -v

# Deployment tests
python -m pytest tests/test_deployment.py -v

# Configuration tests
python -m pytest tests/test_configuration.py -v

# End-to-end tests
python -m pytest tests/test_e2e.py -v

# SET commands tests
python -m pytest tests/test_set_commands_integration.py -v
```

### Run Tests by Category
```bash
# Unit tests only
python -m pytest tests/ -k "not e2e" -v

# Integration tests only
python -m pytest tests/test_e2e.py tests/test_set_commands_integration.py -v

# Fast tests (exclude slow integration tests)
python -m pytest tests/ -m "not slow" -v
```

## 📊 Test Coverage

### Current Coverage Areas

#### ✅ Core Validation (test_comprehensive.py)
- Hex frame generation and validation
- Command decoder mapping and integration
- Batch validation in mock/live modes
- Command type enum handling
- Error handling and edge cases
- Performance metrics tracking

#### ✅ Deployment Tools (test_deployment.py)
- DRSDeployer class initialization
- SSH connectivity and command execution
- Git installation and repository management
- Docker operations and container management
- Service verification and health checks
- Deployment workflow orchestration

#### ✅ Configuration Management (test_configuration.py)
- YAML file parsing and validation
- ValidationScenarios class functionality
- Scenario retrieval and filtering
- Configuration error handling
- Default scenario fallbacks

#### ✅ End-to-End Workflows (test_e2e.py)
- Complete API endpoint validation
- WebSocket logging integration
- Result persistence and retrieval
- Batch command processing workflows
- Scenario-based validation flows
- Error handling and edge cases

#### ✅ SET Commands Integration (test_set_commands_integration.py)
- Master SET commands validation
- Remote SET commands validation
- Command type differentiation
- SET vs GET command handling

## 🎯 Test Execution Modes

### Development Mode
```bash
# Run tests with auto-reload during development
python -m pytest tests/ -v --tb=short

# Run failed tests only
python -m pytest tests/ --lf

# Run tests and stop on first failure
python -m pytest tests/ -x
```

### CI/CD Mode
```bash
# Run all tests with coverage for CI
python -m pytest tests/ --cov=src --cov-report=xml --junitxml=results/test-results.xml

# Run tests in parallel (if pytest-xdist installed)
python -m pytest tests/ -n auto
```

### Debug Mode
```bash
# Verbose output with captured logs
python -m pytest tests/ -v -s

# Debug specific test
python -m pytest tests/test_comprehensive.py::TestBatchCommandsValidator::test_mock_decoder_integration -v -s
```

## 📈 Coverage Analysis

### Generate Coverage Reports
```bash
# HTML coverage report
python -m pytest tests/ --cov=src --cov-report=html
# View: open htmlcov/index.html

# Terminal coverage summary
python -m pytest tests/ --cov=src --cov-report=term-missing

# XML coverage for CI tools
python -m pytest tests/ --cov=src --cov-report=xml
```

### Coverage Goals
- **Core Logic**: >95% coverage
- **API Endpoints**: >90% coverage
- **Error Handling**: >85% coverage
- **Configuration**: >90% coverage
- **Deployment**: >80% coverage

## 🔧 Test Configuration

### Pytest Configuration
Tests use standard pytest configuration with the following markers:

```python
@pytest.mark.slow  # Mark slow-running tests
@pytest.mark.integration  # Mark integration tests
@pytest.mark.e2e  # Mark end-to-end tests
```

### Test Fixtures
Common test fixtures are available in `conftest.py` (when created):

- `test_client`: FastAPI test client
- `mock_validator`: Mocked BatchCommandsValidator
- `test_config`: Test configuration data
- `temp_dir`: Temporary directory for file operations

## 📋 Test Results and Reporting

### Test Output
```
======================== 17 passed, 3 skipped in 45.67s ========================
```

### Understanding Results
- **passed**: Tests that completed successfully
- **failed**: Tests that failed with assertion errors
- **skipped**: Tests skipped due to missing dependencies or conditions
- **errors**: Tests that failed with exceptions

### Common Test Failures

#### Import Errors
```
ImportError: No module named 'fastapi'
```
**Solution**: Install test dependencies
```bash
pip install -r requirements.txt
```

#### Network Timeouts
```
ConnectionError: Connection timed out
```
**Solution**: Ensure test server is running or use mock mode

#### File Permission Errors
```
PermissionError: [Errno 13] Permission denied
```
**Solution**: Check file permissions in test directories

## 🛠️ Test Maintenance

### Adding New Tests

#### Unit Test Pattern
```python
class TestNewFeature(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.test_data = {"key": "value"}

    def test_feature_functionality(self):
        """Test specific functionality"""
        result = some_function(self.test_data)
        self.assertEqual(result, expected_value)
```

#### Integration Test Pattern
```python
class TestFeatureIntegration(unittest.TestCase):
    def setUp(self):
        """Set up integration test fixtures"""
        self.client = TestClient(app)

    def test_api_endpoint_integration(self):
        """Test complete API workflow"""
        response = self.client.post("/api/endpoint", json=test_data)
        self.assertEqual(response.status_code, 200)
```

### Test Organization Guidelines

1. **One concept per test**: Each test should validate one specific behavior
2. **Descriptive names**: Use `test_feature_condition_expected_result` format
3. **Independent tests**: Tests should not depend on each other
4. **Fast execution**: Keep unit tests under 100ms, integration under 1s
5. **Proper cleanup**: Use `setUp`/`tearDown` or context managers

### Mocking Guidelines

```python
from unittest.mock import patch, MagicMock

@patch('module.Class.method')
def test_with_mock(self, mock_method):
    mock_method.return_value = expected_value
    # Test code here
```

## 🔍 Debugging Tests

### Debug Failed Tests
```bash
# Run with detailed traceback
python -m pytest tests/test_file.py::TestClass::test_method -v --tb=long

# Debug with pdb
python -m pytest tests/test_file.py::TestClass::test_method -v --pdb

# Print all variables on failure
python -m pytest tests/ -v --tb=short --capture=no
```

### Common Debug Scenarios

#### API Test Failures
```python
# Check API response details
response = self.client.get("/api/endpoint")
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
```

#### Mock Verification
```python
# Verify mock was called correctly
mock_method.assert_called_once_with(expected_arg)
print(f"Call args: {mock_method.call_args}")
```

## � References

- [DRS Validator Main Documentation](../docs/README.md)
- [Batch Commands API Guide](../docs/BATCH_COMMANDS_API_GUIDE.md)
- [Deployment Documentation](../docs/GUIA_DEPLOYMENT.md)
- [Configuration Guide](../docs/DOCUMENTACION_TECNICA.md)
- [pytest Documentation](https://docs.pytest.org/)

## 🤝 Contributing

When adding new tests:

1. Follow the existing naming conventions
2. Add appropriate docstrings
3. Include test cases for error conditions
4. Update this README if adding new test categories
5. Ensure tests run in CI/CD pipeline

### Test File Template
```python
#!/usr/bin/env python3
"""
Unit Tests for [Feature Name]

Tests [specific functionality] including:
- [Feature 1]
- [Feature 2]
- [Feature 3]
"""

import unittest
import sys
from pathlib import Path

# Add src to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

class TestFeatureName(unittest.TestCase):
    """Test suite for [Feature Name] functionality"""

    def setUp(self):
        """Set up test fixtures"""
        pass

    def test_feature_behavior(self):
        """Test [specific behavior]"""
        pass

def run_tests():
    """Run test suite"""
    # Test execution code here
    pass

if __name__ == "__main__":
    run_tests()
```
