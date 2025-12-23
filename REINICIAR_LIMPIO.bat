@echo off
echo ============================================
echo   LIMPIANDO CACHE Y REINICIANDO SISTEMA
echo ============================================
echo.

REM Detener procesos Python anteriores
echo 1. Deteniendo procesos Flask anteriores...
taskkill /F /IM python.exe /T 2>nul
taskkill /F /IM pythonw.exe /T 2>nul
timeout /t 2 /nobreak >nul

REM Eliminar archivos de cache
echo 2. Eliminando archivos de cache...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
del /s /q *.pyc 2>nul
del /s /q *.pyo 2>nul

echo 3. Cache eliminada exitosamente
echo.

REM Eliminar base de datos para empezar limpio (OPCIONAL - comentar si quieres mantener datos)
REM del /f sistema_ventas.db 2>nul

echo ============================================
echo   INICIANDO SERVIDOR LIMPIO...
echo ============================================
echo.
echo El servidor se iniciara en: http://localhost:5000
echo Usuario: admin
echo Contraseña: admin123
echo.
echo Presiona Ctrl+C para detener el servidor
echo ============================================
echo.

python app.py

pause
