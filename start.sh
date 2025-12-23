#!/bin/bash

echo "Inicializando base de datos..."
python -c "from app import init_db; init_db()"

echo "Iniciando servidor con Gunicorn..."
gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
