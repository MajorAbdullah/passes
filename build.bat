@echo off
echo SecurePass Password Manager - Quick EXE Builder
echo ================================================

echo Installing required packages...
pip install -r requirements.txt

echo.
echo Building executable...
python build_exe.py

echo.
echo Build process completed!
pause
