@echo off
REM Sets up a virtual environment, installs dependencies, and launches
REM Lowkey Minesweeper. For Windows. macOS/Linux users: run setup.sh instead.
setlocal

cd /d "%~dp0"

if not exist ".venv" (
    echo Creating virtual environment ^(.venv^)...
    python -m venv .venv
)

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo Setup complete. Launching Lowkey Minesweeper...
python minesweeper.py

pause
