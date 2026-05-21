import os
import csv
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configuracion_base.settings')
django.setup()

from inventario.models import Categoria, Producto
from compras.models import Proveedor, OrdenCompra
from ventas.models import Cliente, Factura, DetalleFactura

OUTPUT_DIR = 'exports'
os.makedirs(OUTPUT_DIR, exist_ok=True)

def export_csv(filename, headers, rows):
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    print(f"  OK {filename} ({len(rows)} registros)")

# 1. Categorías
export_csv('categorias.csv',
    ['id', 'nombre', 'descripcion'],
    [(c.id, c.nombre, c.descripcion) for c in Categoria.objects.all()]
)

# 2. Productos
export_csv('productos.csv',
    ['id', 'sku', 'nombre', 'categoria', 'precio_compra', 'precio_venta', 'stock'],
    [(p.id, p.sku, p.nombre, p.categoria.nombre, p.precio_compra, p.precio_venta, p.stock)
     for p in Producto.objects.select_related('categoria')]
)

# 3. Proveedores
export_csv('proveedores.csv',
    ['id', 'nombre', 'contacto', 'telefono'],
    [(p.id, p.nombre, p.contacto, p.telefono) for p in Proveedor.objects.all()]
)

# 4. Órdenes de Compra
export_csv('ordenes_compra.csv',
    ['id', 'proveedor', 'producto', 'cantidad', 'costo_total', 'fecha_compra'],
    [(o.id, o.proveedor.nombre, o.producto.nombre, o.cantidad, o.costo_total,
      o.fecha_compra.strftime('%Y-%m-%d %H:%M:%S'))
     for o in OrdenCompra.objects.select_related('proveedor', 'producto')]
)

# 5. Clientes
export_csv('clientes.csv',
    ['id', 'nombre', 'nit', 'correo', 'telefono'],
    [(c.id, c.nombre, c.nit, c.correo, c.telefono) for c in Cliente.objects.all()]
)

# 6. Facturas
export_csv('facturas.csv',
    ['id', 'numero_factura', 'cliente', 'fecha_venta', 'total'],
    [(f.id, f.numero_factura, f.cliente.nombre,
      f.fecha_venta.strftime('%Y-%m-%d %H:%M:%S'), f.total)
     for f in Factura.objects.select_related('cliente').order_by('fecha_venta')]
)

# 7. Detalle de Facturas
export_csv('detalle_facturas.csv',
    ['id', 'numero_factura', 'producto', 'cantidad', 'precio_unitario', 'subtotal'],
    [(d.id, d.factura.numero_factura, d.producto.nombre, d.cantidad,
      d.precio_unitario, d.cantidad * d.precio_unitario)
     for d in DetalleFactura.objects.select_related('factura', 'producto')]
)

print(f"\n¡Exportación completa! Archivos guardados en la carpeta '{OUTPUT_DIR}/'")
print("Puedes abrir esta carpeta y compartir los CSV directamente con Power BI.")
