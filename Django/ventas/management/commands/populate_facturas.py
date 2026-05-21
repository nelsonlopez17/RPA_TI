from django.core.management.base import BaseCommand
import random
from decimal import Decimal
from ventas.models import Factura, DetalleFactura
from inventario.models import Producto

class Command(BaseCommand):
    help = ('Repopulate product details for ALL invoices, deleting any existing '
            "DetalleFactura rows and recalculating totals. Stock is left untouched.")

    def handle(self, *args, **options):
        total_facturas = Factura.objects.count()
        self.stdout.write(self.style.SUCCESS(f'Total facturas a procesar: {total_facturas}'))

        # Eliminar todos los detalles existentes
        deleted, _ = DetalleFactura.objects.all().delete()
        self.stdout.write(f'Detalles de factura eliminados: {deleted}')

        productos = list(Producto.objects.all())
        if not productos:
            self.stderr.write('Error: No hay productos en la base de datos.')
            return

        procesadas = 0
        for factura in Factura.objects.all():
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

        self.stdout.write(self.style.SUCCESS(
            f'Listo! {procesadas} facturas repobladas con detalle y totales calculados.'
        ))
        self.stdout.write('El stock de los productos NO fue modificado.')
