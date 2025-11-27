@echo off
title Generador MathPro (Modo Blindado)

:: --- LA LINEA DE ORO: Forzar que trabaje en la carpeta actual ---
cd /d "%~dp0"

echo ==========================================
echo   DIAGNOSTICO RAPIDO
echo ==========================================
echo Estoy trabajando en: %CD%

:: Verificar si existe el entorno virtual
if exist ".venv\Scripts\python.exe" (
    echo [OK] Entorno virtual detectado.
    set "PYTHON_CMD=.venv\Scripts\python.exe"
) else (
    echo [ALERTA] No encuentro '.venv'. Buscando Python global...
    set "PYTHON_CMD=python"
)

echo Usare este Python: %PYTHON_CMD%
echo.
echo Presiona ENTER para empezar la limpieza...
pause

echo ==========================================
echo   PASO 1: LIMPIEZA
echo ==========================================

if exist dist (
    rmdir /s /q dist
    echo - Carpeta 'dist' eliminada.
)
if exist build (
    rmdir /s /q build
    echo - Carpeta 'build' eliminada.
)
if exist *.spec (
    del /q *.spec
    echo - Archivo .spec eliminado.
)

echo.
echo ==========================================
echo   PASO 2: CREANDO EJECUTABLE
echo ==========================================
echo Generando... (Esto puede tardar 1 minuto)

:: EJECUCION DIRECTA
:: Usamos el python del venv para llamar a PyInstaller como modulo (-m)
:: Esto evita problemas de PATH

"%PYTHON_CMD%" -m PyInstaller --noconsole --onefile --icon="icono.ico" --name="MathPro" --collect-all customtkinter main.py

if %errorlevel% neq 0 (
    color 47
    echo.
    echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    echo [ERROR] ALGO FALLO EN PYINSTALLER.
    echo Revisa el mensaje rojo arriba.
    echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    pause
    exit /b
)

echo.
echo ==========================================
echo   PASO 3: ACCESO DIRECTO
echo ==========================================

set "RUTA_EXE=%CD%\dist\MathPro.exe"
set "RUTA_ICONO="C:\Users\luisg\OneDrive\Desktop\algebra lineal\Algebra_Lineal\icono.ico"\icono.ico"
set "RUTA_LNK=%USERPROFILE%\Desktop\MathPro.lnk"

echo Creando acceso directo en el Escritorio...

powershell -command "$s = (New-Object -ComObject WScript.Shell).CreateShortcut('C:\Users\luisg\OneDrive\Desktop\MathPro.lnk'); $s.TargetPath = 'C:\Users\luisg\OneDrive\Desktop\Algebra_Lineal\Algebra_Luis\dist\MathPro.exe'; $s.WorkingDirectory = 'C:\Users\luisg\OneDrive\Desktop\Algebra_Lineal\Algebra_Luis\dist'; $s.IconLocation = 'C:\Users\luisg\OneDrive\Desktop\Algebra_Lineal\Algebra_Luis\icono.ico'; $s.Save()"


echo.
echo ==========================================
echo   EXITO TOTAL MAE!
echo ==========================================
echo Tu programa esta listo en el escritorio.
pause