from django.core.management.base import BaseCommand
from django.db import transaction

from inventario.models import Categoria, Producto
from compras.models import Proveedor, OrdenCompra
from ventas.models import Cliente, Factura, DetalleFactura

class Command(BaseCommand):
    help = 'Elimina todos los datos de prueba generados (Categorías, Productos, Proveedores, Clientes, Facturas y Órdenes)'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Borrando todos los datos...'))

        with transaction.atomic():
            # El orden de borrado importa si hay restricciones (aunque CASCADE suele limpiar automáticamente)
            DetalleFactura.objects.all().delete()
            Factura.objects.all().delete()
            OrdenCompra.objects.all().delete()
            Producto.objects.all().delete()
            Cliente.objects.all().delete()
            
            # Borramos proveedores (excepto el predeterminado si es necesario, o todos)
            Proveedor.objects.all().delete()
            Categoria.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('¡Base de datos limpiada con éxito!'))
