import os
import django
import random
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configuracion_base.settings')
django.setup()

from ventas.models import Factura, DetalleFactura
from inventario.models import Producto

# Diagnóstico
total = Factura.objects.count()
sin_detalle = Factura.objects.filter(detalles__isnull=True).count()
print(f"Total facturas: {total}")
print(f"Sin productos: {sin_detalle}")
print(f"Con productos: {total - sin_detalle}")

if sin_detalle == 0:
    print("\nTodas las facturas ya tienen productos. No se requiere acción.")
    exit()

print(f"\nAgregando productos a {sin_detalle} facturas (SIN modificar stock)...")

productos = list(Producto.objects.all())
if not productos:
    print("Error: No hay productos en la BD.")
    exit()

facturas_sin_detalle = Factura.objects.filter(detalles__isnull=True)
procesadas = 0

for factura in facturas_sin_detalle:
    num_productos = random.randint(1, 4)
    seleccionados = random.sample(productos, min(num_productos, len(productos)))
    total_factura = Decimal('0.00')

    for producto in seleccionados:
        cantidad = random.randint(1, 3)
        subtotal = producto.precio_venta * cantidad

        DetalleFactura.objects.create(
            factura=factura,
            producto=producto,
            cantidad=cantidad,
            precio_unitario=producto.precio_venta
        )
        total_factura += subtotal

    # Actualizar el total de la factura sin tocar el stock
    Factura.objects.filter(id=factura.id).update(total=total_factura)
    procesadas += 1

print(f"Listo! {procesadas} facturas actualizadas con productos y totales calculados.")
print("El stock de los productos NO fue modificado.")
