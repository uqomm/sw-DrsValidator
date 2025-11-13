#!/usr/bin/env python3
"""
End-to-End Tests for DRS Validator

Tests complete validation workflows from API endpoints to results:
- Full validation runs (mock and live modes)
- WebSocket logging integration
- Result persistence and retrieval
- Batch command processing
- Scenario-based validation
- Error handling and edge cases
"""

import unittest
import sys
import asyncio
import json
import time
from pathlib import Path
from unittest.mock import patch, AsyncMock, MagicMock

# Add src to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

# Try to import FastAPI test client
try:
    from fastapi.testclient import TestClient
    from validation_app import app
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False
    # Create mock classes for testing when FastAPI is not available
    TestClient = None
    app = None
except Exception as e:
    # Handle path issues during import
    if "No such file or directory" in str(e):
        FASTAPI_AVAILABLE = False
        TestClient = None
        app = None
    else:
        raise


class TestEndToEndValidation(unittest.TestCase):
    """End-to-end test suite for complete validation workflows"""

    def setUp(self):
        """Set up test fixtures"""
        if not FASTAPI_AVAILABLE:
            self.skipTest("FastAPI test client not available")

        self.client = TestClient(app)
        self.test_ip = "192.168.1.100"
        self.test_client_id = f"test-e2e-{int(time.time())}"

    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn("status", data)
        self.assertIn("timestamp", data)
        self.assertEqual(data["status"], "healthy")

    def test_api_test_endpoint(self):
        """Test API test endpoint"""
        response = self.client.get("/api/test")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn("message", data)
        self.assertIn("timestamp", data)

    def test_supported_commands_endpoint(self):
        """Test supported commands endpoint"""
        response = self.client.get("/api/validation/supported-commands")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn("master_commands", data)
        self.assertIn("remote_commands", data)
        self.assertIn("total_commands", data)

        # Should have commands
        self.assertGreater(len(data["master_commands"]), 10)
        self.assertGreater(len(data["remote_commands"]), 10)
        self.assertGreater(data["total_commands"], 20)

    def test_validation_scenarios_endpoint(self):
        """Test validation scenarios endpoint"""
        response = self.client.get("/api/validation/scenarios")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn("scenarios", data)
        self.assertIsInstance(data["scenarios"], list)

    @patch('validation_app.BatchCommandsValidator')
    def test_batch_commands_validation_mock(self, mock_validator_class):
        """Test complete batch commands validation workflow in mock mode"""
        # Mock the validator
        mock_validator = MagicMock()
        mock_validator.validate_batch_commands.return_value = {
            "overall_status": "PASS",
            "command_type": "master",
            "mode": "mock",
            "ip_address": self.test_ip,
            "total_commands": 3,
            "commands_tested": 3,
            "statistics": {
                "total_commands": 3,
                "passed": 3,
                "failed": 0,
                "success_rate": 100.0
            },
            "results": [
                {
                    "command": "device_id",
                    "status": "PASS",
                    "duration_ms": 50,
                    "decoded_values": {"device_id": 12345}
                },
                {
                    "command": "temperature",
                    "status": "PASS",
                    "duration_ms": 45,
                    "decoded_values": {"temperature": 25.5}
                },
                {
                    "command": "optical_port_devices_connected_1",
                    "status": "PASS",
                    "duration_ms": 48,
                    "decoded_values": {"connected_devices": 2}
                }
            ],
            "duration_ms": 143,
            "timestamp": "2025-01-13T10:00:00Z"
        }
        mock_validator_class.return_value = mock_validator

        # Test request
        request_data = {
            "ip_address": self.test_ip,
            "command_type": "master",
            "mode": "mock",
            "selected_commands": ["device_id", "temperature", "optical_port_devices_connected_1"],
            "timeout_seconds": 3
        }

        response = self.client.post("/api/validation/batch-commands", json=request_data)
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data["overall_status"], "PASS")
        self.assertEqual(data["mode"], "mock")
        self.assertEqual(data["total_commands"], 3)
        self.assertEqual(len(data["results"]), 3)

        # Verify validator was called correctly
        mock_validator.validate_batch_commands.assert_called_once()
        call_args = mock_validator.validate_batch_commands.call_args
        self.assertEqual(call_args[1]["ip_address"], self.test_ip)
        self.assertEqual(call_args[1]["command_type"], "master")
        self.assertEqual(call_args[1]["mode"], "mock")

    @patch('validation_app.BatchCommandsValidator')
    def test_batch_commands_validation_with_timeouts(self, mock_validator_class):
        """Test batch commands validation with timeouts"""
        mock_validator = MagicMock()
        mock_validator.validate_batch_commands.return_value = {
            "overall_status": "FAIL",
            "command_type": "remote",
            "mode": "live",
            "ip_address": "192.168.1.200",  # Non-existent IP
            "total_commands": 2,
            "commands_tested": 2,
            "statistics": {
                "total_commands": 2,
                "passed": 0,
                "failed": 0,
                "timeouts": 2,
                "success_rate": 0.0
            },
            "results": [
                {
                    "command": "device_id",
                    "status": "TIMEOUT",
                    "duration_ms": 3000,
                    "error": "Connection timeout"
                },
                {
                    "command": "temperature",
                    "status": "TIMEOUT",
                    "duration_ms": 3000,
                    "error": "Connection timeout"
                }
            ],
            "duration_ms": 6000,
            "timestamp": "2025-01-13T10:00:00Z"
        }
        mock_validator_class.return_value = mock_validator

        request_data = {
            "ip_address": "192.168.1.200",
            "command_type": "remote",
            "mode": "live",
            "selected_commands": ["device_id", "temperature"]
        }

        response = self.client.post("/api/validation/batch-commands", json=request_data)
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data["overall_status"], "FAIL")
        self.assertEqual(data["statistics"]["timeouts"], 2)
        self.assertEqual(data["statistics"]["success_rate"], 0.0)

    def test_batch_commands_invalid_request(self):
        """Test batch commands endpoint with invalid request"""
        # Missing required fields
        invalid_request = {
            "mode": "mock"
            # Missing ip_address, command_type
        }

        response = self.client.post("/api/validation/batch-commands", json=invalid_request)
        # Should handle gracefully - either 422 validation error or custom error
        self.assertIn(response.status_code, [400, 422])

    @patch('validation_app.BackgroundTasks')
    @patch('validation_app.BatchCommandsValidator')
    def test_full_validation_run_workflow(self, mock_validator_class, mock_background_tasks):
        """Test complete validation run workflow"""
        mock_validator = MagicMock()
        mock_validator.validate_batch_commands.return_value = {
            "overall_status": "PASS",
            "command_type": "master",
            "mode": "mock",
            "ip_address": self.test_ip,
            "total_commands": 5,
            "statistics": {"success_rate": 100.0},
            "results": [],
            "duration_ms": 250,
            "timestamp": "2025-01-13T10:00:00Z"
        }
        mock_validator_class.return_value = mock_validator

        # Mock background tasks
        mock_background_tasks_instance = MagicMock()
        mock_background_tasks.return_value = mock_background_tasks_instance

        request_data = {
            'mode': 'mock',
            'scenario_id': 'master_test',
            'device_config': {
                'ip_address': self.test_ip,
                'device_type': 'master'
            },
            'client_id': self.test_client_id
        }

        response = self.client.post("/api/validation/run", json=request_data)
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn("client_id", data)
        self.assertIn("status", data)
        self.assertEqual(data["client_id"], self.test_client_id)

    def test_ping_device_endpoint_mock(self):
        """Test device ping endpoint in mock mode"""
        response = self.client.post(f"/api/validation/ping/{self.test_ip}?mode=mock")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn("reachable", data)
        self.assertIn("ip_address", data)
        self.assertEqual(data["ip_address"], self.test_ip)

    def test_results_endpoints(self):
        """Test results retrieval endpoints"""
        # Test results list
        response = self.client.get("/api/results")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIsInstance(data, list)

        # Test results history
        response = self.client.get("/api/results/history")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn("results", data)
        self.assertIsInstance(data["results"], list)

    def test_web_interface_endpoints(self):
        """Test web interface HTML endpoints"""
        # Test main page
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/html", response.headers.get("content-type", ""))

        # Test result page
        response = self.client.get("/result")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/html", response.headers.get("content-type", ""))

    def test_error_handling_invalid_ip(self):
        """Test error handling with invalid IP addresses"""
        request_data = {
            "ip_address": "invalid.ip.address",
            "command_type": "master",
            "mode": "mock",
            "selected_commands": ["device_id"]
        }

        response = self.client.post("/api/validation/batch-commands", json=request_data)
        # Should handle gracefully
        self.assertIn(response.status_code, [200, 400, 422])

    def test_validation_task_status_endpoint(self):
        """Test validation task status endpoint"""
        # Test with non-existent task
        response = self.client.get(f"/api/validation/task/nonexistent-task-id")
        # Should return 404 or appropriate error
        self.assertIn(response.status_code, [404, 422])

    def test_batch_commands_status_endpoint(self):
        """Test batch commands status endpoint"""
        response = self.client.get("/api/validation/batch-commands/status")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn("status", data)
        self.assertIn("timestamp", data)


