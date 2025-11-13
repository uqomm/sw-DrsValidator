#!/usr/bin/env python3
"""
Unit Tests for Deployment Tools

Tests deployment functionality including:
- DRSDeployer class methods
- SSH connectivity and command execution
- Git and Docker installation checks
- Repository operations
- Container management
- Service verification
"""

import unittest
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add src to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

# Import deployment tools
sys.path.insert(0, str(project_root / "tools"))

# Try to import deploy module
try:
    from tools.deploy import DRSDeployer, Colors
    DEPLOY_AVAILABLE = True
except ImportError:
    DEPLOY_AVAILABLE = False
    # Create mock classes for testing
    class DRSDeployer:
        pass
    class Colors:
        GREEN = '\033[92m'
        RED = '\033[91m'
        YELLOW = '\033[93m'
        BLUE = '\033[94m'
        BOLD = '\033[1m'
        END = '\033[0m'


class TestDRSDeployer(unittest.TestCase):
    """Test suite for DRSDeployer functionality"""

    def setUp(self):
        """Set up test fixtures"""
        if not DEPLOY_AVAILABLE:
            self.skipTest("Deployment tools not available for testing")

        self.deployer = DRSDeployer(
            host="192.168.1.100",
            port=8089,
            user="testuser",
            dry_run=True  # Use dry run for testing
        )
        self.colors = Colors

    def test_deployer_initialization(self):
        """Test DRSDeployer initialization with different parameters"""
        # Test with password authentication
        deployer_with_pass = DRSDeployer(
            host="192.168.1.100",
            password="testpass",
            dry_run=True
        )
        self.assertIn("sshpass", deployer_with_pass.ssh_cmd)
        self.assertIn("testpass", deployer_with_pass.ssh_cmd)

        # Test with SSH key authentication (default)
        deployer_with_key = DRSDeployer(
            host="192.168.1.100",
            dry_run=True
        )
        self.assertNotIn("sshpass", deployer_with_key.ssh_cmd)

        # Test custom parameters
        self.assertEqual(deployer_with_key.host, "192.168.1.100")
        self.assertEqual(deployer_with_key.port, 8089)
        self.assertEqual(deployer_with_key.user, "sigmadev")
        self.assertEqual(deployer_with_key.branch, "feature/ui-fixes-final")

    @patch('tools.deploy.subprocess.run')
    def test_run_remote_command_dry_run(self, mock_subprocess):
        """Test remote command execution in dry run mode"""
        result = self.deployer.run_remote_command("echo 'test'", "Test command")

        # In dry run mode, should return True without executing
        self.assertTrue(result)
        mock_subprocess.assert_not_called()

    @patch('tools.deploy.subprocess.run')
    def test_run_remote_command_success(self, mock_subprocess):
        """Test successful remote command execution"""
        # Configure deployer for actual execution
        self.deployer.dry_run = False

        mock_result = Mock()
        mock_result.stdout = "command output"
        mock_result.stderr = ""
        mock_subprocess.return_value = mock_result

        result = self.deployer.run_remote_command("echo 'test'", "Test command")

        self.assertEqual(result, "command output")
        mock_subprocess.assert_called_once()

    @patch('tools.deploy.subprocess.run')
    def test_run_remote_command_failure(self, mock_subprocess):
        """Test failed remote command execution"""
        self.deployer.dry_run = False

        # Simular CalledProcessError que es lo que el código captura
        from subprocess import CalledProcessError
        mock_subprocess.side_effect = CalledProcessError(1, 'cmd', stderr='Command failed')

        result = self.deployer.run_remote_command("failing command", "Test command")

        self.assertFalse(result)

    @patch('tools.deploy.DRSDeployer.run_remote_command')
    def test_check_ssh_connectivity(self, mock_run_cmd):
        """Test SSH connectivity checking"""
        mock_run_cmd.return_value = "SSH OK"

        result = self.deployer.check_ssh_connectivity()

        self.assertTrue(result)
        mock_run_cmd.assert_called_with("echo 'SSH OK'", "Verificando conectividad SSH")

    @patch('tools.deploy.DRSDeployer.run_remote_command')
    def test_check_git_installation_already_installed(self, mock_run_cmd):
        """Test Git installation check when already installed"""
        mock_run_cmd.return_value = "OK"

        result = self.deployer.check_git_installation()

        self.assertTrue(result)
        # Should check if git is available
        self.assertIn("command -v git", mock_run_cmd.call_args[0][0])

    @patch('tools.deploy.DRSDeployer.run_remote_command')
    def test_check_git_installation_auto_install(self, mock_run_cmd):
        """Test Git auto-installation when not present"""
        # First call returns NOT_FOUND, second call succeeds
        mock_run_cmd.side_effect = ["NOT_FOUND", True]

        result = self.deployer.check_git_installation()

        self.assertTrue(result)
        # Should attempt to install git
        install_call = mock_run_cmd.call_args_list[1]
        self.assertIn("apt-get install -y git", install_call[0][0])

    @patch('tools.deploy.DRSDeployer.run_remote_command')
    def test_check_docker_installation(self, mock_run_cmd):
        """Test Docker installation checking"""
        mock_run_cmd.return_value = "OK"

        result = self.deployer.check_docker_installation()

        self.assertTrue(result)
        mock_run_cmd.assert_called_with(
            "command -v docker &> /dev/null && echo 'OK' || echo 'NOT_FOUND'",
            "Verificando instalación de Docker"
        )

    @patch('tools.deploy.DRSDeployer.run_remote_command')
    def test_check_docker_compose(self, mock_run_cmd):
        """Test Docker Compose availability checking"""
        mock_run_cmd.return_value = "OK"

        result = self.deployer.check_docker_compose()

        self.assertTrue(result)
        mock_run_cmd.assert_called_with(
            "docker compose version &> /dev/null && echo 'OK' || docker-compose --version &> /dev/null && echo 'OK' || echo 'NOT_FOUND'",
            "Verificando docker-compose"
        )

    @patch('tools.deploy.DRSDeployer.run_remote_script')
    def test_update_repository_clone(self, mock_run_script):
        """Test repository cloning when directory doesn't exist"""
        mock_run_script.return_value = True

        result = self.deployer.update_repository()

        self.assertTrue(result)
        script_lines = mock_run_script.call_args[0][0]
        # Should contain git clone command
        script_text = "\n".join(script_lines)
        self.assertIn("git clone", script_text)
        self.assertIn(self.deployer.branch, script_text)

    @patch('tools.deploy.DRSDeployer.run_remote_script')
    def test_configure_port(self, mock_run_script):
        """Test port configuration in docker-compose.yml"""
        mock_run_script.return_value = True

        result = self.deployer.configure_port()

        self.assertTrue(result)
        script_lines = mock_run_script.call_args[0][0]
        script_text = "\n".join(script_lines)
        self.assertIn("sed -i", script_text)
        self.assertIn(str(self.deployer.port), script_text)

    @patch('tools.deploy.DRSDeployer.run_remote_script')
    def test_stop_containers(self, mock_run_script):
        """Test stopping existing containers"""
        mock_run_script.return_value = True

        result = self.deployer.stop_containers()

        self.assertTrue(result)
        script_lines = mock_run_script.call_args[0][0]
        script_text = "\n".join(script_lines)
        self.assertIn("docker-compose down", script_text)

    @patch('tools.deploy.DRSDeployer.run_remote_script')
    def test_build_and_start_containers(self, mock_run_script):
        """Test building and starting containers"""
        mock_run_script.return_value = True

        result = self.deployer.build_and_start_containers()

        self.assertTrue(result)
        script_lines = mock_run_script.call_args[0][0]
        script_text = "\n".join(script_lines)
        self.assertIn("docker-compose up -d --build", script_text)

    @patch('tools.deploy.DRSDeployer.run_remote_script')
    @patch('tools.deploy.requests.get')
    def test_verify_deployment_success(self, mock_requests, mock_run_script):
        """Test successful deployment verification"""
        self.deployer.dry_run = False

        # Mock the docker-compose ps script
        mock_run_script.return_value = "container status"

        mock_response = Mock()
        mock_response.status_code = 200
        mock_requests.return_value = mock_response

        result = self.deployer.verify_deployment()

        self.assertTrue(result)
        # Should succeed on first endpoint, so call_count should be 1
        self.assertEqual(mock_requests.call_count, 1)

    @patch('tools.deploy.DRSDeployer.run_remote_script')
    @patch('tools.deploy.requests.get')
    def test_verify_deployment_failure(self, mock_requests, mock_run_script):
        """Test failed deployment verification"""
        self.deployer.dry_run = False

        # Mock the docker-compose ps script
        mock_run_script.return_value = "container status"

        # Simular RequestException que es lo que el código captura
        from requests import RequestException
        mock_requests.side_effect = RequestException("Connection failed")

        result = self.deployer.verify_deployment()

        self.assertFalse(result)
        # Should try all 3 endpoints
        self.assertEqual(mock_requests.call_count, 3)

    def test_wait_for_service(self):
        """Test service waiting logic"""
        # In dry run mode, should not actually wait
        result = self.deployer.wait_for_service()
        # wait_for_service doesn't return a value, just logs
        self.assertIsNone(result)

    @patch('tools.deploy.DRSDeployer.run_remote_script')
    def test_show_logs(self, mock_run_script):
        """Test log display functionality"""
        mock_run_script.return_value = "log output"

        # show_logs no retorna un valor, solo imprime
        self.deployer.show_logs()

        # Verificar que se llamó con los parámetros correctos
        mock_run_script.assert_called_once()
        script_lines = mock_run_script.call_args[0][0]
        script_text = "\n".join(script_lines)
        self.assertIn("docker-compose logs --tail=10", script_text)

    def test_deploy_dry_run(self):
        """Test full deployment process in dry run mode"""
        # All methods should return True in dry run mode
        with patch.object(self.deployer, 'check_ssh_connectivity', return_value=True), \
             patch.object(self.deployer, 'check_git_installation', return_value=True), \
             patch.object(self.deployer, 'check_docker_installation', return_value=True), \
             patch.object(self.deployer, 'check_docker_compose', return_value=True), \
             patch.object(self.deployer, 'update_repository', return_value=True), \
             patch.object(self.deployer, 'configure_port', return_value=True), \
             patch.object(self.deployer, 'stop_containers', return_value=True), \
             patch.object(self.deployer, 'build_and_start_containers', return_value=True), \
             patch.object(self.deployer, 'wait_for_service'), \
             patch.object(self.deployer, 'verify_deployment', return_value=True), \
             patch.object(self.deployer, 'show_logs'), \
             patch.object(self.deployer, 'show_summary'):

            result = self.deployer.deploy()

            self.assertTrue(result)

    def test_deploy_with_failure(self):
        """Test deployment process with a step failure"""
        with patch.object(self.deployer, 'check_ssh_connectivity', return_value=False):
            result = self.deployer.deploy()

            self.assertFalse(result)


