"""
BOT DE FACTURACIÓN Y REPORTES

Escanea continuamente el ERP en busca de facturas recién generadas en estado 'Emitida'. 
Simula el proceso de enviarlas al cliente, y luego actualiza su estado a 'Enviada' 
mediante la API para evitar re-procesos.
"""
import requests
import time
import sys

# Forzar codificación UTF-8 en la consola de Windows para evitar errores con emojis
sys.stdout.reconfigure(encoding='utf-8')

API_URL = "https://erp-django-smea.onrender.com/api/v1/facturas/"

def run_bot():
    print("🤖 Iniciando Bot de Reportes y Facturación...")
    print("🔍 Buscando facturas en estado 'Emitida'...")
    
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            facturas = response.json()
            # Asumiendo que facturas es una lista, o dict si hay paginación. 
            # Si DRF usa paginación, facturas['results']
            facturas_list = facturas if isinstance(facturas, list) else facturas.get('results', [])
            
            pendientes = [f for f in facturas_list if f['estado'] == 'Emitida']
            
            if not pendientes:
                print("✅ No hay facturas pendientes de envío.")
                return
            
            print(f"📦 Se encontraron {len(pendientes)} facturas por procesar.")
            
            for factura in pendientes:
                print(f"\n⏳ Procesando Factura #{factura['numero_factura']} (Total: Q.{factura['total']})...")
                time.sleep(1) # Simular generación de PDF
                print(f"📧 ¡Factura enviada al cliente por correo electrónico!")
                
                # Actualizar estado a Enviada
                patch_url = f"{API_URL}{factura['id']}/"
                patch_response = requests.patch(patch_url, json={"estado": "Enviada"})
                
                if patch_response.status_code == 200:
                    print(f"✅ Estado de factura actualizado a 'Enviada' en el ERP.")
                else:
                    print(f"❌ Error al actualizar estado: {patch_response.text}")
                    
        else:
            print(f"❌ Error al conectar con la API: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error crítico: {e}")

if __name__ == "__main__":
    run_bot()
