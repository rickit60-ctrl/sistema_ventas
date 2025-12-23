"""
Script de verificación de rutas - Sistema ERP Ventas
Ejecuta este script para verificar que todas las rutas estén correctamente registradas
"""

import sys
sys.path.insert(0, '.')

from app import app

print("=" * 60)
print("VERIFICACIÓN DE RUTAS - SISTEMA ERP VENTAS")
print("=" * 60)
print()

# Listar todas las rutas registradas
print("Rutas registradas en Flask:")
print("-" * 60)

routes = []
for rule in app.url_map.iter_rules():
    routes.append({
        'endpoint': rule.endpoint,
        'methods': ','.join(sorted(rule.methods - {'HEAD', 'OPTIONS'})),
        'path': rule.rule
    })

# Ordenar por endpoint
routes.sort(key=lambda x: x['endpoint'])

# Imprimir en formato tabla
for route in routes:
    print(f"{route['endpoint']:25} {route['methods']:15} {route['path']}")

print()
print("-" * 60)
print(f"Total de rutas: {len(routes)}")
print()

# Verificar rutas específicas importantes
print("=" * 60)
print("VERIFICACIÓN DE MÓDULOS:")
print("=" * 60)
print()

modules = {
    'Dashboard': 'dashboard',
    'Inventario': 'inventario',
    'Ventas': 'ventas',
    'Cuentas por Cobrar': 'cuentas_por_cobrar',
    'Diezmos': 'diezmos',
    'Gastos': 'gastos',
    'Reportes': 'reportes',
    'Configuración': 'configuracion'
}

for module_name, endpoint in modules.items():
    exists = any(r['endpoint'] == endpoint for r in routes)
    status = "✓ OK" if exists else "✗ FALTA"
    print(f"{module_name:20} → {endpoint:20} {status}")

print()
print("=" * 60)

# Verificar rutas de gastos específicamente
print("RUTAS DEL MÓDULO DE GASTOS:")
print("-" * 60)

gastos_routes = [r for r in routes if 'gasto' in r['endpoint'].lower()]
if gastos_routes:
    for route in gastos_routes:
        print(f"✓ {route['endpoint']:25} → {route['path']}")
    print(f"\nTotal: {len(gastos_routes)} rutas de gastos encontradas")
else:
    print("✗ NO SE ENCONTRARON RUTAS DE GASTOS")
    print("\nPosibles causas:")
    print("1. El archivo app.py no se guardó correctamente")
    print("2. Hay un error de sintaxis que impide registrar las rutas")
    print("3. Las rutas se agregaron en un lugar incorrecto del archivo")

print()
print("=" * 60)
print("FIN DE VERIFICACIÓN")
print("=" * 60)
