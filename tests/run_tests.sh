#!/bin/bash
# DRS Validation Test Suite - Helper Script
# Proporciona acceso rápido a los tests más comunes

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEST_SCRIPT="$SCRIPT_DIR/test_drs_validation_suite.py"

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Función para mostrar el menú
show_menu() {
    clear
    echo -e "${CYAN}╔════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║        DRS Validation Test Suite - Menú de Pruebas                ║${NC}"
    echo -e "${CYAN}╚════════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${GREEN}Tests Modo Mock (sin dispositivo físico):${NC}"
    echo "  1) Test Master Commands (15 comandos)"
    echo "  2) Test Remote Commands (13 comandos)"
    echo "  3) Test API Endpoint directo"
    echo "  4) Test WebSocket Logging"
    echo "  5) Todos los tests Mock"
    echo ""
    echo -e "${YELLOW}Tests Modo Live (requiere dispositivo DRS):${NC}"
    echo "  6) Test Live - Remote Commands"
    echo "  7) Test Live - Master Commands"
    echo "  8) Todos los tests (Mock + Live)"
    echo ""
    echo -e "${BLUE}Opciones avanzadas:${NC}"
    echo "  9) Test con output detallado (verbose)"
    echo " 10) Test con reporte JSON"
    echo " 11) Test custom (ingresar parámetros)"
    echo ""
    echo "  0) Salir"
    echo ""
    echo -e "${CYAN}════════════════════════════════════════════════════════════════════${NC}"
}

# Función para ejecutar test
run_test() {
    echo -e "\n${GREEN}Ejecutando test...${NC}\n"
    python3 "$TEST_SCRIPT" "$@"
    local exit_code=$?
    
    echo -e "\n${CYAN}════════════════════════════════════════════════════════════════════${NC}"
    if [ $exit_code -eq 0 ]; then
        echo -e "${GREEN}✅ Test completado exitosamente${NC}"
    else
        echo -e "${YELLOW}⚠️  Test completado con errores (código: $exit_code)${NC}"
    fi
    echo -e "${CYAN}════════════════════════════════════════════════════════════════════${NC}"
    
    echo ""
    read -p "Presiona Enter para continuar..."
}

# Loop principal
while true; do
    show_menu
    read -p "Selecciona una opción [0-11]: " choice
    
    case $choice in
        1)
            run_test --test master
            ;;
        2)
            run_test --test remote
            ;;
        3)
            run_test --test api
            ;;
        4)
            run_test --test websocket
            ;;
        5)
            run_test --test all
            ;;
        6)
            echo -e "\n${YELLOW}⚠️  Asegúrate de que el dispositivo DRS esté conectado en 192.168.11.22${NC}"
            read -p "¿Continuar? (s/N): " confirm
            if [[ $confirm == [sS] ]]; then
                run_test --test remote --live
            fi
            ;;
        7)
            echo -e "\n${YELLOW}⚠️  Asegúrate de que el dispositivo DRS esté conectado en 192.168.11.22${NC}"
            read -p "¿Continuar? (s/N): " confirm
            if [[ $confirm == [sS] ]]; then
                run_test --test master --live
            fi
            ;;
        8)
            echo -e "\n${YELLOW}⚠️  Esto ejecutará tests Mock y Live${NC}"
            echo -e "${YELLOW}    Requiere dispositivo DRS conectado${NC}"
            read -p "¿Continuar? (s/N): " confirm
            if [[ $confirm == [sS] ]]; then
                run_test --test all --live
            fi
            ;;
        9)
            echo -e "\n${BLUE}Tests disponibles:${NC}"
            echo "  1) Master"
            echo "  2) Remote"
            echo "  3) API"
            echo "  4) WebSocket"
            echo "  5) All"
            read -p "Selecciona test [1-5]: " test_choice
            
            case $test_choice in
                1) run_test --test master --verbose ;;
                2) run_test --test remote --verbose ;;
                3) run_test --test api --verbose ;;
                4) run_test --test websocket --verbose ;;
                5) run_test --test all --verbose ;;
                *) echo -e "${YELLOW}Opción inválida${NC}"; sleep 2 ;;
            esac
            ;;
        10)
            run_test --test all --save-report --verbose
            ;;
        11)
            echo -e "\n${BLUE}Test Custom${NC}"
            read -p "Test type [master/remote/api/websocket/all]: " test_type
            read -p "¿Modo verbose? (s/N): " verbose
            read -p "¿Incluir live? (s/N): " live
            read -p "¿Guardar reporte? (s/N): " report
            
            args="--test $test_type"
            [[ $verbose == [sS] ]] && args="$args --verbose"
            [[ $live == [sS] ]] && args="$args --live"
            [[ $report == [sS] ]] && args="$args --save-report"
            
            run_test $args
            ;;
        0)
            echo -e "\n${GREEN}👋 Adiós!${NC}\n"
            exit 0
            ;;
        *)
            echo -e "\n${YELLOW}⚠️  Opción inválida${NC}"
            sleep 2
            ;;
    esac
done
