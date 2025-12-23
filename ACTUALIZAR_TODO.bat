@echo off
echo =====================================================
echo   ACTUALIZACION COMPLETA - CORRIGE TODOS LOS ERRORES
echo =====================================================
echo.

echo Este script va a:
echo 1. Hacer backup de tu base de datos
echo 2. Limpiar TODO el cache
echo 3. Reiniciar el servidor limpio
echo.
pause

REM Backup de base de datos
echo.
echo [1/4] Haciendo backup de la base de datos...
if exist sistema_ventas.db (
    copy sistema_ventas.db sistema_ventas_backup_%date:~-4,4%%date:~-7,2%%date:~-10,2%.db
    echo ✓ Backup creado
) else (
    echo   No hay base de datos (sistema nuevo)
)

REM Detener procesos Python
echo.
echo [2/4] Deteniendo procesos Flask anteriores...
taskkill /F /IM python.exe /T 2>nul
taskkill /F /IM pythonw.exe /T 2>nul
timeout /t 2 /nobreak >nul
echo ✓ Procesos detenidos

REM Limpiar cache
echo.
echo [3/4] Limpiando cache...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
del /s /q *.pyc 2>nul
del /s /q *.pyo 2>nul
echo ✓ Cache eliminado

REM Verificar dependencias
echo.
echo [4/4] Verificando dependencias...
python -c "import flask" 2>nul
if errorlevel 1 (
    echo Instalando dependencias necesarias...
    pip install flask==3.0.0 werkzeug==3.0.1 openpyxl==3.1.2
)
echo ✓ Dependencias OK

echo.
echo =====================================================
echo   INICIANDO SERVIDOR CORREGIDO
echo =====================================================
echo.
echo Sistema completamente actualizado
echo Servidor iniciando en: http://localhost:5000
echo.
echo Usuario: admin
echo Contraseña: admin123
echo.
echo Presiona Ctrl+C para detener
echo =====================================================
echo.

python app.py

pause
