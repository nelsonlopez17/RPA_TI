from django.core.management.base import BaseCommand
import random
from decimal import Decimal
from ventas.models import Factura, DetalleFactura
from inventario.models import Producto

class Command(BaseCommand):
    help = 'Add product details to invoices that lack them without modifying stock (simulating replenishment)'

    def handle(self, *args, **options):
        total = Factura.objects.count()
        sin_detalle = Factura.objects.filter(detalles__isnull=True).count()
        self.stdout.write(self.style.SUCCESS(f'Total facturas: {total}'))
        self.stdout.write(f'Sin productos: {sin_detalle}')
        self.stdout.write(f'Con productos: {total - sin_detalle}')

        if sin_detalle == 0:
            self.stdout.write(self.style.SUCCESS('Todas las facturas ya tienen productos. No se requiere acción.'))
            return

        productos = list(Producto.objects.all())
        if not productos:
            self.stderr.write('Error: No hay productos en la base de datos.')
            return

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
                    precio_unitario=producto.precio_venta,
                )
                total_factura += subtotal

            Factura.objects.filter(id=factura.id).update(total=total_factura)
            procesadas += 1

        self.stdout.write(self.style.SUCCESS(f'Listo! {procesadas} facturas actualizadas con productos y totales calculados.'))
        self.stdout.write('El stock de los productos NO fue modificado.')
