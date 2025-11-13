#!/usr/bin/env python3
"""
DRS Validator - Automated Remote Deployment Script
Combines functionality from deploy-remote.sh and quick-deploy.sh

Usage:
    python deploy.py [options]

Examples:
    # Quick deploy to default server (192.168.60.140)
    python deploy.py

    # Deploy to custom server with password
    python deploy.py --host 192.168.11.22 --port 8089 --password mypass

    # Deploy with SSH key (default)
    python deploy.py --host 192.168.60.140 --branch main

    # Dry run to see what would be executed
    python deploy.py --dry-run
"""

import argparse
import subprocess
import sys
import time
import requests
from pathlib import Path

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

class DRSDeployer:
    def __init__(self, host, port=8089, user="root", password=None,
                 branch="feature/ui-fixes-final", remote_dir="/opt/drs-validation",
                 repo_url="https://github.com/arturoSigmadev/sw-DrsValidator.git",
                 dry_run=False):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.branch = branch
        self.remote_dir = remote_dir
        self.repo_url = repo_url
        self.dry_run = dry_run

        # SSH command setup
        if password:
            self.ssh_cmd = ["sshpass", "-p", password, "ssh", "-o", "StrictHostKeyChecking=no"]
        else:
            self.ssh_cmd = ["ssh", "-o", "StrictHostKeyChecking=no"]

        self.ssh_cmd.extend([f"{user}@{host}"])

    def log(self, message, color=Colors.BLUE):
        """Log a message with color"""
        print(f"{color}{message}{Colors.END}")

    def run_remote_command(self, command, description=""):
        """Execute a command on the remote server"""
        if description:
            self.log(f"🔄 {description}...", Colors.YELLOW)

        full_cmd = self.ssh_cmd + [command]

        if self.dry_run:
            self.log(f"DRY RUN: {' '.join(full_cmd)}", Colors.YELLOW)
            return True

        try:
            result = subprocess.run(full_cmd, capture_output=True, text=True, check=True)
            if description:
                self.log(f"✅ {description}", Colors.GREEN)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            self.log(f"❌ {description}: {e.stderr}", Colors.RED)
            return False

    def run_remote_script(self, script_lines, description=""):
        """Execute a multi-line script on the remote server"""
        script = "\n".join(script_lines)
        return self.run_remote_command(script, description)

    def check_ssh_connectivity(self):
        """Step 1: Check SSH connectivity"""
        return self.run_remote_command("echo 'SSH OK'", "Verificando conectividad SSH")

    def check_git_installation(self):
        """Step 1.5: Check if Git is installed on remote"""
        result = self.run_remote_command(
            "command -v git &> /dev/null && echo 'OK' || echo 'NOT_FOUND'",
            "Verificando instalación de Git"
        )
        if result == "OK":
            self.log("✅ Git instalado", Colors.GREEN)
            return True
        else:
            self.log("⚠️  Git no está instalado. Instalando...", Colors.YELLOW)
            # Instalar Git automáticamente
            install_result = self.run_remote_command(
                "apt-get update && apt-get install -y git",
                "Instalando Git"
            )
            if install_result:
                self.log("✅ Git instalado correctamente", Colors.GREEN)
                return True
            else:
                self.log("❌ Error instalando Git", Colors.RED)
                return False

    def check_docker_installation(self):
        """Step 2: Check if Docker is installed"""
        result = self.run_remote_command(
            "command -v docker &> /dev/null && echo 'OK' || echo 'NOT_FOUND'",
            "Verificando instalación de Docker"
        )
        if result == "OK":
            self.log("✅ Docker instalado", Colors.GREEN)
            return True
        else:
            self.log("❌ Docker no está instalado en el servidor remoto", Colors.RED)
            return False

    def check_docker_compose(self):
        """Step 2.5: Check if docker-compose is available"""
        result = self.run_remote_command(
            "docker compose version 2>/dev/null | grep -q 'Docker Compose' && echo 'OK' || echo 'NOT_FOUND'",
            "Verificando docker compose"
        )
        if result == "OK":
            self.log("✅ docker compose disponible", Colors.GREEN)
            return True
        else:
            self.log("❌ docker compose no está disponible", Colors.RED)
            return False

    def update_repository(self):
        """Step 3: Clone or update repository"""
        script = [
            f"if [ -d {self.remote_dir} ]; then",
            f"    cd {self.remote_dir}",
            f"    git fetch origin",
            f"    git checkout {self.branch}",
            f"    git pull origin {self.branch}",
            f"    echo 'Repository updated'",
            f"else",
            f"    git clone -b {self.branch} {self.repo_url} {self.remote_dir}",
            f"    echo 'Repository cloned'",
            f"fi"
        ]
        return self.run_remote_script(script, "Actualizando código desde GitHub")

    def configure_port(self):
        """Step 4: Update docker-compose.yml port"""
        script = [
            f"cd {self.remote_dir}",
            f"sed -i 's/- \"[0-9]*:8080\"/- \"{self.port}:8080\"/' docker-compose.yml",
            f"echo 'Port configured to {self.port}'"
        ]
        return self.run_remote_script(script, f"Configurando puerto {self.port}")

    def stop_containers(self):
        """Step 5: Stop existing containers"""
        script = [
            f"cd {self.remote_dir}",
            f"docker compose down || true",
            f"echo 'Containers stopped'"
        ]
        return self.run_remote_script(script, "Deteniendo contenedores existentes")

    def build_and_start_containers(self):
        """Step 6: Build and start containers"""
        script = [
            f"cd {self.remote_dir}",
            f"docker compose up -d --build",
            f"echo 'Containers started'"
        ]
        return self.run_remote_script(script, "Construyendo e iniciando contenedores")

    def wait_for_service(self):
        """Step 7: Wait for service to be ready"""
        self.log("⏳ Esperando que el servicio esté listo...", Colors.YELLOW)
        if not self.dry_run:
            time.sleep(5)
        self.log("✅ Servicio listo", Colors.GREEN)

    def verify_deployment(self):
        """Step 8: Verify deployment with multiple checks"""
        script = [
            f"cd {self.remote_dir}",
            f"docker compose ps"
        ]
        self.run_remote_script(script, "Verificando estado de contenedores")

        # Test service response with multiple endpoints
        if not self.dry_run:
            endpoints = [
                f"http://{self.host}:{self.port}/api/test",
                f"http://{self.host}:{self.port}/health",
                f"http://{self.host}:{self.port}/"
            ]

            for endpoint in endpoints:
                try:
                    response = requests.get(endpoint, timeout=10)
                    if response.status_code == 200:
                        self.log(f"✅ Servicio funcionando: {endpoint}", Colors.GREEN)
                        return True
                except requests.RequestException:
                    continue

            self.log("⚠️  Servicio puede no estar respondiendo correctamente", Colors.YELLOW)
            return False
        return True

    def show_logs(self):
        """Step 9: Show recent logs"""
        script = [
            f"cd {self.remote_dir}",
            f"docker compose logs --tail=10"
        ]
        self.log("📋 Últimas líneas del log:", Colors.BLUE)
        result = self.run_remote_script(script, "")
        if result:
            print(result)

    def show_summary(self):
        """Show deployment summary and useful commands"""
        print("\n" + "="*50)
        self.log("✅ Deployment completado exitosamente!", Colors.GREEN)
        print("="*50)
        print()
        self.log(f"🌐 Acceso al servicio: http://{self.host}:{self.port}", Colors.BLUE)
        print()
        self.log("📊 Comandos útiles:", Colors.BOLD)
        print(f"   Ver logs:      ssh {self.user}@{self.host} 'cd {self.remote_dir} && docker compose logs -f'")
        print(f"   Reiniciar:     ssh {self.user}@{self.host} 'cd {self.remote_dir} && docker compose restart'")
        print(f"   Detener:       ssh {self.user}@{self.host} 'cd {self.remote_dir} && docker compose down'")
        print(f"   Estado:        ssh {self.user}@{self.host} 'cd {self.remote_dir} && docker compose ps'")
        print()

    def deploy(self):
        """Execute full deployment process"""
        self.log("🚀 DRS Validator - Remote Deployment", Colors.BOLD)
        print("="*50)
        self.log(f"Target: {self.user}@{self.host}", Colors.BLUE)
        self.log(f"Port: {self.port}", Colors.BLUE)
        self.log(f"Branch: {self.branch}", Colors.BLUE)
        if self.dry_run:
            self.log("DRY RUN MODE - No actual changes will be made", Colors.YELLOW)
        print("="*50)
        print()

        steps = [
            self.check_ssh_connectivity,
            self.check_git_installation,
            self.check_docker_installation,
            self.check_docker_compose,
            self.update_repository,
            self.configure_port,
            self.stop_containers,
            self.build_and_start_containers,
            self.wait_for_service,
            self.verify_deployment,
            self.show_logs,
        ]

        for step in steps:
            if not step():
                self.log("❌ Deployment failed!", Colors.RED)
                return False

        self.show_summary()
        return True

