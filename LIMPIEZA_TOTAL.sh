#!/bin/bash

clear
echo "============================================"
echo "  LIMPIEZA TOTAL Y REINICIO"
echo "============================================"
echo ""
echo "Este script va a:"
echo "1. Detener TODOS los procesos de Python/Flask"
echo "2. Eliminar TODO el cache"
echo "3. Eliminar archivos compilados viejos"
echo "4. Iniciar servidor completamente limpio"
echo ""
read -p "Presiona Enter para continuar..."
echo ""

echo "[PASO 1/4] Deteniendo procesos Python..."
pkill -9 -f "python.*app.py" 2>/dev/null || true
pkill -9 python 2>/dev/null || true
sleep 3
echo "OK - Procesos detenidos"

echo ""
echo "[PASO 2/4] Eliminando cache de Python..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type f -name "*.pyo" -delete 2>/dev/null || true
echo "OK - Cache eliminado"

echo ""
echo "[PASO 3/4] Eliminando archivo problemático..."
if [ -f "utils/excel_exporter.py" ]; then
    rm -f "utils/excel_exporter.py"
    echo "OK - Archivo problemático eliminado"
else
    echo "OK - Archivo ya no existe"
fi

echo ""
echo "[PASO 4/4] Verificando dependencias..."
if command -v python3 &> /dev/null; then
    PYTHON=python3
    PIP=pip3
else
    PYTHON=python
    PIP=pip
fi

$PYTHON -c "import flask, openpyxl" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Instalando dependencias faltantes..."
    $PIP install flask werkzeug openpyxl
fi
echo "OK - Dependencias listas"

echo ""
echo "============================================"
echo "  INICIANDO SERVIDOR LIMPIO"
echo "============================================"
echo ""
echo "URL: http://localhost:5000"
echo "Usuario: admin"
echo "Contraseña: admin123"
echo ""
echo "Presiona Ctrl+C para detener"
echo "============================================"
echo ""

$PYTHON app.py
