"""
Configuración de base de datos PostgreSQL para Railway
Versión con mejor manejo de errores
"""
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash

# Obtener URL de base de datos
DATABASE_URL = os.environ.get('DATABASE_URL')

# Railway usa postgres:// pero psycopg2 necesita postgresql://
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

def get_db():
    """Crea y retorna conexión a PostgreSQL"""
    try:
        if not DATABASE_URL:
            raise Exception("❌ ERROR: DATABASE_URL no configurada. Configura la variable de entorno en Railway.")
        
        print(f"📊 Conectando a PostgreSQL...")
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        print("✓ Conexión exitosa a PostgreSQL")
        return conn
    except Exception as e:
        print(f"❌ ERROR al conectar a PostgreSQL: {e}")
        raise

def init_db():
    """Inicializa todas las tablas en PostgreSQL"""
    try:
        print("\n" + "="*50)
        print("  INICIALIZANDO BASE DE DATOS POSTGRESQL")
        print("="*50 + "\n")
        
        conn = get_db()
        cur = conn.cursor()
        
        # Tabla de usuarios
        print("📝 Creando tabla: usuarios")
        cur.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id SERIAL PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                nombre VARCHAR(200) NOT NULL,
                rol VARCHAR(50) DEFAULT 'admin',
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("✓ Tabla usuarios creada")
        
        # Tabla de productos
        print("📝 Creando tabla: productos")
        cur.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(200) NOT NULL,
                descripcion TEXT,
                cantidad INTEGER DEFAULT 0,
                costo_unitario DECIMAL(10,2) NOT NULL,
                precio_venta DECIMAL(10,2) NOT NULL,
                stock_minimo INTEGER DEFAULT 5,
                estado VARCHAR(50) DEFAULT 'disponible',
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                usuario_id INTEGER NOT NULL REFERENCES usuarios(id)
            )
        ''')
        print("✓ Tabla productos creada")
        
        # Tabla de ventas
        print("📝 Creando tabla: ventas")
        cur.execute('''
            CREATE TABLE IF NOT EXISTS ventas (
                id SERIAL PRIMARY KEY,
                producto_id INTEGER NOT NULL REFERENCES productos(id),
                cliente_nombre VARCHAR(200) NOT NULL,
                cliente_telefono VARCHAR(50),
                cantidad INTEGER NOT NULL,
                precio_unitario DECIMAL(10,2) NOT NULL,
                total_vendido DECIMAL(10,2) NOT NULL,
                costo_total DECIMAL(10,2) NOT NULL,
                ganancia DECIMAL(10,2) NOT NULL,
                diezmo DECIMAL(10,2) NOT NULL,
                tipo_venta VARCHAR(50) DEFAULT 'contado',
                estado_pago VARCHAR(50) DEFAULT 'completado',
                fecha_venta DATE NOT NULL,
                usuario_id INTEGER NOT NULL REFERENCES usuarios(id),
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("✓ Tabla ventas creada")
        
        # Tabla de pagos
        print("📝 Creando tabla: pagos")
        cur.execute('''
            CREATE TABLE IF NOT EXISTS pagos (
                id SERIAL PRIMARY KEY,
                venta_id INTEGER NOT NULL REFERENCES ventas(id),
                monto DECIMAL(10,2) NOT NULL,
                fecha_pago DATE NOT NULL,
                metodo_pago VARCHAR(100),
                notas TEXT,
                usuario_id INTEGER NOT NULL REFERENCES usuarios(id),
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("✓ Tabla pagos creada")
        
        # Tabla de diezmos
        print("📝 Creando tabla: diezmos_mensuales")
        cur.execute('''
            CREATE TABLE IF NOT EXISTS diezmos_mensuales (
                id SERIAL PRIMARY KEY,
                mes INTEGER NOT NULL,
                anio INTEGER NOT NULL,
                total_diezmo DECIMAL(10,2) NOT NULL,
                estado VARCHAR(50) DEFAULT 'Pendiente',
                fecha_entrega TIMESTAMP,
                usuario_id INTEGER NOT NULL REFERENCES usuarios(id),
                UNIQUE(mes, anio, usuario_id)
            )
        ''')
        print("✓ Tabla diezmos_mensuales creada")
        
        # Tabla de configuración
        print("📝 Creando tabla: configuracion")
        cur.execute('''
            CREATE TABLE IF NOT EXISTS configuracion (
                id SERIAL PRIMARY KEY,
                clave VARCHAR(100) UNIQUE NOT NULL,
                valor TEXT NOT NULL,
                usuario_id INTEGER NOT NULL REFERENCES usuarios(id),
                fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("✓ Tabla configuracion creada")
        
        # Tabla de gastos
        print("📝 Creando tabla: gastos")
        cur.execute('''
            CREATE TABLE IF NOT EXISTS gastos (
                id SERIAL PRIMARY KEY,
                fecha DATE NOT NULL,
                categoria VARCHAR(100) NOT NULL,
                descripcion TEXT,
                monto DECIMAL(10,2) NOT NULL,
                usuario_id INTEGER NOT NULL REFERENCES usuarios(id),
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("✓ Tabla gastos creada")
        
        # Índices para rendimiento
        print("📝 Creando índices...")
        cur.execute('CREATE INDEX IF NOT EXISTS idx_ventas_fecha ON ventas(fecha_venta)')
        cur.execute('CREATE INDEX IF NOT EXISTS idx_ventas_usuario ON ventas(usuario_id)')
        cur.execute('CREATE INDEX IF NOT EXISTS idx_gastos_fecha ON gastos(fecha)')
        cur.execute('CREATE INDEX IF NOT EXISTS idx_productos_usuario ON productos(usuario_id)')
        print("✓ Índices creados")
        
        # Crear usuario admin por defecto
        print("📝 Verificando usuario admin...")
        cur.execute('SELECT id FROM usuarios WHERE username = %s', ('admin',))
        if cur.fetchone() is None:
            print("📝 Creando usuario admin...")
            hashed_password = generate_password_hash('admin123')
            cur.execute(
                'INSERT INTO usuarios (username, password, nombre, rol) VALUES (%s, %s, %s, %s) RETURNING id',
                ('admin', hashed_password, 'Administrador', 'admin')
            )
            user_id = cur.fetchone()['id']
            print(f"✓ Usuario admin creado (ID: {user_id})")
            
            # Configuración por defecto
            print("📝 Creando configuración por defecto...")
            cur.execute('INSERT INTO configuracion (clave, valor, usuario_id) VALUES (%s, %s, %s)',
                       ('moneda_simbolo', 'RD$', user_id))
            cur.execute('INSERT INTO configuracion (clave, valor, usuario_id) VALUES (%s, %s, %s)',
                       ('moneda_codigo', 'DOP', user_id))
            print("✓ Configuración creada")
        else:
            print("✓ Usuario admin ya existe")
        
        conn.commit()
        cur.close()
        conn.close()
        
        print("\n" + "="*50)
        print("  ✅ BASE DE DATOS INICIALIZADA CORRECTAMENTE")
        print("="*50 + "\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR AL INICIALIZAR BASE DE DATOS:")
        print(f"   {str(e)}")
        print("\nVerifica:")
        print("  1. DATABASE_URL está configurada en Railway")
        print("  2. PostgreSQL está corriendo")
        print("  3. La URL es correcta\n")
        raise
