@echo off
echo.
echo ========================================
echo     SecurePass Password Manager
echo         Installation Script
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.7 or higher from https://python.org
    pause
    exit /b 1
)

python --version
echo ✅ Python found!
echo.

echo Installing required packages...
echo.
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ❌ Failed to install dependencies
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

echo.
echo ✅ Installation completed successfully!
echo.
echo You can now run SecurePass using:
echo   - Double-click "run.bat"
echo   - Or run "python main.py" in this directory
echo.
echo 🔐 Welcome to SecurePass - Your Personal Password Manager!
echo.
pause