class TestDeploymentUtilities(unittest.TestCase):
    """Test deployment utility functions and argument parsing"""

    @patch('tools.deploy.subprocess.run')
    def test_sshpass_check_in_main(self, mock_subprocess):
        """Test sshpass availability check in main function"""
        # This would require mocking argparse and the main function
        # For now, just test that the import works
        try:
            from tools.deploy import main
            self.assertTrue(callable(main))
        except ImportError:
            self.skipTest("deploy.py not available for testing")

    def test_colors_class(self):
        """Test Colors class constants"""
        try:
            from tools.deploy import Colors

            self.assertEqual(Colors.GREEN, '\033[92m')
            self.assertEqual(Colors.RED, '\033[91m')
            self.assertEqual(Colors.YELLOW, '\033[93m')
            self.assertEqual(Colors.BLUE, '\033[94m')
            self.assertEqual(Colors.BOLD, '\033[1m')
            self.assertEqual(Colors.END, '\033[0m')
        except ImportError:
            self.skipTest("deploy.py not available for testing")


def run_deployment_tests():
    """Run deployment test suite"""
    print("=== 🚀 Running Deployment Tools Test Suite ===")
    print()

    # Create test suite
    test_suite = unittest.TestSuite()

    # Add test classes
    test_suite.addTest(unittest.makeSuite(TestDRSDeployer))
    test_suite.addTest(unittest.makeSuite(TestDeploymentUtilities))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    # Summary
    print("\n=== 📊 Deployment Tests Results Summary ===")
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
        print("🎉 ALL DEPLOYMENT TESTS PASSED - Deployment tools ready!")
    elif success_rate >= 80.0:
        print("✅ Most deployment tests passed - Minor issues to address")
    else:
        print("⚠️ Multiple deployment test failures detected - Review required")

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_deployment_tests()
    sys.exit(0 if success else 1)