def main():
    parser = argparse.ArgumentParser(
        description="DRS Validator - Automated Remote Deployment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Quick deploy to default server (192.168.60.140)
  python deploy.py

  # Deploy to custom server with password
  python deploy.py --host 192.168.11.22 --port 8089 --password mypass

  # Deploy with SSH key (default)
  python deploy.py --host 192.168.60.140 --branch main

  # Dry run to see what would be executed
  python deploy.py --dry-run
        """
    )

    parser.add_argument("--host", default="192.168.60.140",
                       help="Remote server hostname or IP (default: 192.168.60.140)")
    parser.add_argument("--port", type=int, default=8089,
                       help="Port to expose the service on (default: 8089)")
    parser.add_argument("--user", default="root",
                       help="SSH username (default: root)")
    parser.add_argument("--password",
                       help="SSH password (if not provided, uses SSH key authentication)")
    parser.add_argument("--branch", default="feature/ui-fixes-final",
                       help="Git branch to deploy (default: feature/ui-fixes-final)")
    parser.add_argument("--remote-dir", default="/opt/drs-validation",
                       help="Remote directory for deployment (default: /opt/drs-validation)")
    parser.add_argument("--repo-url",
                       default="https://github.com/arturoSigmadev/sw-DrsValidator.git",
                       help="Git repository URL")
    parser.add_argument("--dry-run", action="store_true",
                       help="Show what would be executed without making changes")

    args = parser.parse_args()

    # Check if sshpass is available when password is provided
    if args.password and not args.dry_run:
        try:
            subprocess.run(["sshpass", "-V"], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ sshpass is required for password authentication. Install with: apt-get install sshpass")
            sys.exit(1)

    deployer = DRSDeployer(
        host=args.host,
        port=args.port,
        user=args.user,
        password=args.password,
        branch=args.branch,
        remote_dir=args.remote_dir,
        repo_url=args.repo_url,
        dry_run=args.dry_run
    )

    success = deployer.deploy()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()