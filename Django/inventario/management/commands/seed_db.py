import random
import decimal
from datetime import timedelta
from django.utils import timezone
from django.core.management.base import BaseCommand
from django.db import transaction

try:
    from faker import Faker
except ImportError:
    Faker = None

from inventario.models import Categoria, Producto
from compras.models import Proveedor, OrdenCompra
from ventas.models import Cliente, Factura, DetalleFactura

class Command(BaseCommand):
    help = 'Puebla la base de datos con datos de venta de computadoras en Guatemala'

    def handle(self, *args, **kwargs):
        if not Faker:
            self.stdout.write(self.style.ERROR('La librería "faker" no está instalada. Por favor, ejecuta "pip install faker" primero.'))
            return

        # Usar la localización en español
        fake = Faker('es_ES')

        self.stdout.write(self.style.WARNING('Iniciando la generación de datos (puede tardar un par de minutos para 1000 facturas)...'))

        with transaction.atomic():
            # 1. Crear Categorías
            self.stdout.write('1. Creando Categorías...')
            categorias_data = [
                {'nombre': 'Laptops', 'descripcion': 'Equipos portátiles para hogar, oficina y gaming.'},
                {'nombre': 'Computadoras de Escritorio', 'descripcion': 'PC armadas y de marca para escritorio.'},
                {'nombre': 'Procesadores', 'descripcion': 'CPUs Intel y AMD.'},
                {'nombre': 'Tarjetas de Video (GPUs)', 'descripcion': 'Tarjetas gráficas NVIDIA y AMD.'},
                {'nombre': 'Memoria RAM', 'descripcion': 'Módulos de memoria DDR4 y DDR5.'},
                {'nombre': 'Almacenamiento', 'descripcion': 'Discos duros (HDD) y unidades de estado sólido (SSD).'},
                {'nombre': 'Tarjetas Madre', 'descripcion': 'Motherboards compatibles con Intel y AMD.'},
                {'nombre': 'Fuentes de Poder', 'descripcion': 'Fuentes de alimentación certificadas.'},
                {'nombre': 'Periféricos', 'descripcion': 'Teclados, ratones, auriculares y micrófonos.'},
                {'nombre': 'Monitores', 'descripcion': 'Pantallas de oficina y monitores gaming de alta tasa de refresco.'},
                {'nombre': 'Redes', 'descripcion': 'Routers, switches y adaptadores de red.'},
                {'nombre': 'Accesorios', 'descripcion': 'Cables, mochilas, hubs USB y refrigeración.'}
            ]
            
            dic_categorias = {}
            for data in categorias_data:
                cat, _ = Categoria.objects.get_or_create(
                    nombre=data['nombre'],
                    defaults={'descripcion': data['descripcion']}
                )
                dic_categorias[data['nombre']] = cat

            # 2. Crear Proveedores (20 proveedores relacionados a la tecnología)
            self.stdout.write('2. Creando 20 Proveedores...')
            nombres_proveedores = [
                'Intcomex Guatemala', 'Copia Mágica', 'Tecnología Global S.A.', 'Distribuidora Electrónica GT',
                'Importaciones PC', 'Gaming Store Mayoristas', 'MacroSistemas', 'Grupo Inteligo',
                'Suministros Tech', 'Componentes Centrales SA', 'CompuMayorista', 'Redes y Más GT',
                'Cables y Periféricos S.A.', 'TechBox Guatemala', 'Hardware Chapín', 'Innovación Digital SA',
                'KinalTech', 'MegaDistribuidora IT', 'Soluciones Informáticas de Guatemala', 'PC Parts GT'
            ]
            proveedores = []
            for nombre in nombres_proveedores:
                # Generar teléfono formato Guatemala: 2xxx-xxxx o 5xxx-xxxx
                prefijo_tel = random.choice(['2', '4', '5'])
                tel = f"{prefijo_tel}{fake.numerify('###-####')}"
                
                prov, _ = Proveedor.objects.get_or_create(
                    nombre=nombre,
                    defaults={
                        'contacto': fake.name(),
                        'telefono': tel,
                        'email': fake.ascii_company_email()
                    }
                )
                proveedores.append(prov)

            # 3. Crear 100 Productos
            self.stdout.write('3. Creando 100 Productos Consistentes...')
            
            base_productos = [
                ('Laptops', ['Laptop HP Pavilion', 'Laptop Dell Inspiron', 'Lenovo ThinkPad', 'ASUS ROG Strix', 'MacBook Air M2', 'Laptop Acer Nitro 5', 'MSI Katana GF66', 'Lenovo IdeaPad 3', 'Laptop HP Omen', 'MacBook Pro M3']),
                ('Computadoras de Escritorio', ['PC Gamer Armada Entry', 'PC Oficina Básica', 'Workstation Dell Precision', 'HP EliteDesk', 'PC Gamer High-End RTX 4070', 'PC Mini Intel NUC', 'Apple Mac Mini', 'iMac 24 pulgadas']),
                ('Procesadores', ['Intel Core i3-12100F', 'Intel Core i5-13400F', 'Intel Core i7-13700K', 'Intel Core i9-14900K', 'AMD Ryzen 3 3200G', 'AMD Ryzen 5 5600X', 'AMD Ryzen 7 5800X3D', 'AMD Ryzen 9 7950X']),
                ('Tarjetas de Video (GPUs)', ['ASUS RTX 3060 12GB', 'MSI RTX 4060 Ti', 'Gigabyte RTX 4070 12GB', 'Zotac RTX 4090 24GB', 'Sapphire RX 6600 8GB', 'ASRock RX 7800 XT', 'PowerColor RX 7900 XTX', 'NVIDIA GTX 1650 4GB']),
                ('Memoria RAM', ['RAM Corsair Vengeance 8GB DDR4', 'RAM Kingston Fury 16GB DDR4', 'RAM G.Skill Trident Z 32GB DDR5', 'RAM Crucial 16GB DDR5', 'RAM Adata XPG 8GB RGB', 'RAM Kingston Value 4GB', 'RAM Corsair Dominator 64GB']),
                ('Almacenamiento', ['SSD Kingston 240GB 2.5', 'SSD WD Blue 500GB M.2', 'SSD Samsung 980 Pro 1TB NVMe', 'SSD Crucial P3 2TB', 'Disco Duro HDD Seagate 1TB', 'Disco Duro HDD WD Black 2TB', 'Disco Duro Externo Adata 1TB']),
                ('Tarjetas Madre', ['Motherboard ASUS Prime H610M', 'Motherboard Gigabyte B660M', 'Motherboard MSI Z790 Tomahawk', 'Motherboard ASUS ROG X670E', 'Motherboard ASRock B550M Pro4', 'Motherboard Gigabyte A520M']),
                ('Fuentes de Poder', ['Fuente EVGA 500W 80+ White', 'Fuente Corsair CV650 80+ Bronze', 'Fuente XPG Core Reactor 750W 80+ Gold', 'Fuente ASUS ROG Thor 1000W Platinum', 'Fuente Thermaltake 600W RGB']),
                ('Periféricos', ['Mouse Logitech G203', 'Mouse Razer DeathAdder V2', 'Teclado Mecánico Redragon Kumara', 'Teclado HyperX Alloy Origins', 'Audífonos Corsair HS50', 'Audífonos Logitech G733', 'Micrófono HyperX QuadCast', 'Webcam Logitech C920']),
                ('Monitores', ['Monitor LG 24" IPS 75Hz', 'Monitor Samsung 27" Curvo', 'Monitor ASUS TUF 24" 165Hz', 'Monitor AOC 27" 144Hz', 'Monitor Dell UltraSharp 27" 4K', 'Monitor Gigabyte M27Q 170Hz']),
                ('Redes', ['Router TP-Link Archer C50', 'Router ASUS RT-AX58U WiFi 6', 'Switch TP-Link 5 Puertos Gigabit', 'Adaptador WiFi USB Nano', 'Tarjeta de Red PCIe TP-Link', 'Repetidor WiFi Xiaomi']),
                ('Accesorios', ['Cable HDMI 2.0 2m', 'Cable DisplayPort 1.4 2m', 'Mochila Targus para Laptop 15.6"', 'Hub USB-C Ugreen 7 en 1', 'Pasta Térmica Arctic MX-4', 'Ventilador Cooler Master 120mm RGB', 'Mousepad Razer Goliathus Extended'])
            ]

            productos = []
            sku_counter = 1000
            for cat_name, items in base_productos:
                categoria = dic_categorias[cat_name]
                for item_name in items:
                    # Determinar precio base aproximado en Quetzales (GTQ) según el nombre
                    if 'RTX 4090' in item_name or 'MacBook Pro' in item_name:
                        precio_compra = random.uniform(15000, 20000)
                    elif 'Laptop' in item_name or 'PC' in item_name or 'iMac' in item_name or 'MacBook' in item_name:
                        precio_compra = random.uniform(3500, 10000)
                    elif 'RTX 4070' in item_name or 'RX 7900' in item_name or 'i9' in item_name or 'Ryzen 9' in item_name:
                        precio_compra = random.uniform(4000, 8000)
                    elif 'Monitor' in item_name or 'Motherboard' in item_name or 'Procesador' in item_name or 'Ryzen 7' in item_name or 'i7' in item_name or 'RTX 3060' in item_name or 'RX 6600' in item_name:
                        precio_compra = random.uniform(1000, 3000)
                    elif 'SSD' in item_name or 'RAM' in item_name or 'Fuente' in item_name or 'Router' in item_name:
                        precio_compra = random.uniform(250, 900)
                    else: # Periféricos, cables y otros
                        precio_compra = random.uniform(50, 400)
                        
                    precio_compra = round(precio_compra, 2)
                    # Margen de ganancia entre 15% y 35%
                    margen = random.uniform(1.15, 1.35)
                    precio_venta = round(precio_compra * margen, 2)
                    
                    # Generar variantes si no llegamos a 100 productos (duplicar con otra marca o capacidad)
                    # Pero con la lista base ya tenemos más de 75 productos. Lleguemos a 100 repitiendo algunos.
                    
                    prod = Producto.objects.create(
                        nombre=item_name,
                        sku=f"PRD-{sku_counter}",
                        categoria=categoria,
                        descripcion=f"{item_name} de alta calidad, ideal para tu setup.",
                        precio_compra=precio_compra,
                        precio_venta=precio_venta,
                        stock=random.randint(10, 150),
                        proveedor_predeterminado=random.choice(proveedores)
                    )
                    productos.append(prod)
                    sku_counter += 1

            # Si nos faltan para los 100, rellenamos con variantes aleatorias
            while len(productos) < 100:
                prod_base = random.choice(productos)
                nuevo_nombre = f"{prod_base.nombre} (Edición Especial)"
                nuevo_sku = f"PRD-{sku_counter}"
                precio_compra = float(prod_base.precio_compra) * 1.10
                
                prod = Producto.objects.create(
                    nombre=nuevo_nombre,
                    sku=nuevo_sku,
                    categoria=prod_base.categoria,
                    descripcion=prod_base.descripcion,
                    precio_compra=round(precio_compra, 2),
                    precio_venta=round(precio_compra * 1.25, 2),
                    stock=random.randint(5, 50),
                    proveedor_predeterminado=random.choice(proveedores)
                )
                productos.append(prod)
                sku_counter += 1

            # 4. Crear 50 Clientes de Guatemala
            self.stdout.write('4. Creando 50 Clientes (formato NIT Guatemala)...')
            clientes = []
            for _ in range(50):
                # Generar NIT realista de Guatemala (ej. 1234567-K o 8765432-1)
                num_base = fake.numerify('#######')
                digito_verificador = random.choice(['1', '2', '3', '4', '5', '6', '7', '8', '9', 'K'])
                nit_gt = f"{num_base}-{digito_verificador}"
                
                prefijo_tel = random.choice(['3', '4', '5'])
                tel_gt = f"{prefijo_tel}{fake.numerify('###-####')}"
                
                cli = Cliente.objects.create(
                    nombre=fake.name(),
                    nit=nit_gt,
                    correo=fake.email(),
                    telefono=tel_gt
                )
                clientes.append(cli)

            # Para facturas, a veces el NIT es "C/F" (Consumidor Final)
            cli_cf, _ = Cliente.objects.get_or_create(
                nombre="Consumidor Final",
                defaults={
                    'nit': 'C/F',
                    'correo': 'cf@example.com',
                    'telefono': '00000000'
                }
            )
            clientes.append(cli_cf)

            # 5. Crear Órdenes de Compra (Simulando el abastecimiento)
            self.stdout.write('5. Creando Órdenes de Compra a proveedores...')
            estados_oc = ['Pendiente', 'Recibida', 'Cancelada']
            for _ in range(150): # 150 ordenes de compra a los proveedores
                prov = random.choice(proveedores)
                prod = random.choice(productos)
                cantidad = random.randint(5, 50)
                costo_total = round(cantidad * float(prod.precio_compra), 2)
                
                oc = OrdenCompra.objects.create(
                    proveedor=prov,
                    producto=prod,
                    cantidad=cantidad,
                    costo_total=costo_total,
                    estado=random.choices(estados_oc, weights=[0.2, 0.7, 0.1])[0] # La mayoría recibidas
                )
                
                # Asignar fecha aleatoria en los últimos 3 meses
                random_days = random.randint(0, 90)
                random_date = timezone.now() - timedelta(days=random_days)
                OrdenCompra.objects.filter(id=oc.id).update(fecha_compra=random_date)

            # 6. Crear 1000 Facturas
            self.stdout.write('6. Creando 1000 Facturas de Venta (Esto tomará tiempo)...')
            estados_fac = ['Borrador', 'Emitida', 'Enviada', 'Pagada']
            
            # Lista para crear las facturas en bloque y acelerar un poco el proceso
            facturas_creadas = []
            
            for i in range(1000):
                # 30% de las ventas son a Consumidor Final
                cli = cli_cf if random.random() < 0.3 else random.choice(clientes)
                
                serie = random.choice(['A', 'B', 'C'])
                num_correlativo = str(i + 1).zfill(6)
                
                estado = random.choices(estados_fac, weights=[0.05, 0.1, 0.1, 0.75])[0] # Mayoría pagadas
                
                factura = Factura.objects.create(
                    cliente=cli,
                    numero_factura=f"FAC-{serie}-{num_correlativo}",
                    total=0,  # Se actualizará luego
                    estado=estado
                )
                
                # Crear entre 1 y 4 detalles para la factura (1 a 4 productos distintos)
                num_detalles = random.randint(1, 4)
                total_factura = decimal.Decimal('0.00')
                productos_seleccionados = random.sample(productos, num_detalles)
                
                for prod in productos_seleccionados:
                    # En tecnología, la gente suele comprar 1 o 2 unidades (ej. 1 laptop, o 2 memorias RAM)
                    cantidad = random.choices([1, 2, 3, 4, 5], weights=[0.7, 0.15, 0.05, 0.05, 0.05])[0]
                    precio_unitario = decimal.Decimal(str(prod.precio_venta))
                    
                    DetalleFactura.objects.create(
                        factura=factura,
                        producto=prod,
                        cantidad=cantidad,
                        precio_unitario=precio_unitario
                    )
                    total_factura += (decimal.Decimal(str(cantidad)) * precio_unitario)
                
                factura.total = total_factura
                factura.save()
                
                # Asignar fecha aleatoria en los últimos 3 meses (90 días)
                random_days = random.randint(0, 90)
                random_date = timezone.now() - timedelta(days=random_days)
                Factura.objects.filter(id=factura.id).update(fecha_venta=random_date)
                
                # Imprimir progreso cada 200 facturas
                if (i + 1) % 200 == 0:
                    self.stdout.write(f"   -> Progreso: {i + 1}/1000 facturas generadas...")

        self.stdout.write(self.style.SUCCESS('¡Datos de tienda de computación en Guatemala generados exitosamente!'))
