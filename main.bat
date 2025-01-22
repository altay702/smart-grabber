@echo off
chcp 65001
color 05
title Python Tools - Main Menu

cls

echo.          ███████╗███╗   ███╗ █████╗ ██████╗ ████████╗     ██████╗ ██████╗  █████╗ ██████╗ ██████╗ ███████╗██████╗ 
echo.          ██╔════╝████╗ ████║██╔══██╗██╔══██╗╚══██╔══╝    ██╔════╝ ██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
echo.          ███████╗██╔████╔██║███████║██████╔╝   ██║       ██║  ███╗██████╔╝███████║██████╔╝██████╔╝█████╗  ██████╔╝
echo.          ╚════██║██║╚██╔╝██║██╔══██║██╔══██╗   ██║       ██║   ██║██╔══██╗██╔══██║██╔══██╗██╔══██╗██╔══╝  ██╔══██╗
echo.          ███████║██║ ╚═╝ ██║██║  ██║██║  ██║   ██║       ╚██████╔╝██║  ██║██║  ██║██████╔╝██████╔╝███████╗██║  ██║
echo.          ╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝        ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
                                                                                                         

echo.                                      1. Build File          github.com/altay702
echo.                                      2. Use Tools
echo.                                      3. Exit
echo.
echo.

set /p choice=Enter your choice (1/2/3): 
if "%choice%"=="" (
    echo Error: No choice entered. Exiting.
    pause
    exit
)

echo You chose: %choice%
pause

if "%choice%"=="1" (
    echo Running Build File...
    python main.py --build || (
        echo Error: Python script failed during "Build File" operation.
        pause
        exit
    )
) else if "%choice%"=="2" (
    echo Running Use Tools...
    python main.py --tools || (
        echo Error: Python script failed during "Use Tools" operation.
        pause
        exit
    )
) else if "%choice%"=="3" (
    echo Exiting the program. Goodbye!
    timeout /t 2 >nul
    exit
) else (
    echo Invalid choice. Please try again.
    pause
    cls
    goto :eof
)

pause
