#!/bin/bash

echo "============================================"
echo "  LIMPIANDO CACHÉ Y REINICIANDO SISTEMA"
echo "============================================"
echo ""

# Detener cualquier proceso de Python que esté ejecutando Flask
echo "1. Deteniendo procesos Flask anteriores..."
pkill -f "python.*app.py" 2>/dev/null || true
sleep 2

# Eliminar archivos de caché
echo "2. Eliminando archivos de caché..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type f -name "*.pyo" -delete 2>/dev/null || true

# Eliminar base de datos para empezar limpio (OPCIONAL - comentar si quieres mantener datos)
# rm -f sistema_ventas.db

echo "3. Caché eliminada exitosamente"
echo ""
echo "============================================"
echo "  INICIANDO SERVIDOR LIMPIO..."
echo "============================================"
echo ""

# Ejecutar Python
if command -v python3 &> /dev/null
then
    python3 app.py
else
    python app.py
fi
