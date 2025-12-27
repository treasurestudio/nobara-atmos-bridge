#!/bin/bash
echo "🚀 Launching Nobara Atmos Bridge..."
# This runs the monitor and the hub from the correct folders
python3 ./src/bridge_monitor.py &
python3 ./src/main.py
