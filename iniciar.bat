@echo off
echo ========================================
echo   Sistema de Gestion de Ventas
echo ========================================
echo.
echo Instalando dependencias...
pip install -r requirements.txt
echo.
echo Iniciando servidor...
echo.
echo La plataforma estara disponible en: http://localhost:5000
echo Usuario: admin
echo Contrasena: admin123
echo.
echo Presiona Ctrl+C para detener el servidor
echo.
python app.py
pause
