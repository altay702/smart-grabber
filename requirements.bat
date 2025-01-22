@echo off
color 05

echo Installing required Python packages...

pip install requests
pip install colorama
pip install pyperclip
pip install astor
pip install pycryptodome
pip install pypiwin32

echo.
echo All packages have been installed successfully!

pause
