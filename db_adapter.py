"""
Adaptador de Base de Datos
Soporta SQLite (desarrollo) y PostgreSQL (producción)
"""
import os

# Detectar cuál base de datos usar
DATABASE_URL = os.environ.get('DATABASE_URL')
USE_POSTGRES = DATABASE_URL is not None

if USE_POSTGRES:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    DB_TYPE = 'postgresql'
else:
    import sqlite3
    DB_TYPE = 'sqlite'

def get_db_connection():
    """Retorna conexión a la base de datos apropiada"""
    if USE_POSTGRES:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    else:
        conn = sqlite3.connect('sistema_ventas.db')
        conn.row_factory = sqlite3.Row
        return conn

def get_cursor(conn):
    """Retorna cursor apropiado según el tipo de BD"""
    if USE_POSTGRES:
        return conn.cursor(cursor_factory=RealDictCursor)
    else:
        return conn.cursor()

def get_placeholder():
    """Retorna el placeholder apropiado (? para SQLite, %s para PostgreSQL)"""
    return '%s' if USE_POSTGRES else '?'

def adapt_query(query):
    """Adapta una query de SQLite a PostgreSQL si es necesario"""
    if not USE_POSTGRES:
        return query
    
    # Convertir tipos de datos
    query = query.replace('INTEGER PRIMARY KEY AUTOINCREMENT', 'SERIAL PRIMARY KEY')
    query = query.replace('REAL', 'DECIMAL(10,2)')
    query = query.replace('TIMESTAMP DEFAULT CURRENT_TIMESTAMP', 'TIMESTAMP DEFAULT NOW()')
    
    # Convertir placeholders
    query = query.replace('?', '%s')
    
    # Convertir funciones de fecha
    query = query.replace("strftime('%m',", "EXTRACT(MONTH FROM")
    query = query.replace("strftime('%Y',", "EXTRACT(YEAR FROM")
    query = query.replace("strftime('%d',", "EXTRACT(DAY FROM")
    
    # Cerrar paréntesis de EXTRACT
    if 'EXTRACT(' in query:
        # Contar paréntesis y ajustar
        pass  # Por simplicidad, asumimos que las queries ya están bien formadas
    
    return query

def init_database(app):
    """Inicializa la base de datos"""
    with app.app_context():
        conn = get_db_connection()
        cur = get_cursor(conn)
        
        # Tabla de usuarios
        query = adapt_query('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                nombre TEXT NOT NULL,
                rol TEXT DEFAULT 'admin',
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cur.execute(query)
        
        # Tabla de productos
        query = adapt_query('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                cantidad INTEGER DEFAULT 0,
                costo_unitario REAL NOT NULL,
                precio_venta REAL NOT NULL,
                stock_minimo INTEGER DEFAULT 5,
                estado TEXT DEFAULT 'disponible',
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                usuario_id INTEGER NOT NULL,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            )
        ''')
        cur.execute(query)
        
        # Tabla de ventas
        query = adapt_query('''
            CREATE TABLE IF NOT EXISTS ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                producto_id INTEGER NOT NULL,
                cliente_nombre TEXT NOT NULL,
                cliente_telefono TEXT,
                cantidad INTEGER NOT NULL,
                precio_unitario REAL NOT NULL,
                total_vendido REAL NOT NULL,
                costo_total REAL NOT NULL,
                ganancia REAL NOT NULL,
                diezmo REAL NOT NULL,
                tipo_venta TEXT DEFAULT 'contado',
                estado_pago TEXT DEFAULT 'completado',
                fecha_venta DATE NOT NULL,
                usuario_id INTEGER NOT NULL,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (producto_id) REFERENCES productos (id),
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            )
        ''')
        cur.execute(query)
        
        # Tabla de pagos
        query = adapt_query('''
            CREATE TABLE IF NOT EXISTS pagos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                venta_id INTEGER NOT NULL,
                monto REAL NOT NULL,
                fecha_pago DATE NOT NULL,
                metodo_pago TEXT,
                notas TEXT,
                usuario_id INTEGER NOT NULL,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (venta_id) REFERENCES ventas (id),
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            )
        ''')
        cur.execute(query)
        
        # Tabla de diezmos mensuales
        query = adapt_query('''
            CREATE TABLE IF NOT EXISTS diezmos_mensuales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mes INTEGER NOT NULL,
                anio INTEGER NOT NULL,
                total_diezmo REAL NOT NULL,
                estado TEXT DEFAULT 'Pendiente',
                fecha_entrega TIMESTAMP,
                usuario_id INTEGER NOT NULL,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
                UNIQUE(mes, anio, usuario_id)
            )
        ''')
        cur.execute(query)
        
        # Tabla de configuración
        query = adapt_query('''
            CREATE TABLE IF NOT EXISTS configuracion (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                clave TEXT UNIQUE NOT NULL,
                valor TEXT NOT NULL,
                usuario_id INTEGER NOT NULL,
                fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            )
        ''')
        cur.execute(query)
        
        # Tabla de gastos
        query = adapt_query('''
            CREATE TABLE IF NOT EXISTS gastos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha DATE NOT NULL,
                categoria TEXT NOT NULL,
                descripcion TEXT,
                monto REAL NOT NULL,
                usuario_id INTEGER NOT NULL,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            )
        ''')
        cur.execute(query)
        
        # Crear usuario admin por defecto
        ph = get_placeholder()
        cur.execute(f'SELECT id FROM usuarios WHERE username = {ph}', ('admin',))
        if cur.fetchone() is None:
            from werkzeug.security import generate_password_hash
            hashed_password = generate_password_hash('admin123')
            cur.execute(
                f'INSERT INTO usuarios (username, password, nombre, rol) VALUES ({ph}, {ph}, {ph}, {ph})',
                ('admin', hashed_password, 'Administrador', 'admin')
            )
            cur.execute(f'SELECT id FROM usuarios WHERE username = {ph}', ('admin',))
            user_id = cur.fetchone()[0] if USE_POSTGRES else cur.fetchone()['id']
            
            # Configuración por defecto
            cur.execute(f'INSERT INTO configuracion (clave, valor, usuario_id) VALUES ({ph}, {ph}, {ph})',
                       ('moneda_simbolo', 'RD$', user_id))
            cur.execute(f'INSERT INTO configuracion (clave, valor, usuario_id) VALUES ({ph}, {ph}, {ph})',
                       ('moneda_codigo', 'DOP', user_id))
        
        conn.commit()
        cur.close()
        conn.close()
        print(f"✓ Base de datos {DB_TYPE.upper()} inicializada correctamente")
