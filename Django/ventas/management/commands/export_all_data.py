import os
import csv
from pathlib import Path
from django.core.management.base import BaseCommand
from decimal import Decimal

# Importar modelos de todas las apps relevantes
from ventas.models import Cliente, Factura, DetalleFactura
from inventario.models import Producto, Categoria
from compras.models import Proveedor

class Command(BaseCommand):
    help = 'Exporta toda la data del ERP a archivos CSV (para Power BI)'

    def handle(self, *args, **options):
        # Directorio donde se guardarán los CSV
        export_dir = Path('exports')
        export_dir.mkdir(exist_ok=True)

        # Función sencilla para escribir CSV
        def export_qs(qs, filename, headers, row_func):
            file_path = export_dir / filename
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                for obj in qs:
                    writer.writerow(row_func(obj))
            self.stdout.write(self.style.SUCCESS(f'OK {filename} exportado ({qs.count()} registros)'))

        # 1️⃣ Clientes
        export_qs(
            Cliente.objects.all(),
            'clientes.csv',
            ['id', 'nombre', 'nit', 'correo', 'telefono'],
            lambda c: [c.id, c.nombre, c.nit, c.correo, c.telefono]
        )

        # 2️⃣ Proveedores
        export_qs(
            Proveedor.objects.all(),
            'proveedores.csv',
            ['id', 'nombre', 'contacto', 'telefono'],
            lambda p: [p.id, p.nombre, p.contacto, p.telefono]
        )

        # 3️⃣ Categorías
        export_qs(
            Categoria.objects.all(),
            'categorias.csv',
            ['id', 'nombre', 'descripcion'],
            lambda cat: [cat.id, cat.nombre, cat.descripcion]
        )

        # 4️⃣ Productos
        export_qs(
            Producto.objects.select_related('categoria').all(),
            'productos.csv',
            ['id', 'sku', 'nombre', 'descripcion', 'precio_compra', 'precio_venta', 'stock', 'categoria_id', 'categoria_nombre'],
            lambda prod: [
                prod.id,
                prod.sku,
                prod.nombre,
                prod.descripcion,
                prod.precio_compra,
                prod.precio_venta,
                prod.stock,
                prod.categoria.id if prod.categoria else None,
                prod.categoria.nombre if prod.categoria else ''
            ]
        )

        # 5️⃣ Facturas (cabecera)
        export_qs(
            Factura.objects.select_related('cliente').all(),
            'facturas.csv',
            ['id', 'numero_factura', 'fecha_venta', 'cliente_id', 'cliente_nombre', 'total'],
            lambda f: [
                f.id,
                f.numero_factura,
                f.fecha_venta.strftime('%Y-%m-%d %H:%M:%S') if f.fecha_venta else '',
                f.cliente.id if f.cliente else None,
                f.cliente.nombre if f.cliente else '',
                f.total
            ]
        )

        # 6️⃣ Detalle de Facturas
        export_qs(
            DetalleFactura.objects.select_related('factura', 'producto').all(),
            'detalle_facturas.csv',
            [
                'id', 'factura_id', 'producto_id', 'producto_nombre',
                'cantidad', 'precio_unitario', 'subtotal'
            ],
            lambda d: [
                d.id,
                d.factura.id,
                d.producto.id,
                d.producto.nombre,
                d.cantidad,
                d.precio_unitario,
                d.cantidad * d.precio_unitario
            ]
        )

        self.stdout.write(self.style.SUCCESS('Exportacion completada. Encuentra los CSV en la carpeta "exports/"'))
