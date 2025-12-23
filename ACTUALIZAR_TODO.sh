#!/bin/bash

echo "====================================================="
echo "  ACTUALIZACIÓN COMPLETA - CORRIGE TODOS LOS ERRORES"
echo "====================================================="
echo ""

echo "Este script va a:"
echo "1. Hacer backup de tu base de datos"
echo "2. Limpiar TODO el caché"
echo "3. Reiniciar el servidor limpio"
echo ""
read -p "Presiona Enter para continuar..."

# Detectar Python
if command -v python3 &> /dev/null; then
    PYTHON=python3
    PIP=pip3
else
    PYTHON=python
    PIP=pip
fi

# Backup de base de datos
echo ""
echo "[1/4] Haciendo backup de la base de datos..."
if [ -f "sistema_ventas.db" ]; then
    cp sistema_ventas.db "sistema_ventas_backup_$(date +%Y%m%d_%H%M%S).db"
    echo "✓ Backup creado"
else
    echo "  No hay base de datos (sistema nuevo)"
fi

# Detener procesos Python
echo ""
echo "[2/4] Deteniendo procesos Flask anteriores..."
pkill -f "python.*app.py" 2>/dev/null || true
sleep 2
echo "✓ Procesos detenidos"

# Limpiar caché
echo ""
echo "[3/4] Limpiando caché..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type f -name "*.pyo" -delete 2>/dev/null || true
echo "✓ Caché eliminado"

# Verificar dependencias
echo ""
echo "[4/4] Verificando dependencias..."
$PYTHON -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Instalando dependencias necesarias..."
    $PIP install flask==3.0.0 werkzeug==3.0.1 openpyxl==3.1.2
fi
echo "✓ Dependencias OK"

echo ""
echo "====================================================="
echo "  INICIANDO SERVIDOR CORREGIDO"
echo "====================================================="
echo ""
echo "Sistema completamente actualizado"
echo "Servidor iniciando en: http://localhost:5000"
echo ""
echo "Usuario: admin"
echo "Contraseña: admin123"
echo ""
echo "Presiona Ctrl+C para detener"
echo "====================================================="
echo ""

$PYTHON app.py
