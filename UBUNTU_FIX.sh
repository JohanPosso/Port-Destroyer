#!/bin/bash
################################################################################
# Script para solucionar problema de python3-gi en Ubuntu
# 
# El problema: venv no tiene acceso a paquetes del sistema como python3-gi
# La solución: Recrear venv con --system-site-packages
################################################################################

echo "======================================"
echo "Port-Destroyer - Fix para Ubuntu"
echo "======================================"
echo ""

cd ~/Proyectos/Port-Destroyer

echo "[1/4] Instalando dependencias del sistema..."
sudo apt install -y gir1.2-appindicator3-0.1 python3-gi libcairo2-dev pkg-config python3-dev

echo ""
echo "[2/4] Eliminando venv antiguo..."
rm -rf venv

echo ""
echo "[3/4] Creando nuevo venv con acceso a paquetes del sistema..."
python3 -m venv --system-site-packages venv

echo ""
echo "[4/4] Instalando dependencias Python..."
source venv/bin/activate
pip install Pillow cairosvg

echo ""
echo "======================================"
echo "Instalación completada!"
echo "======================================"
echo ""
echo "Ahora ejecuta:"
echo "  source venv/bin/activate"
echo "  python3 port_destroyer_tray_linux.py"
echo ""
echo "NO uses sudo, no es necesario para ver puertos."
echo "Solo usa sudo si necesitas MATAR procesos de otros usuarios."
echo ""

