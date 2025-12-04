#!/usr/bin/env python3
"""
Script de ayuda para ejecutar el proyecto
Uso: python run_project.py [comando]

Comandos:
    setup       - Instalar dependencias
    backend     - Ejecutar backend
    frontend    - Ejecutar frontend
    test        - Ejecutar todas las pruebas
    test-unit   - Ejecutar pruebas unitarias
    test-int    - Ejecutar pruebas de integración
    test-e2e    - Ejecutar pruebas E2E
    lint        - Ejecutar análisis estático
    coverage    - Generar reporte de cobertura
    ci          - Simular pipeline CI
    help        - Mostrar esta ayuda
"""

import sys
import subprocess
import os


def run_command(cmd, cwd=None):
    """Ejecuta un comando en el shell"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            check=True
        )
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"Error ejecutando: {cmd}")
        print(f"Código de salida: {e.returncode}")
        return False


def setup():
    """Instalar dependencias"""
    print("📦 Instalando dependencias...")
    return run_command("pip install -r requirements.txt")


def run_backend():
    """Ejecutar backend"""
    print("🚀 Iniciando backend en http://localhost:5000")
    run_command("python app.py", cwd="backend")


def run_frontend():
    """Ejecutar frontend"""
    print("🌐 Iniciando frontend en http://localhost:3000")
    run_command("python app.py", cwd="frontend")


def run_tests():
    """Ejecutar todas las pruebas"""
    print("🧪 Ejecutando todas las pruebas...")
    return run_command("pytest tests/ -v --cov=backend")


def run_unit_tests():
    """Ejecutar pruebas unitarias"""
    print("🔬 Ejecutando pruebas unitarias...")
    return run_command("pytest tests/unit/ -v")


def run_integration_tests():
    """Ejecutar pruebas de integración"""
    print("🔗 Ejecutando pruebas de integración...")
    return run_command("pytest tests/integration/ -v")


def run_e2e_tests():
    """Ejecutar pruebas E2E"""
    print("🌍 Ejecutando pruebas E2E...")
    print("⚠️  Asegúrate de tener backend y frontend ejecutándose")
    return run_command("pytest tests/e2e/ -v")


def run_lint():
    """Ejecutar análisis estático"""
    print("🔍 Ejecutando Flake8...")
    flake_ok = run_command("flake8 backend/ frontend/ --count --show-source")

    print("\n🔒 Ejecutando Bandit...")
    bandit_ok = run_command("bandit -r backend/ -f txt")

    return flake_ok and bandit_ok


def run_coverage():
    """Generar reporte de cobertura"""
    print("📊 Generando reporte de cobertura...")
    if run_command("pytest --cov=backend --cov-report=html"):
        print("\n✅ Reporte generado en htmlcov/index.html")
        return True
    return False


def run_ci():
    """Simular pipeline CI"""
    print("🔄 Simulando pipeline CI...\n")

    steps = [
        ("Análisis estático - Flake8", run_lint),
        ("Pruebas unitarias", run_unit_tests),
        ("Pruebas de integración", run_integration_tests),
        ("Cobertura de código", run_coverage),
    ]

    for step_name, step_func in steps:
        print(f"\n{'=' * 50}")
        print(f"Ejecutando: {step_name}")
        print('=' * 50)

        if not step_func():
            print(f"\n❌ {step_name} FALLÓ")
            return False

        print(f"✅ {step_name} EXITOSO")

    print("\n" + "=" * 50)
    print("✅ Pipeline CI completado exitosamente")
    print("=" * 50)
    print("\n🎉 OK 🎉\n")
    return True


def show_help():
    """Mostrar ayuda"""
    print(__doc__)


def main():
    """Función principal"""
    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1].lower()

    commands = {
        'setup': setup,
        'backend': run_backend,
        'frontend': run_frontend,
        'test': run_tests,
        'test-unit': run_unit_tests,
        'test-int': run_integration_tests,
        'test-e2e': run_e2e_tests,
        'lint': run_lint,
        'coverage': run_coverage,
        'ci': run_ci,
        'help': show_help,
    }

    if command in commands:
        commands[command]()
    else:
        print(f"❌ Comando desconocido: {command}")
        show_help()


if __name__ == '__main__':
    main()