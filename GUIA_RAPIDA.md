# 🚀 GUÍA RÁPIDA - Sistema de Gestión de Ventas

## ⚡ Inicio en 3 Pasos

### Windows:
```
1. Descomprimir sistema_ventas.zip
2. Doble click en iniciar.bat
3. Abrir http://localhost:5000
```

### Linux/Mac:
```bash
1. unzip sistema_ventas.zip
2. cd sistema_ventas
3. ./iniciar.sh
```

## 🔐 Login

```
Usuario: admin
Contraseña: admin123
```

## 📋 Primeros Pasos

### 1️⃣ Configurar Moneda
```
→ Menú "Configuración"
→ Establecer símbolo (RD$, US$, €)
→ Establecer código (DOP, USD, EUR)
→ Guardar
```

### 2️⃣ Agregar Productos
```
→ Menú "Inventario"
→ Click "+ Nuevo Producto"
→ Nombre: Ej. "Camisa Polo"
→ Cantidad inicial: 100
→ Costo unitario: 500
→ Precio venta: 800
→ Stock mínimo: 5
→ Guardar
```

### 3️⃣ Registrar Venta
```
→ Menú "Ventas"
→ Click "+ Nueva Venta"
→ Seleccionar producto
→ Cliente: Nombre del cliente
→ Cantidad: 2 (sistema verifica stock)
→ Tipo: Contado o Crédito
→ Registrar
```

**Sistema calcula automáticamente:**
- ✓ Total vendido
- ✓ Ganancia
- ✓ Diezmo (10%)
- ✓ Actualiza stock
- ✓ Actualiza diezmo mensual

### 4️⃣ Pagos (si venta a crédito)
```
→ Menú "Por Cobrar"
→ Click "Ver Pagos" en la venta
→ Registrar pago parcial o completo
→ Sistema actualiza automáticamente
```

### 5️⃣ Ver Diezmos
```
→ Menú "Diezmos"
→ Ver consolidado mensual
→ Marcar como "Entregado" cuando corresponda
```

### 6️⃣ Exportar Reportes
```
→ Menú "Reportes"
→ Seleccionar mes y año
→ Click "Descargar Reporte Excel"
```

## 🎯 Características Principales

### Inventario
- ✅ Control de stock en tiempo real
- ✅ Alertas de stock bajo/agotado
- ✅ Cálculo automático de margen
- ✅ Valor total del inventario

### Ventas
- ✅ Contado y crédito
- ✅ Descuento automático de stock
- ✅ Cálculo de ganancia
- ✅ Diezmo automático (10%)
- ✅ No permite venta sin stock

### Cuentas por Cobrar
- ✅ Pagos parciales
- ✅ Saldo pendiente automático
- ✅ Historial de pagos
- ✅ Estados: Pendiente/Parcial/Completado

### Diezmos
- ✅ 10% del total vendido (NO editable)
- ✅ Consolidado mensual automático
- ✅ Estados: Pendiente/Entregado
- ✅ Historial completo

### Dashboard
- ✅ Métricas del mes actual
- ✅ Gráfico de ventas
- ✅ Alertas de stock
- ✅ Productos críticos
- ✅ Ventas recientes

### Reportes
- ✅ Exportar a Excel por mes
- ✅ Todas las ventas
- ✅ Ganancia total
- ✅ Diezmo del mes
- ✅ Resumen por producto

## 💡 Consejos

### Stock
- El sistema NO permite ventas sin stock
- Las alertas se activan según el stock mínimo
- El stock se actualiza automáticamente al vender

### Diezmos
- Se calculan automáticamente (10% del total vendido)
- NO son editables
- Se consolidan por mes automáticamente

### Ventas a Crédito
- Se pueden registrar pagos parciales
- El sistema actualiza el estado automáticamente
- Ver saldo pendiente en tiempo real

### Reportes
- Solo para análisis (sistema opera 100% web)
- Generados con todos los datos del mes
- Formato profesional en Excel

## 🔧 Solución Rápida

### Error de puerto:
```python
# Editar app.py, última línea:
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Resetear sistema:
```bash
# Eliminar base de datos
rm sistema_ventas.db
# Reiniciar (se crea nueva)
python app.py
```

## 📱 Acceso

- **PC:** http://localhost:5000
- **Móvil (misma red):** http://IP-DE-TU-PC:5000

## 🎉 ¡Listo!

Ya puedes gestionar tu negocio completo:
- 📦 Inventario
- 💰 Ventas
- 🧾 Cuentas por cobrar
- 🙏 Diezmos
- 📊 Reportes

Para más detalles, consulta el README.md completo.
