#!/usr/bin/env python3
"""
Convertidor robusto de SQLite a PostgreSQL para Flask
"""
import re
import sys

def convert_sqlite_to_postgres(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Imports
    content = content.replace(
        'import sqlite3',
        'import psycopg2\nfrom psycopg2.extras import RealDictCursor'
    )
    
    # 2. DATABASE variable
    content = re.sub(
        r"DATABASE = .*",
        "DATABASE_URL = os.environ.get('DATABASE_URL')",
        content
    )
    
    # 3. get_db function - reemplazar completamente
    get_db_old = re.search(r'def get_db\(\):.*?return conn', content, re.DOTALL)
    if get_db_old:
        get_db_new = '''def get_db():
    """Obtiene conexión a PostgreSQL"""
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        # Producción (Railway provee DATABASE_URL)
        conn = psycopg2.connect(database_url)
    else:
        # Desarrollo local
        conn = psycopg2.connect(
            host=os.environ.get('DB_HOST', 'localhost'),
            database=os.environ.get('DB_NAME', 'sistema_ventas'),
            user=os.environ.get('DB_USER', 'postgres'),
            password=os.environ.get('DB_PASSWORD', 'postgres'),
            port=os.environ.get('DB_PORT', '5432')
        )
    return conn'''
        content = content[:get_db_old.start()] + get_db_new + content[get_db_old.end():]
    
    # 4. SQL Data Types
    content = content.replace('INTEGER PRIMARY KEY AUTOINCREMENT', 'SERIAL PRIMARY KEY')
    content = content.replace('REAL NOT NULL', 'DECIMAL(10,2) NOT NULL')
    content = content.replace('REAL DEFAULT', 'DECIMAL(10,2) DEFAULT')
    content = content.replace('TIMESTAMP DEFAULT CURRENT_TIMESTAMP', 'TIMESTAMP DEFAULT NOW()')
    content = content.replace('VARCHAR', 'VARCHAR')  # No change needed
    
    # 5. Query placeholders ? to %s
    # Cuidadoso con esto - solo en contextos SQL
    content = re.sub(r'(\s+)(\(.*?\?.*?\))', lambda m: m.group(1) + m.group(2).replace('?', '%s'), content)
    content = re.sub(r"execute\(('''|\"\"\")(.*?)('''|\"\"\")", 
                     lambda m: f"execute({m.group(1)}{m.group(2).replace('?', '%s')}{m.group(3)}", 
                     content, flags=re.DOTALL)
    
    # 6. cursor() calls - add RealDictCursor
    content = re.sub(
        r'(\w+)\.cursor\(\)',
        r'\1.cursor(cursor_factory=RealDictCursor)',
        content
    )
    
    # 7. strftime to EXTRACT  
    # Pattern: strftime('%m', field) -> EXTRACT(MONTH FROM field)
    content = re.sub(r"strftime\('%m',\s*([a-z_\.]+)\)", r'EXTRACT(MONTH FROM \1)', content)
    content = re.sub(r"strftime\('%Y',\s*([a-z_\.]+)\)", r'EXTRACT(YEAR FROM \1)', content)
    content = re.sub(r"strftime\('%d',\s*([a-z_\.]+)\)", r'EXTRACT(DAY FROM \1)', content)
    
    # 8. CAST for PostgreSQL
    content = re.sub(r'CAST\(strftime\(.*?\) AS INTEGER\)', 
                     lambda m: m.group(0).replace('CAST(strftime', 'CAST(EXTRACT').replace(') AS INTEGER)', ')::INTEGER'),
                     content)
    
    # 9. fetchone() con índices - PostgreSQL con RealDictCursor devuelve dicts
    # No cambiar - ya funcionará con RealDictCursor
    
    # 10. Conversión de valores decimales al retornar
    # Agregar float() donde sea necesario
    content = re.sub(
        r"(\w+)\['(\w+)'\](\s*\))",
        lambda m: f"float({m.group(1)}['{m.group(2)}']){m.group(3)}" if any(x in m.group(2) for x in ['total', 'monto', 'precio', 'costo', 'ganancia', 'diezmo', 'valor']) else m.group(0),
        content
    )
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ Conversión completada: {input_file} -> {output_file}")
    print("✓ Verificar manualmente las siguientes secciones:")
    print("  - init_db() - tipos de datos SQL")
    print("  - Queries con fechas - EXTRACT vs strftime")
    print("  - fetchone() / fetchall() con RealDictCursor")

if __name__ == '__main__':
    convert_sqlite_to_postgres('app_sqlite_backup.py', 'app.py')
