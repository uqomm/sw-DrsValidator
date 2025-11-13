#!/usr/bin/env python3
"""
Unit Tests for Configuration Management

Tests YAML configuration loading, scenario management, and validation:
- ValidationScenarios class functionality
- YAML file parsing and validation
- Scenario retrieval and filtering
- Configuration error handling
- Default scenario fallbacks
"""

import unittest
import sys
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, mock_open

# Add src to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from validation.scenarios import ValidationScenarios


class TestValidationScenarios(unittest.TestCase):
    """Test suite for ValidationScenarios functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.temp_dir, "test_scenarios.yaml")

        # Sample valid configuration
        self.valid_config = {
            "validation_scenarios": [
                {
                    "id": "test_scenario_1",
                    "name": "Test Scenario 1",
                    "description": "First test scenario",
                    "device_config": {
                        "device_type": "master",
                        "default_ip": "192.168.1.100",
                        "default_hostname": "test-device-1"
                    },
                    "validation_criteria": {
                        "must_connect": True,
                        "response_timeout_seconds": 10,
                        "temperature_range": [10, 50]
                    },
                    "modes": {"mock": True, "live": True},
                    "enabled": True
                },
                {
                    "id": "test_scenario_2",
                    "name": "Test Scenario 2",
                    "description": "Second test scenario",
                    "device_config": {
                        "device_type": "remote",
                        "default_ip": "192.168.1.200",
                        "default_hostname": "test-device-2"
                    },
                    "modes": {"mock": True, "live": False},
                    "enabled": False
                }
            ],
            "validation_modes": {
                "mock": {
                    "description": "Mock mode for testing",
                    "use_case": "Development and testing"
                },
                "live": {
                    "description": "Live mode with real devices",
                    "use_case": "Production validation"
                }
            }
        }

    def tearDown(self):
        """Clean up test fixtures"""
        # Remove temporary files
        if os.path.exists(self.config_file):
            os.remove(self.config_file)
        os.rmdir(self.temp_dir)

    def test_initialization_with_valid_config(self):
        """Test ValidationScenarios initialization with valid config file"""
        # Create temporary config file
        import yaml
        with open(self.config_file, 'w') as f:
            yaml.dump(self.valid_config, f)

        # Mock the config directory path
        with patch('validation.scenarios.config_dir', Path(self.temp_dir)):
            scenarios = ValidationScenarios("test_scenarios.yaml")

            self.assertIsNotNone(scenarios.scenarios)
            self.assertIn("validation_scenarios", scenarios.scenarios)
            self.assertEqual(len(scenarios.scenarios["validation_scenarios"]), 2)

    def test_initialization_with_missing_file(self):
        """Test ValidationScenarios initialization with missing config file"""
        # Use non-existent file
        with patch('validation.scenarios.config_dir', Path(self.temp_dir)):
            scenarios = ValidationScenarios("nonexistent.yaml")

            # Should fall back to default scenarios
            self.assertIsNotNone(scenarios.scenarios)
            self.assertIn("validation_scenarios", scenarios.scenarios)
            # Should have at least the default scenarios
            self.assertGreaterEqual(len(scenarios.scenarios["validation_scenarios"]), 2)

    def test_initialization_with_invalid_yaml(self):
        """Test ValidationScenarios initialization with invalid YAML"""
        # Create file with invalid YAML
        with open(self.config_file, 'w') as f:
            f.write("invalid: yaml: content: [\n")

        with patch('validation.scenarios.config_dir', Path(self.temp_dir)):
            scenarios = ValidationScenarios("test_scenarios.yaml")

            # Should fall back to default scenarios
            self.assertIsNotNone(scenarios.scenarios)
            self.assertIn("validation_scenarios", scenarios.scenarios)

    def test_get_all_scenarios(self):
        """Test retrieving all scenarios"""
        import yaml
        with open(self.config_file, 'w') as f:
            yaml.dump(self.valid_config, f)

        with patch('validation.scenarios.config_dir', Path(self.temp_dir)):
            scenarios = ValidationScenarios("test_scenarios.yaml")

            all_scenarios = scenarios.get_all_scenarios()
            self.assertEqual(len(all_scenarios), 2)
            self.assertEqual(all_scenarios[0]["id"], "test_scenario_1")
            self.assertEqual(all_scenarios[1]["id"], "test_scenario_2")

    def test_get_scenario_by_id(self):
        """Test retrieving specific scenario by ID"""
        import yaml
        with open(self.config_file, 'w') as f:
            yaml.dump(self.valid_config, f)

        with patch('validation.scenarios.config_dir', Path(self.temp_dir)):
            scenarios = ValidationScenarios("test_scenarios.yaml")

            # Test existing scenario
            scenario = scenarios.get_scenario("test_scenario_1")
            self.assertEqual(scenario["id"], "test_scenario_1")
            self.assertEqual(scenario["name"], "Test Scenario 1")

            # Test non-existing scenario
            scenario = scenarios.get_scenario("nonexistent")
            self.assertEqual(scenario, {})

    def test_get_enabled_scenarios(self):
        """Test retrieving only enabled scenarios"""
        import yaml
        with open(self.config_file, 'w') as f:
            yaml.dump(self.valid_config, f)

        with patch('validation.scenarios.config_dir', Path(self.temp_dir)):
            scenarios = ValidationScenarios("test_scenarios.yaml")

            enabled_scenarios = scenarios.get_enabled_scenarios()
            self.assertEqual(len(enabled_scenarios), 1)
            self.assertEqual(enabled_scenarios[0]["id"], "test_scenario_1")
            self.assertTrue(enabled_scenarios[0]["enabled"])

    def test_default_scenarios_structure(self):
        """Test default scenarios fallback structure"""
        with patch('validation.scenarios.config_dir', Path(self.temp_dir)):
            scenarios = ValidationScenarios("nonexistent.yaml")

            default_scenarios = scenarios.get_all_scenarios()
            self.assertGreaterEqual(len(default_scenarios), 2)

            # Check structure of first default scenario
            scenario = default_scenarios[0]
            required_fields = ["id", "name", "description", "device_config", "modes"]
            for field in required_fields:
                self.assertIn(field, scenario)

            # Check device_config structure
            device_config = scenario["device_config"]
            self.assertIn("device_type", device_config)
            self.assertIn("default_ip", device_config)

    def test_scenario_validation_criteria(self):
        """Test scenario validation criteria parsing"""
        import yaml
        with open(self.config_file, 'w') as f:
            yaml.dump(self.valid_config, f)

        with patch('validation.scenarios.config_dir', Path(self.temp_dir)):
            scenarios = ValidationScenarios("test_scenarios.yaml")

            scenario = scenarios.get_scenario("test_scenario_1")
            criteria = scenario.get("validation_criteria", {})

            self.assertIn("must_connect", criteria)
            self.assertIn("response_timeout_seconds", criteria)
            self.assertIn("temperature_range", criteria)
            self.assertEqual(criteria["response_timeout_seconds"], 10)
            self.assertEqual(criteria["temperature_range"], [10, 50])

    def test_scenario_modes_configuration(self):
        """Test scenario modes configuration"""
        import yaml
        with open(self.config_file, 'w') as f:
            yaml.dump(self.valid_config, f)

        with patch('validation.scenarios.config_dir', Path(self.temp_dir)):
            scenarios = ValidationScenarios("test_scenarios.yaml")

            # Test scenario with both modes enabled
            scenario1 = scenarios.get_scenario("test_scenario_1")
            self.assertTrue(scenario1["modes"]["mock"])
            self.assertTrue(scenario1["modes"]["live"])

            # Test scenario with only mock enabled
            scenario2 = scenarios.get_scenario("test_scenario_2")
            self.assertTrue(scenario2["modes"]["mock"])
            self.assertFalse(scenario2["modes"]["live"])

    def test_device_config_validation(self):
        """Test device configuration validation"""
        import yaml
        with open(self.config_file, 'w') as f:
            yaml.dump(self.valid_config, f)

        with patch('validation.scenarios.config_dir', Path(self.temp_dir)):
            scenarios = ValidationScenarios("test_scenarios.yaml")

            scenario = scenarios.get_scenario("test_scenario_1")
            device_config = scenario["device_config"]

            # Required fields
            self.assertIn("device_type", device_config)
            self.assertIn("default_ip", device_config)
            self.assertIn("default_hostname", device_config)

            # Field types
            self.assertIsInstance(device_config["device_type"], str)
            self.assertIsInstance(device_config["default_ip"], str)
            self.assertIsInstance(device_config["default_hostname"], str)

    def test_config_file_path_resolution(self):
        """Test configuration file path resolution"""
        with patch('validation.scenarios.config_dir', Path("/test/config/path")):
            scenarios = ValidationScenarios("custom_config.yaml")

            expected_path = Path("/test/config/path/custom_config.yaml")
            self.assertEqual(scenarios.config_file, expected_path)


class TestConfigurationValidation(unittest.TestCase):
    """Test configuration validation and error handling"""

    def test_yaml_parsing_error_handling(self):
        """Test YAML parsing error handling"""
        temp_dir = tempfile.mkdtemp()
        config_file = os.path.join(temp_dir, "invalid.yaml")

        try:
            # Create invalid YAML file
            with open(config_file, 'w') as f:
                f.write("invalid: yaml: content: [\ninvalid")

            with patch('validation.scenarios.config_dir', Path(temp_dir)):
                scenarios = ValidationScenarios("invalid.yaml")

                # Should not crash and should have default scenarios
                self.assertIsNotNone(scenarios.scenarios)
                self.assertIn("validation_scenarios", scenarios.scenarios)

        finally:
            if os.path.exists(config_file):
                os.remove(config_file)
            os.rmdir(temp_dir)

    def test_empty_config_file_handling(self):
        """Test handling of empty configuration file"""
        temp_dir = tempfile.mkdtemp()
        config_file = os.path.join(temp_dir, "empty.yaml")

        try:
            # Create empty YAML file
            with open(config_file, 'w') as f:
                f.write("")

            with patch('validation.scenarios.config_dir', Path(temp_dir)):
                scenarios = ValidationScenarios("empty.yaml")

                # Should fall back to defaults
                self.assertIsNotNone(scenarios.scenarios)
                default_scenarios = scenarios.get_all_scenarios()
                self.assertGreater(len(default_scenarios), 0)

        finally:
            if os.path.exists(config_file):
                os.remove(config_file)
            os.rmdir(temp_dir)


def run_configuration_tests():
    """Run configuration test suite"""
    print("=== 🔧 Running Configuration Management Test Suite ===")
    print()

    # Create test suite
    test_suite = unittest.TestSuite()

    # Add test classes
    test_suite.addTest(unittest.makeSuite(TestValidationScenarios))
    test_suite.addTest(unittest.makeSuite(TestConfigurationValidation))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    # Summary
    print("\n=== 📊 Configuration Tests Results Summary ===")
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    if result.failures:
        print("\n❌ FAILURES:")
        for test, failure in result.failures:
            print(f"  - {test}: {failure}")

    if result.errors:
        print("\n🚫 ERRORS:")
        for test, error in result.errors:
            print(f"  - {test}: {error}")

    success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun) * 100
    print(f"\n🎯 Overall Success Rate: {success_rate:.1f}%")

    if success_rate == 100.0:
        print("🎉 ALL CONFIGURATION TESTS PASSED - Configuration system ready!")
    elif success_rate >= 80.0:
        print("✅ Most configuration tests passed - Minor issues to address")
    else:
        print("⚠️ Multiple configuration test failures detected - Review required")

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_configuration_tests()
    sys.exit(0 if success else 1)