#!/bin/bash
################################################################################
# PortDestroyer - Universal Startup Script
#
# Author: Jesus Posso
# Version: 1.0.0
# License: MIT
#
# Description:
#   Starts the PortDestroyer system tray application with virtual environment
#   support. Works on macOS and Linux.
#
# Usage:
#   ./start_tray.sh
################################################################################

# Navigate to script directory
cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "[INFO] Activating virtual environment..."
    source venv/bin/activate
fi

# Start PortDestroyer system tray application
echo "[INFO] Starting PortDestroyer..."
python3 port_destroyer_tray.py --start 3000 --end 9000

