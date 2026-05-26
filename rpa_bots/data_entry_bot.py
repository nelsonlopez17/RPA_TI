import csv
import requests
import time
import sys

# Forzar codificación UTF-8 en la consola de Windows para evitar errores con emojis
sys.stdout.reconfigure(encoding='utf-8')


API_URL = "https://erp-django-smea.onrender.com/api/v1/productos/"
CSV_PATH = "data/nuevos_productos.csv"

def run_bot():
    print("🤖 Iniciando Bot de Data Entry...")
    print(f"📄 Leyendo archivo: {CSV_PATH}")
    
    with open(CSV_PATH, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            print(f"⏳ Procesando: {row['nombre']} (SKU: {row['sku']})")
            
            payload = {
                "nombre": row['nombre'],
                "sku": row['sku'],
                "categoria": int(row['categoria']),
                "descripcion": row['descripcion'],
                "precio_compra": row['precio_compra'],
                "precio_venta": row['precio_venta'],
                "stock": int(row['stock'])
            }
            
            try:
                response = requests.post(API_URL, json=payload)
                if response.status_code == 201:
                    print(f"✅ ¡Éxito! Producto '{row['nombre']}' registrado en el ERP.")
                else:
                    print(f"❌ Error al registrar '{row['nombre']}': {response.status_code} - {response.text}")
            except Exception as e:
                print(f"❌ Error de conexión: {e}")
            
            # Simular tiempo de carga humano (opcional, para visualización de RPA)
            time.sleep(1)
            
    print("🏁 Bot de Data Entry finalizó sus tareas.")

if __name__ == "__main__":
    run_bot()
