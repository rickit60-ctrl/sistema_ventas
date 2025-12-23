#!/bin/bash
echo "========================================"
echo "  Sistema de Gestión de Ventas"
echo "========================================"
echo ""
echo "Instalando dependencias..."
pip3 install -r requirements.txt
echo ""
echo "Iniciando servidor..."
echo ""
echo "La plataforma estará disponible en: http://localhost:5000"
echo "Usuario: admin"
echo "Contraseña: admin123"
echo ""
echo "Presiona Ctrl+C para detener el servidor"
echo ""
python3 app.py
