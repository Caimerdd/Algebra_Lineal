@echo off
title Generador MathPro (Optimizado en DIST)

:: 1. Ubicarse en la carpeta del proyecto
cd /d "%~dp0"

echo ==========================================
echo   DIAGNOSTICO
echo ==========================================
if exist ".venv\Scripts\python.exe" (
    set "PYTHON_CMD=.venv\Scripts\python.exe"
    echo [OK] Usando entorno virtual.
) else (
    set "PYTHON_CMD=python"
    echo [INFO] Usando Python global.
)

echo.
echo ==========================================
echo   PASO 1: LIMPIEZA
echo ==========================================
if exist build rmdir /s /q build
if exist *.spec del /q *.spec
:: Nota: No borramos 'dist' completo para no borrar otros exes viejos si tienes,
:: pero PyInstaller sobrescribirá MathPro.exe.
echo - Limpieza lista.

echo.
echo ==========================================
echo   PASO 2: GENERANDO EXE (OPTIMIZADO)
echo ==========================================
echo Creando archivo unico en la carpeta 'dist'...
echo Aplicando optimizacion --noupx para inicio mas rapido.

:: COMANDO OPTIMIZADO:
:: --onefile: Crea un solo archivo .exe (sin carpetas).
:: --noupx: NO comprime el ejecutable. (Hace que pese mas, pero abre mas rapido).
:: --windowed: Sin consola negra.

"%PYTHON_CMD%" -m PyInstaller ^
 --noconsole ^
 --onefile ^
 --clean ^
 --noupx ^
 --icon="icono.ico" ^
 --name="MathPro" ^
 --collect-all customtkinter ^
 --collect-all matplotlib ^
 main.py

if %errorlevel% neq 0 (
    color 4C
    echo [ERROR] Fallo la creacion.
    pause
    exit /b
)

:: Limpieza final de archivos temporales
if exist build rmdir /s /q build
if exist *.spec del /q *.spec

echo.
echo ==========================================
echo   LISTO MAE!
echo ==========================================
echo Tu archivo esta en la carpeta: dist/MathPro.exe
echo.
echo Pruebalo desde ahi. Deberia abrir mas rapido que antes.
pause