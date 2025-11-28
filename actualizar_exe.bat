@echo off
title Generador MathPro (Modo VELOCIDAD - OneDir)

cd /d "%~dp0"

echo ==========================================
echo   DIAGNOSTICO
echo ==========================================
if exist ".venv\Scripts\python.exe" (
    set "PYTHON_CMD=.venv\Scripts\python.exe"
) else (
    set "PYTHON_CMD=python"
)

echo.
echo ==========================================
echo   PASO 1: LIMPIEZA
echo ==========================================
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist *.spec del /q *.spec
echo - Limpieza lista.

echo.
echo ==========================================
echo   PASO 2: CREANDO PROGRAMA (MODO CARPETA)
echo ==========================================
echo Generando... (Esto es mas rapido que antes)

:: CAMBIO CLAVE: Usamos --onedir en vez de --onefile
:: Esto crea una carpeta con todo descomprimido = Inicio Instantaneo

"%PYTHON_CMD%" -m PyInstaller ^
 --noconsole ^
 --onedir ^
 --clean ^
 --icon="icono.ico" ^
 --name="MathPro" ^
 --collect-all customtkinter ^
 --collect-all matplotlib ^
 main.py

if %errorlevel% neq 0 (
    color 4C
    echo [ERROR] FALLO PYINSTALLER.
    pause
    exit /b
)

echo.
echo ==========================================
echo   PASO 3: CREANDO ACCESO DIRECTO
echo ==========================================

:: Ahora el EXE esta dentro de una carpeta
set "RUTA_EXE=%CD%\dist\MathPro\MathPro.exe"
set "RUTA_DIR=%CD%\dist\MathPro"
set "RUTA_LNK=%USERPROFILE%\Desktop\MathPro.lnk"

:: Creamos el acceso directo en el escritorio apuntando a la carpeta dist
powershell -Command "$s=(New-Object -COM WScript.Shell).CreateShortcut('%RUTA_LNK%'); $s.TargetPath='%RUTA_EXE%'; $s.WorkingDirectory='%RUTA_DIR%'; $s.IconLocation='%RUTA_EXE%,0'; $s.Save()"

echo.
echo ==========================================
echo   LISTO MAE!
echo ==========================================
echo Prueba el icono en tu Escritorio.
echo Deberia abrir DE UNA VEZ (sin esperar).
echo.
echo NOTA: No muevas la carpeta 'dist' o se rompe el link.
pause