class TestEndToEndIntegration(unittest.TestCase):
    """Integration tests for end-to-end workflows"""

    def setUp(self):
        """Set up integration test fixtures"""
        if not FASTAPI_AVAILABLE:
            self.skipTest("FastAPI test client not available")

        self.client = TestClient(app)

    def test_complete_validation_workflow(self):
        """Test complete validation workflow from start to finish"""
        # 1. Check health
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)

        # 2. Get supported commands
        response = self.client.get("/api/validation/supported-commands")
        self.assertEqual(response.status_code, 200)
        commands_data = response.json()

        # 3. Run validation with some commands
        master_commands = commands_data.get("master_commands", [])[:3]  # First 3 commands
        if master_commands:
            request_data = {
                "ip_address": "192.168.1.100",
                "command_type": "master",
                "mode": "mock",
                "selected_commands": master_commands
            }

            response = self.client.post("/api/validation/batch-commands", json=request_data)
            self.assertEqual(response.status_code, 200)

            validation_result = response.json()
            self.assertIn("overall_status", validation_result)
            self.assertIn("statistics", validation_result)

    def test_scenario_based_validation(self):
        """Test scenario-based validation workflow"""
        # Get available scenarios
        response = self.client.get("/api/validation/scenarios")
        self.assertEqual(response.status_code, 200)
        scenarios_data = response.json()

        if scenarios_data.get("scenarios"):
            # Use first available scenario
            scenario = scenarios_data["scenarios"][0]
            scenario_id = scenario.get("id")

            if scenario_id:
                request_data = {
                    'mode': 'mock',
                    'scenario_id': scenario_id,
                    'device_config': scenario.get("device_config", {}),
                    'client_id': f'test-scenario-{scenario_id}'
                }

                response = self.client.post("/api/validation/run", json=request_data)
                self.assertEqual(response.status_code, 200)

                result = response.json()
                self.assertIn("client_id", result)
                self.assertIn("status", result)


def run_e2e_tests():
    """Run end-to-end test suite"""
    print("=== 🚀 Running End-to-End Test Suite ===")
    print()

    # Create test suite
    test_suite = unittest.TestSuite()

    # Add test classes
    test_suite.addTest(unittest.makeSuite(TestEndToEndValidation))
    test_suite.addTest(unittest.makeSuite(TestEndToEndIntegration))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    # Summary
    print("\n=== 📊 End-to-End Tests Results Summary ===")
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
        print("🎉 ALL E2E TESTS PASSED - Complete workflow validated!")
    elif success_rate >= 80.0:
        print("✅ Most E2E tests passed - Minor integration issues to address")
    else:
        print("⚠️ Multiple E2E test failures detected - Integration issues require attention")

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_e2e_tests()
    sys.exit(0 if success else 1)