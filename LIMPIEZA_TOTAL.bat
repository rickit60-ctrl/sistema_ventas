@echo off
cls
echo ============================================
echo   LIMPIEZA TOTAL Y REINICIO
echo ============================================
echo.
echo Este script va a:
echo 1. Detener TODOS los procesos de Python
echo 2. Eliminar TODO el cache
echo 3. Eliminar archivos compilados viejos
echo 4. Iniciar servidor completamente limpio
echo.
pause
echo.

echo [PASO 1/4] Deteniendo procesos Python...
taskkill /F /IM python.exe /T 2>nul
taskkill /F /IM pythonw.exe /T 2>nul
timeout /t 3 /nobreak >nul
echo OK - Procesos detenidos

echo.
echo [PASO 2/4] Eliminando cache de Python...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
del /s /q *.pyc 2>nul
del /s /q *.pyo 2>nul
echo OK - Cache eliminado

echo.
echo [PASO 3/4] Eliminando archivo problemático...
if exist "utils\excel_exporter.py" (
    del /f "utils\excel_exporter.py" 2>nul
    echo OK - Archivo problemático eliminado
) else (
    echo OK - Archivo ya no existe
)

echo.
echo [PASO 4/4] Verificando dependencias...
python -c "import flask, openpyxl" 2>nul
if errorlevel 1 (
    echo Instalando dependencias faltantes...
    pip install flask werkzeug openpyxl
)
echo OK - Dependencias listas

echo.
echo ============================================
echo   INICIANDO SERVIDOR LIMPIO
echo ============================================
echo.
echo URL: http://localhost:5000
echo Usuario: admin
echo Contraseña: admin123
echo.
echo Presiona Ctrl+C para detener
echo ============================================
echo.

python app.py

pause
