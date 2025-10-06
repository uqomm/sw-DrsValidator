#!/usr/bin/env python3
"""
Script para probar conectividad con Jira API
"""
import os
import requests
import base64
import json
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def load_env():
    """Cargar variables de entorno desde .env.jira"""
    env_path = "/home/arturo/sw-DrsValidator/planning/.env.jira"
    env_vars = {}
    
    try:
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    # Remover comillas si existen
                    value = value.strip('"').strip("'")
                    env_vars[key] = value
        return env_vars
    except Exception as e:
        print(f"❌ Error leyendo .env.jira: {e}")
        return {}

def test_jira_connection():
    """Probar conectividad con Jira"""
    print("🔍 Probando conectividad con Jira API...")
    
    # Cargar configuración
    env = load_env()
    if not env:
        return False
    
    jira_url = env.get('JIRA_URL', '')
    username = env.get('JIRA_USERNAME', '')
    api_token = env.get('JIRA_API_TOKEN', '')
    
    print(f"URL: {jira_url}")
    print(f"Usuario: {username}")
    print(f"Token: {api_token[:20]}...")
    
    if not all([jira_url, username, api_token]):
        print("❌ Faltan variables de configuración")
        return False
    
    # Configurar sesión con reintentos
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    # Preparar autenticación
    auth_string = f"{username}:{api_token}"
    encoded_auth = base64.b64encode(auth_string.encode()).decode()
    
    headers = {
        'Authorization': f'Basic {encoded_auth}',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    
    try:
        # Probar endpoint de usuario actual
        print("\n🔗 Probando endpoint /myself...")
        response = session.get(
            f"{jira_url}/rest/api/3/myself",
            headers=headers,
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ Autenticación exitosa!")
            print(f"Usuario: {user_data.get('displayName', 'N/A')}")
            print(f"Email: {user_data.get('emailAddress', 'N/A')}")
            return True
        else:
            print(f"❌ Error de autenticación: {response.status_code}")
            print(f"Respuesta: {response.text[:200]}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def test_issue_access():
    """Probar acceso a issues específicas"""
    print("\n🎯 Probando acceso a issues...")
    
    env = load_env()
    if not env:
        return False
    
    jira_url = env.get('JIRA_URL', '')
    username = env.get('JIRA_USERNAME', '')
    api_token = env.get('JIRA_API_TOKEN', '')
    
    # Configurar sesión
    session = requests.Session()
    auth_string = f"{username}:{api_token}"
    encoded_auth = base64.b64encode(auth_string.encode()).decode()
    
    headers = {
        'Authorization': f'Basic {encoded_auth}',
        'Accept': 'application/json'
    }
    
    issues_to_test = ['SWDM-16', 'SWDM-18', 'SWDM-19']
    
    for issue_key in issues_to_test:
        try:
            response = session.get(
                f"{jira_url}/rest/api/3/issue/{issue_key}?fields=key,status,summary",
                headers=headers,
                timeout=15
            )
            
            if response.status_code == 200:
                issue_data = response.json()
                print(f"✅ {issue_key}: {issue_data['fields']['status']['name']} - {issue_data['fields']['summary'][:50]}")
            else:
                print(f"❌ {issue_key}: Error {response.status_code}")
                
        except Exception as e:
            print(f"❌ {issue_key}: Error de conexión - {e}")
    
    return True

if __name__ == "__main__":
    print("🔧 Test de Conectividad Jira API")
    print("=" * 40)
    
    if test_jira_connection():
        test_issue_access()
    else:
        print("\n❌ No se pudo establecer conectividad básica con Jira")
        print("Posibles causas:")
        print("- Token de API expirado o incorrecto")
        print("- Problemas de red corporativa/firewall")
        print("- URL de Jira incorrecta")
        print("- Restricciones de acceso al proyecto")