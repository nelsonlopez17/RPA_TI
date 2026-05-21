import sys
try:
    import requests
except ImportError:
    import urllib.request as _urllib
    import json as _json
    class SimpleRequests:
        @staticmethod
        def get(url):
            resp = _urllib.urlopen(url)
            return type('Response', (), {'status_code': resp.getcode(), 'json': lambda: _json.loads(resp.read().decode())})
        @staticmethod
        def post(url, json=None):
            data = _json.dumps(json).encode() if json else None
            req = _urllib.Request(url, data=data, headers={'Content-Type': 'application/json'})
            resp = _urllib.urlopen(req)
            return type('Response', (), {'status_code': resp.getcode(), 'text': resp.read().decode(), 'json': lambda: _json.loads(resp.read().decode())})
        @staticmethod
        def patch(url, json=None):
            data = _json.dumps(json).encode() if json else None
            req = _urllib.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='PATCH')
            resp = _urllib.urlopen(req)
            return type('Response', (), {'status_code': resp.getcode(), 'text': resp.read().decode()})
    requests = SimpleRequests
sys.stdout.reconfigure(encoding='utf-8')
import requests
import time

ALERTAS_URL = "http://127.0.0.1:8000/api/v1/alertas/"
ORDENES_URL = "http://127.0.0.1:8000/api/v1/ordenes/"
PRODUCTOS_URL = "http://127.0.0.1:8000/api/v1/productos/"

STOCK_OBJETIVO = 50  # Cantidad ideal de stock a la que queremos llegar
STOCK_LIMITE_ALERTA = 10  # Umbral para disparar una alerta de bajo stock


def calcular_cantidad(producto_id, stock_objetivo):
    """Obtiene stock y precio del producto desde la API.
    Si el producto no existe o la llamada falla, devuelve None.
    """
    try:
        response = requests.get(f"{PRODUCTOS_URL}{producto_id}/")
        if response.status_code == 200:
            producto = response.json()
            stock_actual = producto.get('stock', 0)
            precio_compra = float(producto.get('precio_compra', 0))
            cantidad = max(stock_objetivo - stock_actual, 1)
            costo_total = round(cantidad * precio_compra, 2)
            return cantidad, costo_total, producto.get('nombre', f'Producto #{producto_id}'), stock_actual, producto.get('proveedor_predeterminado') or producto.get('proveedor_id')
    except Exception as e:
        print(f"⚠️ Error al consultar producto #{producto_id}: {e}")
    # Producto no encontrado o error
    return None


def run_bot():
    """Verifica en tiempo real el stock de todos los productos.
    - Genera alertas temporales si y solo si el stock es menor a 10.
    - Muestra la información de los productos con bajo stock.
    - Finalmente crea las órdenes de compra para alcanzar un stock de 50.
    """
    print("🤖 Iniciando Bot de Abastecimiento (M2M) v2.0...")
    print("📡 Consultando stock de todos los productos...")

    try:
        # Obtener todos los productos
        response = requests.get(PRODUCTOS_URL)
        if response.status_code != 200:
            print(f"❌ Error al obtener productos: {response.status_code}")
            return
        productos = response.json()
        if isinstance(productos, dict):
            # Cuando la API devuelve {'results': [...]}
            productos = productos.get('results', [])

        low_stock_items = []
        # Verificar cada producto
        for prod in productos:
            prod_id = prod.get('id')
            nombre = prod.get('nombre', f'Producto #{prod_id}')
            stock = prod.get('stock', 0)
            # Solo alertar si el stock es estrictamente menor a 10
            if stock < STOCK_LIMITE_ALERTA:
                # Alerta temporal (no se persiste en BD)
                print(f"⚠️  ALERTA: {nombre} (SKU: {prod.get('sku')}) tiene {stock} unidades (umbral crítico: {STOCK_LIMITE_ALERTA})")
                low_stock_items.append(prod)

        if not low_stock_items:
            print(f"✅ Todos los productos tienen suficiente stock (>= {STOCK_LIMITE_ALERTA}). No se generan alertas.")
            return

        # Mostrar información consolidada
        print(f"\n📊 Se encontraron {len(low_stock_items)} productos con bajo stock:")
        for prod in low_stock_items:
            nombre = prod.get('nombre', f'Producto #{prod.get("id")}')
            sku = prod.get('sku')
            stock = prod.get('stock', 0)
            print(f"- {nombre} (SKU: {sku}) – Stock actual: {stock}")

        # Obtener órdenes existentes para evitar duplicados
        productos_con_orden_pendiente = set()
        try:
            ordenes_resp = requests.get(ORDENES_URL)
            if ordenes_resp.status_code == 200:
                ordenes = ordenes_resp.json()
                ordenes_list = ordenes if isinstance(ordenes, list) else ordenes.get('results', [])
                for ord in ordenes_list:
                    if ord.get('estado') in ['Pendiente', 'En proceso', 'Procesando']:
                        productos_con_orden_pendiente.add(ord.get('producto'))
        except Exception as e:
            print(f"⚠️ No se pudieron consultar las órdenes existentes: {e}")

        # Crear órdenes de compra para cada producto con proveedor disponible
        print("\n🚚 Generando órdenes de compra...")
        for prod in low_stock_items:
            prod_id = prod.get('id')
            nombre = prod.get('nombre', f'Producto #{prod_id}')
            
            # Verificar duplicados antes de crear
            if prod_id in productos_con_orden_pendiente:
                print(f"ℹ️  Ya existe una orden de compra pendiente para {nombre}. Se omite la creación.")
                continue

            stock_actual = prod.get('stock', 0)
            precio_compra = float(prod.get('precio_compra', 0))
            cantidad = max(STOCK_OBJETIVO - stock_actual, 1)
            costo_total = round(cantidad * precio_compra, 2)
            proveedor = prod.get('proveedor_predeterminado') or prod.get('proveedor_id')
            if not proveedor:
                print(f"⚠️  Sin proveedor para {nombre}. No se crea orden.")
                continue
            orden_payload = {
                "proveedor": proveedor,
                "producto": prod_id,
                "cantidad": cantidad,
                "costo_total": str(costo_total),
                "estado": "Pendiente"
            }
            orden_resp = requests.post(ORDENES_URL, json=orden_payload)
            if orden_resp.status_code == 201:
                orden = orden_resp.json()
                print(f"✅ Orden creada para {nombre}: #{orden.get('id')} (cantidad {cantidad})")
            else:
                print(f"❌ Error al crear orden para {nombre}: {orden_resp.text}")

    except Exception as e:
        print(f"❌ Error crítico durante la ejecución: {e}")

if __name__ == "__main__":
    run_bot()
