#!/usr/bin/env bash
# Sets up a virtual environment, installs dependencies, and launches
# Lowkey Minesweeper. For macOS/Linux. Windows users: run setup.bat instead.
set -e

cd "$(dirname "$0")"

if [ ! -d ".venv" ]; then
    echo "Creating virtual environment (.venv)..."
    python3 -m venv .venv
fi

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "Setup complete. Launching Lowkey Minesweeper..."
python3 minesweeper.py
